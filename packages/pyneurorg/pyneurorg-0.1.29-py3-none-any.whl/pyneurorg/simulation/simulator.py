# src/pyneurorg/simulation/simulator.py

"""
Defines the Simulator class for orchestrating pyneurorg simulations.
"""

import brian2 as b2
import numpy as np
from ..organoid.organoid import Organoid
from ..mea.mea import MEA
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
        # No stimulus_namespace_counter needed if assigning directly to variable slices

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

        The `target_current_var` (default: 'I_input') of the identified target neurons
        will be set to follow the `stimulus_waveform` (a Brian2 TimedArray).
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

        # --- CORRECTED APPROACH FOR APPLYING TIMEDARRAY TO SUBGROUP ---
        # Directly assign the TimedArray to the sliced/indexed state variable
        # of the NeuronGroup. Brian2 handles making the variable for these
        # specific neurons follow the TimedArray over time.
        try:
            # Get the VariableView for the target current variable
            variable_to_set = getattr(target_ng, target_current_var)
            # Assign the TimedArray to the slice of neurons
            variable_to_set[target_neuron_indices] = stimulus_waveform
            
            print(f"Stimulus from electrode {electrode_id} assigned to '{target_current_var}' of "
                  f"{len(target_neuron_indices)} neurons in '{target_group_name}'.")
            # TimedArrays are not BrianObjects that need to be in the Network collection
            # if assigned to a group variable. The group itself holds the reference.
            self._stimulus_current_sources.append(stimulus_waveform) # Keep our own reference
        except Exception as e:
            print(f"Error assigning TimedArray to subgroup for variable '{target_current_var}': {e}")
            print("Ensure that the variable is part of the NeuronGroup's equations "
                  "(e.g., 'I_input : amp') and can be indexed by a TimedArray.")
            raise
        # --- END OF CORRECTED APPROACH ---


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