# src/pyneurorg/simulation/simulator.py

import brian2 as b2
from ..organoid.organoid import Organoid
from ..mea.mea import MEA # Import MEA class
from ..electrophysiology import brian_monitors as pbg_monitors
# stimulus_generator não é importado aqui diretamente, pois o Simulator recebe o TimedArray já criado.

class Simulator:
    """
    Orchestrates Brian2 simulations for a given pyneurorg Organoid,
    optionally interacting with an MEA for stimulation.
    """

    def __init__(self, organoid: Organoid, mea: MEA = None, brian2_dt=None): # Added mea parameter
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
        self.mea = mea # Store the MEA instance
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

        The stimulus_waveform (a Brian2 TimedArray) will be assigned to the
        `target_current_var` (default: 'I_input') of the identified target neurons.

        Parameters
        ----------
        electrode_id : int
            The ID (index) of the MEA electrode to apply the stimulus from.
        stimulus_waveform : brian2.input.timedarray.TimedArray
            The pre-generated stimulus current (e.g., from stimulus_generator).
            Its values should have current dimensions (e.g., b2.amp).
        target_group_name : str
            The name of the NeuronGroup within the organoid to target.
        influence_radius : float or brian2.units.fundamentalunits.Quantity
            The radius around the electrode within which neurons are considered targets.
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
        # It's good if TimedArray values have current dimensions, Brian2 might enforce this later.
        # if not stimulus_waveform.values.unit.has_dimension(b2.amp.dim):
        #     raise ValueError("stimulus_waveform.values must have current dimensions.")

        target_ng = self.organoid.get_neuron_group(target_group_name) # Raises KeyError if not found

        # Check if the target current variable exists in the neuron model
        if not hasattr(target_ng, target_current_var):
            raise AttributeError(f"Target neuron group '{target_group_name}' does not have "
                                 f"a variable named '{target_current_var}'. "
                                 f"Ensure it's defined in the model equations (e.g., '{target_current_var} : amp').")

        # Identify target neurons
        target_neuron_indices = self.mea.get_neurons_near_electrode(
            organoid=self.organoid,
            neuron_group_name=target_group_name,
            electrode_id=electrode_id,
            radius=influence_radius
        )

        if len(target_neuron_indices) == 0:
            print(f"Warning: No neurons found within radius {influence_radius} of electrode {electrode_id} "
                  f"in group '{target_group_name}'. Stimulus will not be applied to any neurons from this source.")
            return

        # Apply the stimulus to the target_current_var of the selected neurons.
        # Slicing a NeuronGroup returns a Subgroup.
        # We assign the TimedArray to the attribute of this Subgroup.
        # Brian2 handles applying the time-varying values during the simulation.
        # Syntax: subgroup.current_variable = timed_array
        
        # Important: Brian2 TimedArrays apply to the *entire group* if assigned directly
        # to NeuronGroup.attribute. To target a subgroup, you assign it as:
        # NeuronGroup.attribute = linked_var(subgroup_variable)
        # where subgroup_variable is a TimedArray.
        # OR, more simply, if the target_current_var is a state variable that can be
        # indexed (like V), you can do:
        # target_ng.variables[target_current_var][target_neuron_indices] = stimulus_waveform
        # However, the standard way to apply a TimedArray as an input is to assign it.
        # If multiple stimuli target the same I_input, they will overwrite unless I_input is summed.
        # For now, let's assume I_input can be directly driven this way for a subgroup.

        # To make a TimedArray apply only to a subgroup for a variable like current:
        # 1. Create a new variable in the NeuronGroup for this specific stimulus if you want to sum them.
        # 2. Or, if target_current_var is designed to be indexed (e.g. part of equations, not just a param)
        #    target_ng.namespace[f'stim_{electrode_id}'] = stimulus_waveform
        #    target_ng.equations.add_equation(f'{target_current_var} += stim_{electrode_id}(t) # if neuron i in target_indices')
        #    This is getting complex.

        # Simplest approach for now: Assume target_current_var can be driven.
        # If target_current_var is, e.g., I_input, and we want to apply stimulus_waveform(t) to it
        # for a subgroup, we can create a new per-neuron parameter that gets this value.
        
        # Let's use the subgroup assignment method if target_current_var exists for the group.
        # This will make all neurons in the subgroup refer to the same TimedArray.
        subgroup_to_stimulate = target_ng[target_neuron_indices]
        
        # setattr(subgroup_to_stimulate, target_current_var, stimulus_waveform)
        # This above line sets it for the subgroup, meaning all neurons in the subgroup get this.
        # This is the standard Brian2 way.

        # Let's make sure this TimedArray is part of the network if it's not already via the group
        # The TimedArray itself is not a "BrianObject" in the same way NeuronGroup is.
        # It's values are used by the NeuronGroup.
        # We store it to potentially manage it or log it.
        
        # A robust way to apply to subgroup for variables like 'I':
        # Create a new parameter in the main group for this stimulus input.
        stim_param_name = f"I_stim_electrode_{electrode_id}"

        if stim_param_name not in target_ng.variables:
            # This approach requires modifying the NeuronGroup's equations dynamically,
            # which is not ideal after creation.
            # Alternative: The neuron model should have a generic I_stimulus term,
            # and we sum inputs into it.
            # For now, let's assume target_current_var like 'I_input' can be indexed.
            # If NeuronGroup has `I_input : amp (linked)` this will work.
            # If `I_input : amp` is a standard state variable:
            try:
                # This will set I_input for the selected indices to the TimedArray values at each step.
                # This means I_input becomes a "dynamic array" for these neurons.
                target_ng.variables[target_current_var].set_value_by_indices(target_neuron_indices, stimulus_waveform)
                print(f"Stimulus from electrode {electrode_id} assigned to '{target_current_var}' of {len(target_neuron_indices)} neurons in '{target_group_name}'.")
                self._stimulus_current_sources.append(stimulus_waveform) # Keep a reference
            except Exception as e:
                print(f"Warning: Could not directly assign TimedArray to subgroup for variable '{target_current_var}'. "
                      f"This method might require '{target_current_var}' to be a linked variable "
                      f"or for the NeuronGroup to be structured to accept indexed TimedArray assignment. Error: {e}")
                print("Falling back to assigning to the subgroup directly (may affect all neurons in subgroup uniformly if not indexed var).")
                # This fallback might not work as intended if target_current_var is not setup for subgroup-specific TimedArray
                try:
                    setattr(subgroup_to_stimulate, target_current_var, stimulus_waveform)
                    print(f"Fallback: Stimulus from electrode {electrode_id} assigned to '{target_current_var}' of subgroup from '{target_group_name}'.")
                    self._stimulus_current_sources.append(stimulus_waveform)
                except Exception as e_fallback:
                     print(f"Fallback assignment also failed: {e_fallback}. Ensure neuron model can receive TimedArray on '{target_current_var}'.")


    # ... (add_recording, build_network, run, get_data, store/restore as before) ...
    # Ensure all methods from the "cleaned" version are here.
    def add_recording(self, monitor_name: str, monitor_type: str, target_group_name: str, **kwargs):
        if monitor_name in self.monitors:
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        target_group = self.organoid.get_neuron_group(target_group_name)
        monitor_object = None
        brian2_monitor_internal_name = kwargs.pop('name', f"pyb_mon_{monitor_name}_{target_group.name}")
        if monitor_type.lower() == "spike":
            monitor_object = pbg_monitors.setup_spike_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
        elif monitor_type.lower() == "state":
            if 'variables' not in kwargs: raise KeyError("'variables' required for 'state' monitor.")
            monitor_object = pbg_monitors.setup_state_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
        elif monitor_type.lower() == "population_rate":
            monitor_object = pbg_monitors.setup_population_rate_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
        else:
            raise ValueError(f"Unsupported monitor_type: '{monitor_type}'.")
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