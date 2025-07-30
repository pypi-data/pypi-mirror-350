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
        self._run_regularly_ops = [] # To store run_regularly operations

    def set_mea(self, mea_instance: MEA):
        if not isinstance(mea_instance, MEA):
            raise TypeError("mea_instance must be an instance of pyneurorg.mea.MEA.")
        self.mea = mea_instance
        print(f"Simulator MEA set to: {mea_instance.name}")

    def add_stimulus(self, electrode_id: int, stimulus_waveform: b2.TimedArray,
                     target_group_name: str, influence_radius,
                     target_current_var: str = 'I_stimulus'):
        """
        Adds a stimulus to be applied via a specified MEA electrode to nearby neurons.

        The `target_current_var` of the identified target neurons will be updated
        at each time step by the `stimulus_waveform` using `run_regularly`.
        """
        if self.mea is None:
            raise ValueError("No MEA has been set for this simulator.")
        if not isinstance(stimulus_waveform, b2.TimedArray):
            raise TypeError("stimulus_waveform must be a Brian2 TimedArray.")

        target_ng = self.organoid.get_neuron_group(target_group_name)

        if target_current_var not in target_ng.variables:
            raise AttributeError(
                f"Target NeuronGroup '{target_group_name}' does not have "
                f"a state variable named '{target_current_var}' defined in its equations. "
                f"Available variables: {list(target_ng.variables.keys())}."
            )

        target_neuron_indices_np = self.mea.get_neurons_near_electrode(
            organoid=self.organoid,
            neuron_group_name=target_group_name,
            electrode_id=electrode_id,
            radius=influence_radius
        )

        if len(target_neuron_indices_np) == 0:
            print(f"Warning: No neurons found for stimulus from electrode {electrode_id}.")
            return

        # --- CORRECTED APPROACH USING NeuronGroup.run_regularly ---
        # 1. Ensure TimedArray and target indices are in the NeuronGroup's namespace.
        ta_name_in_ns = stimulus_waveform.name
        if ta_name_in_ns is None or ta_name_in_ns.startswith(('_timedarray', 'timedarray')) or \
           (ta_name_in_ns in target_ng.namespace and target_ng.namespace[ta_name_in_ns] is not stimulus_waveform):
            ta_name_in_ns = f'pyneurorg_stim_ta_{self._stimulus_namespace_counter}'
            self._stimulus_namespace_counter += 1
        target_ng.namespace[ta_name_in_ns] = stimulus_waveform

        indices_name_in_ns = f'target_indices_stim_{self._stimulus_namespace_counter-1}'
        target_ng.namespace[indices_name_in_ns] = target_neuron_indices_np

        # 2. Define the code to be executed by run_regularly.
        # This code will be executed for *all* neurons in target_ng,
        # so we need the 'if i in ...' condition.
        # It's important that target_current_var is initialized (e.g., to 0*amp)
        # for neurons not receiving this stimulus from other sources.
        # If multiple stimuli target the same variable, consider summing them:
        # code = f"if i in {indices_name_in_ns}: {target_current_var} += {ta_name_in_ns}(t)"
        # but this requires I_stimulus to be reset to 0 at each step by another mechanism or equation.
        # For direct assignment by this stimulus:
        code = f"""
if i in {indices_name_in_ns}:
    {target_current_var} = {ta_name_in_ns}(t)
"""
        # If you want to ensure non-targeted neurons by this specific stimulus get 0 for this var:
        # code = f"""
        # {target_current_var} = {ta_name_in_ns}(t) if i in {indices_name_in_ns} else 0*amp
        # """
        # This 'else 0*amp' is only safe if target_current_var is *only* for this stimulus source.
        # If it's a sum, then the first version (only the if) is better.
        # Let's assume target_current_var should be set by the TimedArray for targets,
        # and potentially reset to 0 for non-targets *by this specific stimulus operation*.
        # If target_current_var is I_stimulus and it's part of I_summed,
        # other neurons should have I_stimulus = 0*amp unless also targeted.
        # So, the version with 'else 0*amp' can be safer IF this is the only source for I_stimulus
        # or if I_stimulus is meant to be reset.
        # A cleaner way is often to have the model itself ensure I_stimulus is 0 unless set.
        # For now, let's use the conditional assignment.

        op_name = f'stim_op_electrode_{electrode_id}_{target_group_name}'
        
        # Create the run_regularly operation.
        # This operation itself needs to be added to the network.
        # dt=None means it runs every simulation time step.
        # 'when' specifies scheduling slot. 'before_neurongroups' or 'start' is good for inputs.
        stim_operation = target_ng.run_regularly(code, dt=self.brian_dt, when='start', name=op_name)
        
        print(f"Stimulus operation '{op_name}' created for electrode {electrode_id}, "
              f"targeting '{target_current_var}' of {len(target_neuron_indices_np)} neurons in '{target_group_name}'.")
        
        self._network_objects.append(stim_operation) # Add the operation to network objects
        self._stimulus_current_sources.append(stimulus_waveform) # Keep track of the TA
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
        # _network_objects now contains NeuronGroups, Synapses, Monitors, and run_regularly operations
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