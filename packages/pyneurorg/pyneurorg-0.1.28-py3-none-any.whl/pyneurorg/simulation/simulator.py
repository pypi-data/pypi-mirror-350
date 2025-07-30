# src/pyneurorg/simulation/simulator.py

"""
Defines the Simulator class for orchestrating pyneurorg simulations.

The Simulator class takes an Organoid instance, allows adding monitors,
constructs a Brian2 Network, and runs the simulation.
"""

import brian2 as b2
import numpy as np # Import numpy for array operations
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
        self._stimulus_current_sources = []
        self._stimulus_namespace_counter = 0

    def set_mea(self, mea_instance: MEA):
        """
        Sets or updates the MEA associated with this simulator.
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
        """
        if self.mea is None:
            raise ValueError("No MEA has been set for this simulator. Call set_mea() or provide at init.")
        if not isinstance(stimulus_waveform, b2.TimedArray):
            raise TypeError("stimulus_waveform must be a Brian2 TimedArray.")

        target_ng = self.organoid.get_neuron_group(target_group_name)

        if not hasattr(target_ng, target_current_var):
            raise AttributeError(f"Target neuron group '{target_group_name}' does not have "
                                 f"a variable named '{target_current_var}'. "
                                 f"Ensure it's defined in the model equations (e.g., '{target_current_var} : amp').")

        target_neuron_indices_np = self.mea.get_neurons_near_electrode( # Returns a NumPy array
            organoid=self.organoid,
            neuron_group_name=target_group_name,
            electrode_id=electrode_id,
            radius=influence_radius
        )

        if len(target_neuron_indices_np) == 0:
            print(f"Warning: No neurons found within radius {influence_radius} of electrode {electrode_id} "
                  f"in group '{target_group_name}'. Stimulus will not be applied.")
            return

        # --- CORRECTED APPROACH FOR APPLYING TIMEDARRAY TO SUBGROUP USING RUN_ON_EVENT ---
        # 1. Ensure the TimedArray has a unique name for the NeuronGroup's namespace.
        timed_array_name_in_namespace = stimulus_waveform.name
        is_generic_name = timed_array_name_in_namespace is None or \
                          timed_array_name_in_namespace.startswith(('_timedarray', 'timedarray'))
        
        if is_generic_name or \
           (timed_array_name_in_namespace in target_ng.namespace and \
            target_ng.namespace[timed_array_name_in_namespace] is not stimulus_waveform):
            timed_array_name_in_namespace = f'pyneurorg_stim_ta_{self._stimulus_namespace_counter}'
            self._stimulus_namespace_counter += 1
        
        target_ng.namespace[timed_array_name_in_namespace] = stimulus_waveform

        # 2. Make the target indices available in the NeuronGroup's namespace.
        #    The name must be a valid Python variable name.
        target_indices_name_in_namespace = f'stim_target_indices_{self._stimulus_namespace_counter-1}' # Link to the TA counter
        target_ng.namespace[target_indices_name_in_namespace] = target_neuron_indices_np # Pass NumPy array of indices

        # 3. Define the code to be executed, conditioned on neuron index 'i'.
        #    The special variable 'i' refers to the neuron index within the group.
        code_to_run = f"""
if i in {target_indices_name_in_namespace}:
    {target_current_var} = {timed_array_name_in_namespace}(t)
else:
    pass 
    # Or, if I_input should be zero for non-targeted by this stimulus:
    # {target_current_var} = 0 * amp 
    # This 'else' part is tricky if I_input is also used by other things like synapses.
    # For now, we only set the current for the targeted neurons.
    # Other neurons' I_input will be unaffected by this specific run_on_event.
    # If I_input is *only* for external stimuli and not summed with synaptic inputs,
    # then setting it to 0 for non-targets might be desired.
    # However, if I_input is also a sum of synaptic currents, this 'else' would zero them out.
    # Let's assume for now that I_input can be driven by multiple sources or is reset elsewhere if needed.
    # The simplest is to only act on the 'if i in target_indices'.
"""
        # More concise way to only act on the subset without an explicit else:
        code_to_run_concise = f"""
if i in {target_indices_name_in_namespace}:
    {target_current_var} = {timed_array_name_in_namespace}(t)
"""
        # --- END OF CORRECTED APPROACH ---
        try:
            # Schedule this code to run at the start of each time step.
            # The 'subset' argument is NOT used here. The subset logic is in the 'code'.
            target_ng.run_on_event(
                event='start',
                code=code_to_run_concise # Use the concise version
            )
            print(f"Stimulus from electrode {electrode_id} (TimedArray '{timed_array_name_in_namespace}', "
                  f"Indices '{target_indices_name_in_namespace}') "
                  f"configured via run_on_event for '{target_current_var}' "
                  f"of {len(target_neuron_indices_np)} neurons in '{target_group_name}'.")
            self._stimulus_current_sources.append(stimulus_waveform)
        except Exception as e:
            print(f"Error configuring run_on_event for stimulus on '{target_current_var}': {e}")
            # Clean up namespace if setup failed
            if timed_array_name_in_namespace in target_ng.namespace:
                del target_ng.namespace[timed_array_name_in_namespace]
            if target_indices_name_in_namespace in target_ng.namespace:
                del target_ng.namespace[target_indices_name_in_namespace]
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
        self.brian_network = b2.Network(self._network_objects, **network_kwargs)

    def run(self, duration: b2.units.fundamentalunits.Quantity, report=None, report_period=10*b2.second, **run_kwargs):
        if not isinstance(duration, b2.Quantity) or not (duration.dimensions == b2.second.dimensions):
            raise TypeError("duration must be a Brian2 Quantity with time units.")
        if self.brian_network is None: self.build_network(**run_kwargs.pop('network_kwargs', {}))
        if self.brian_network is None: raise RuntimeError("Brian2 Network could not be built.")
        self.brian_network.run(duration, report=report, report_period=report_period, **run_kwargs)

    def get_data(self, monitor_name: str):
        if monitor_name not in self.monitors: raise KeyError(f"Monitor '{monitor_name}' not found. Available: {list(self.monitors.keys())}")
        return self.monitors[monitor_name]

    def store_simulation(self, filename="pyneurorg_sim_state"):
        if self.brian_network is None: print("Warning: Network not built. Nothing to store."); return
        self.brian_network.store(name=filename); print(f"State stored in '{filename}.bri'")

    def restore_simulation(self, filename="pyneurorg_sim_state"):
        if self.brian_network is None: print("Warning: Network not explicitly built before restore.")
        b2.restore(name=filename); print(f"State restored from '{filename}.bri'. Network may need rebuild.")
        self.brian_network = None; self.brian_dt = b2.defaultclock.dt

    def __str__(self):
        status = "Built" if self.brian_network else "Not Built"; num_monitors = len(self.monitors)
        return (f"<Simulator for Organoid '{self.organoid.name}' "
                f"with {num_monitors} monitor(s). Network Status: {status}>")
    def __repr__(self): return self.__str__()