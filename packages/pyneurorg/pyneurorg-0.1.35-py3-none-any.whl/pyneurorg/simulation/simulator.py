# src/pyneurorg/simulation/simulator.py

import brian2 as b2
import numpy as np
from ..organoid.organoid import Organoid
from ..mea.mea import MEA
from ..electrophysiology import brian_monitors as pbg_monitors

class Simulator:
    def __init__(self, organoid: Organoid, mea: MEA = None, brian2_dt=None):
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
        self._stimulus_current_sources = [] # Keep track of TimedArray objects
        self._stimulus_namespace_counter = 0 # For unique TimedArray names in namespace
        # Track if reset operation for a cumulative stimulus variable in a group has been added
        self._cumulative_stim_vars_reset_added = set() # Stores tuples: (group_name, cumulative_stim_var_name)

    def set_mea(self, mea_instance: MEA):
        if not isinstance(mea_instance, MEA):
            raise TypeError("mea_instance must be an instance of pyneurorg.mea.MEA.")
        self.mea = mea_instance
        print(f"Simulator MEA set to: {mea_instance.name}")

    def add_stimulus(self, electrode_id: int, stimulus_waveform: b2.TimedArray,
                     target_group_name: str, influence_radius,
                     cumulative_stim_var: str = 'I_stimulus_sum',
                     flag_variable_template: str = "is_targeted_by_stim{id}"):
        """
        Adds a stimulus to be applied via a specified MEA electrode to nearby neurons.

        This method configures a boolean flag for targeted neurons and uses
        `run_regularly` operations to sum the stimulus current into a
        cumulative current variable in the neuron model.

        Parameters
        ----------
        electrode_id : int
            The ID (index) of the MEA electrode.
        stimulus_waveform : brian2.input.timedarray.TimedArray
            The pre-generated stimulus current.
        target_group_name : str
            Name of the NeuronGroup to target.
        influence_radius : float or brian2.units.fundamentalunits.Quantity
            Radius around the electrode to find target neurons.
        cumulative_stim_var : str, optional
            The variable in the neuron model that accumulates stimulus currents
            (e.g., 'I_stimulus_sum'). Default is 'I_stimulus_sum'.
            This variable should be initialized to 0*amp at each time step by a
            separate reset operation.
        flag_variable_template : str, optional
            A template string for the boolean flag variable name in the neuron model.
            '{id}' will be replaced by `electrode_id`.
            Example: "is_targeted_by_stim{id}" becomes "is_targeted_by_stim0".
            Default is "is_targeted_by_stim{id}".
        """
        if self.mea is None: raise ValueError("No MEA set for this simulator.")
        if not isinstance(stimulus_waveform, b2.TimedArray): raise TypeError("stimulus_waveform must be a TimedArray.")

        target_ng = self.organoid.get_neuron_group(target_group_name)

        if cumulative_stim_var not in target_ng.variables:
            raise AttributeError(f"Target NeuronGroup '{target_group_name}' must have a variable "
                                 f"'{cumulative_stim_var}' for summing stimuli. "
                                 f"Available: {list(target_ng.variables.keys())}")

        current_flag_name = flag_variable_template.format(id=electrode_id)
        if current_flag_name not in target_ng.variables:
            raise AttributeError(
                f"Target NeuronGroup '{target_group_name}' does not have the boolean flag variable "
                f"'{current_flag_name}' defined in its equations. This flag is needed to "
                f"target neurons for stimulus from electrode {electrode_id}."
            )

        target_neuron_indices_np = self.mea.get_neurons_near_electrode(
            organoid=self.organoid, neuron_group_name=target_group_name,
            electrode_id=electrode_id, radius=influence_radius
        )

        if len(target_neuron_indices_np) == 0:
            print(f"Warning: No neurons found for stimulus from electrode {electrode_id} in group '{target_group_name}'.")
            return

        # 1. Set the specific boolean flag for the targeted neurons
        # Ensure other neurons have this specific flag as False (should be default from model)
        # getattr(target_ng, current_flag_name)[:] = False # Reset all for this flag (optional, if flags can be reused dynamically)
        getattr(target_ng, current_flag_name)[target_neuron_indices_np] = True
        print(f"Flag '{current_flag_name}' set to True for {len(target_neuron_indices_np)} neurons.")

        # 2. Ensure TimedArray is in the NeuronGroup's namespace with a unique name
        ta_name_in_ns = stimulus_waveform.name
        is_generic_name = ta_name_in_ns is None or \
                          ta_name_in_ns.startswith(('_timedarray', 'timedarray'))
        if is_generic_name or \
           (ta_name_in_ns in target_ng.namespace and \
            target_ng.namespace[ta_name_in_ns] is not stimulus_waveform):
            ta_name_in_ns = f'pyneurorg_stim_ta_{self._stimulus_namespace_counter}'
            self._stimulus_namespace_counter += 1
        target_ng.namespace[ta_name_in_ns] = stimulus_waveform
        
        # 3. Ensure there's an operation to reset the cumulative_stim_var at the start of each time step
        # This reset operation is added only ONCE per (target_group, cumulative_stim_var) combination.
        reset_op_key = (target_group_name, cumulative_stim_var)
        if reset_op_key not in self._cumulative_stim_vars_reset_added:
            reset_op_name = f'reset__{target_group_name}__{cumulative_stim_var}'
            reset_code = f"{cumulative_stim_var} = 0*amp" # Reset to 0 ampere
            
            reset_operation = target_ng.run_regularly(
                reset_code, 
                dt=self.brian_dt, # Run every simulation step
                when='start',     # Run at the very beginning of the step
                order=-1,         # Run before other 'start' operations
                name=reset_op_name 
            )
            if reset_operation not in self._network_objects:
                self._network_objects.append(reset_operation)
            self._cumulative_stim_vars_reset_added.add(reset_op_key)
            print(f"Added reset operation ('{reset_op_name}') for '{cumulative_stim_var}' in group '{target_group_name}'.")

        # 4. Create the operation to SUM this specific stimulus waveform
        #    to the cumulative_stim_var if the neuron's flag is True.
        sum_code = f"""
if {current_flag_name}:
    {cumulative_stim_var} += {ta_name_in_ns}(t)
"""
        sum_op_name = f'sum_stim_e{electrode_id}_to_{cumulative_stim_var}_in_{target_group_name}'
        
        try:
            stim_sum_operation = target_ng.run_regularly(
                sum_code, 
                dt=self.brian_dt, 
                when='start', # Run at the start of the step
                order=0,      # Run after the reset operation (order -1)
                name=sum_op_name
            )
            if stim_sum_operation not in self._network_objects:
                self._network_objects.append(stim_sum_operation)
            self._stimulus_current_sources.append(stimulus_waveform) # Keep ref to TA
            print(f"Summing stimulus operation '{sum_op_name}' added for electrode {electrode_id}.")
        except Exception as e:
            print(f"Error configuring summing run_regularly for stimulus on '{cumulative_stim_var}': {e}")
            # Clean up namespace for TimedArray if summing op failed
            if ta_name_in_ns in target_ng.namespace and target_ng.namespace[ta_name_in_ns] is stimulus_waveform:
                del target_ng.namespace[ta_name_in_ns]
            # Resetting the flag might be complex if other stimuli use it, best to ensure model is correct
            # getattr(target_ng, current_flag_name)[target_neuron_indices_np] = False 
            raise

    # ... (add_recording, build_network, run, get_data, etc. as in the last complete version) ...
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