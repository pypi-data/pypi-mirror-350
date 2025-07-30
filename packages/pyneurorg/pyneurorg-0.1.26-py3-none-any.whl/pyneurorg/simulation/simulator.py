# src/pyneurorg/simulation/simulator.py

"""
Defines the Simulator class for orchestrating pyneurorg simulations.

The Simulator class takes an Organoid instance, allows adding monitors,
constructs a Brian2 Network, and runs the simulation.
"""

import brian2 as b2
from ..organoid.organoid import Organoid # For type hinting
from ..mea.mea import MEA # Import MEA class
from ..electrophysiology import brian_monitors as pbg_monitors

class Simulator:
    """
    Orchestrates Brian2 simulations for a given pyneurorg Organoid,
    optionally interacting with an MEA for stimulation.
    """

    def __init__(self, organoid: Organoid, mea: MEA = None, brian2_dt=None):
        """
        Initializes a new Simulator instance.

        Parameters
        ----------
        organoid : pyneurorg.organoid.organoid.Organoid
            The pyneurorg Organoid instance to be simulated.
        mea : pyneurorg.mea.mea.MEA, optional
            An MEA instance associated with this simulation for stimulation
            and potentially recording (default: None).
        brian2_dt : brian2.units.fundamentalunits.Quantity, optional
            The default clock dt for the simulation.
        """
        if not isinstance(organoid, Organoid):
            raise TypeError("organoid must be an instance of pyneurorg.organoid.Organoid.")
        if mea is not None and not isinstance(mea, MEA):
            raise TypeError("mea must be an instance of pyneurorg.mea.MEA or None.")

        self.organoid = organoid
        self.mea = mea
        self.brian_network = None
        self.monitors = {} 
        
        if brian2_dt is not None:
            if not isinstance(brian2_dt, b2.Quantity) or not (brian2_dt.dimensions == b2.second.dimensions):
                raise TypeError("brian2_dt must be a Brian2 Quantity with time units.")
            self.brian_dt = brian2_dt
            b2.defaultclock.dt = self.brian_dt 
        else:
            self.brian_dt = b2.defaultclock.dt 
        
        self._network_objects = list(self.organoid.brian2_objects)
        self._stimulus_current_sources = [] # To keep track of TimedArrays for stimuli
        self._stimulus_counter = 0 # For unique TimedArray names

    def set_mea(self, mea_instance: MEA):
        """
        Sets or updates the MEA associated with this simulator.

        Parameters
        ----------
        mea_instance : pyneurorg.mea.mea.MEA
            The MEA instance to associate.
        """
        if not isinstance(mea_instance, MEA):
            raise TypeError("mea_instance must be an instance of pyneurorg.mea.MEA.")
        self.mea = mea_instance
        print(f"Simulator MEA set to: {mea_instance.name}")

    def add_stimulus(self, electrode_id: int, stimulus_waveform: b2.TimedArray,
                     target_group_name: str, influence_radius,
                     target_current_var: str = 'I_input'):
        """
        Adds a stimulus to be applied via a specified MEA electrode to nearby neurons.

        The stimulus_waveform (a Brian2 TimedArray) will define the value of
        `target_current_var` (default: 'I_input') for the identified target neurons
        at each time step, using Brian2's `run_on_event` mechanism.

        Parameters
        ----------
        electrode_id : int
            The ID (index) of the MEA electrode to apply the stimulus from.
        stimulus_waveform : brian2.input.timedarray.TimedArray
            The pre-generated stimulus current. Its values should have current dimensions.
        target_group_name : str
            The name of the NeuronGroup within the organoid to target.
        influence_radius : float or brian2.units.fundamentalunits.Quantity
            The radius around the electrode to find target neurons.
            If a float, assumed to be in micrometers (um).
        target_current_var : str, optional
            The name of the current variable in the target neuron model to which
            the stimulus will be applied (default: 'I_input'). This variable
            must be defined in the neuron's equations (e.g., `I_input : amp`).

        Raises
        ------
        ValueError
            If MEA is not set, electrode_id is invalid, or target_group_name is not found.
        TypeError
            If stimulus_waveform is not a TimedArray or influence_radius has wrong type.
        AttributeError
            If the target_current_var does not exist in the target NeuronGroup.
        """
        if self.mea is None:
            raise ValueError("No MEA has been set for this simulator. Call set_mea() or provide at init.")
        if not isinstance(stimulus_waveform, b2.TimedArray):
            raise TypeError("stimulus_waveform must be a Brian2 TimedArray.")

        target_ng = self.organoid.get_neuron_group(target_group_name)

        if not hasattr(target_ng, target_current_var): # Check if variable exists on the group object
            # More robust check: Check target_ng.variables (Brian2 internal)
            # However, hasattr usually works for state variables defined in equations.
            raise AttributeError(f"Target neuron group '{target_group_name}' does not have "
                                 f"a variable named '{target_current_var}'. "
                                 f"Ensure it's defined in the model equations (e.g., '{target_current_var} : amp').")

        target_neuron_indices = self.mea.get_neurons_near_electrode(
            organoid=self.organoid,
            neuron_group_name=target_group_name,
            electrode_id=electrode_id,
            radius=influence_radius
        )

        if len(target_neuron_indices) == 0:
            print(f"Warning: No neurons found within radius {influence_radius} of electrode {electrode_id} "
                  f"in group '{target_group_name}'. Stimulus will not be applied.")
            return

        # Ensure the TimedArray has a unique name for the NeuronGroup's namespace
        # and for the code string in run_on_event.
        unique_timed_array_name = f'stimulus_ta_{self._stimulus_counter}'
        self._stimulus_counter += 1
        stimulus_waveform.name = unique_timed_array_name # Assign the unique name to the object

        # Add the TimedArray to the target NeuronGroup's namespace so it can be referenced
        if unique_timed_array_name in target_ng.namespace:
            print(f"Warning: TimedArray name '{unique_timed_array_name}' already in target NeuronGroup namespace. Overwriting.")
        target_ng.namespace[unique_timed_array_name] = stimulus_waveform
        
        # Define the code to be executed for the subset of neurons
        # This will set target_current_var = stimulus_waveform(t) for the selected neurons
        code_to_run = f"{target_current_var} = {unique_timed_array_name}(t)"

        try:
            # Schedule this code to run for the subset at the start of each time step
            target_ng.run_on_event(
                event='start',  # Run at the start of each time step
                code=code_to_run,
                subset=target_neuron_indices
            )
            print(f"Stimulus from electrode {electrode_id} (using TimedArray '{unique_timed_array_name}') "
                  f"configured via run_on_event for '{target_current_var}' "
                  f"of {len(target_neuron_indices)} neurons in '{target_group_name}'.")
            self._stimulus_current_sources.append(stimulus_waveform) # Keep a reference
        except Exception as e:
            print(f"Error configuring run_on_event for stimulus on '{target_current_var}': {e}")
            # Clean up namespace if it failed?
            if unique_timed_array_name in target_ng.namespace and target_ng.namespace[unique_timed_array_name] is stimulus_waveform:
                del target_ng.namespace[unique_timed_array_name]
            raise


    def add_recording(self, monitor_name: str, monitor_type: str, target_group_name: str, **kwargs):
        if monitor_name in self.monitors:
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        target_group = self.organoid.get_neuron_group(target_group_name)
        monitor_object = None
        brian2_monitor_internal_name = kwargs.pop('name', f"pyb_mon_{monitor_name}_{target_group.name}")
        if monitor_type.lower() == "spike":
            monitor_object = pbg_monitors.setup_spike_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
        elif monitor_type.lower() == "state":
            if 'variables' not in kwargs: raise KeyError("'variables' (str or list) is required for 'state' monitor.")
            monitor_object = pbg_monitors.setup_state_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
        elif monitor_type.lower() == "population_rate":
            monitor_object = pbg_monitors.setup_population_rate_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
        else:
            raise ValueError(f"Unsupported monitor_type: '{monitor_type}'. Supported: 'spike', 'state', 'population_rate'.")
        if monitor_object is not None:
            self.monitors[monitor_name] = monitor_object
            if monitor_object not in self._network_objects: self._network_objects.append(monitor_object)
        return monitor_object

    def build_network(self, **network_kwargs):
        # NeuronGroups (which now might contain TimedArrays in their namespace due to add_stimulus)
        # are already in self._network_objects via self.organoid.brian2_objects.
        # Monitors are also added to self._network_objects.
        # Brian2's Network constructor should handle objects and their namespaces correctly.
        self.brian_network = b2.Network(self._network_objects, **network_kwargs)

    def run(self, duration: b2.units.fundamentalunits.Quantity, report=None, report_period=10*b2.second, **run_kwargs):
        if not isinstance(duration, b2.Quantity) or not (duration.dimensions == b2.second.dimensions):
            raise TypeError("duration must be a Brian2 Quantity with time units.")
        if self.brian_network is None: self.build_network(**run_kwargs.pop('network_kwargs', {}))
        if self.brian_network is None: raise RuntimeError("Brian2 Network could not be built.")
        self.brian_network.run(duration, report=report, report_period=report_period, **run_kwargs)

    def get_data(self, monitor_name: str):
        if monitor_name not in self.monitors: raise KeyError(f"Monitor with name '{monitor_name}' not found. Available monitors: {list(self.monitors.keys())}")
        return self.monitors[monitor_name]

    def store_simulation(self, filename="pyneurorg_sim_state"):
        if self.brian_network is None: print("Warning: Network not built. Nothing to store."); return
        self.brian_network.store(name=filename); print(f"Simulation state stored in '{filename}.bri'")

    def restore_simulation(self, filename="pyneurorg_sim_state"):
        if self.brian_network is None: print("Warning: Network not explicitly built locally before restore. Brian2 will handle network object.")
        b2.restore(name=filename); print(f"State restored from '{filename}.bri'. Network may need rebuild on next run.")
        self.brian_network = None; self.brian_dt = b2.defaultclock.dt

    def __str__(self):
        status = "Built" if self.brian_network else "Not Built"; num_monitors = len(self.monitors)
        return (f"<Simulator for Organoid '{self.organoid.name}' "
                f"with {num_monitors} user-defined monitor(s). Network Status: {status}>")
    def __repr__(self): return self.__str__()