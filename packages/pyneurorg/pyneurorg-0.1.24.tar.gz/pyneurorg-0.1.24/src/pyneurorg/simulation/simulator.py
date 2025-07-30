        # --- MODIFIED SECTION: Applying TimedArray to a subgroup ---
        # To apply a TimedArray to a specific subset of neurons for a state variable
        # like 'I_input', we directly assign the TimedArray to the indexed/sliced
        # view of that variable for the target neurons.
        # Brian2 interprets this as: for these specific neurons, the value of
        # 'target_current_var' will be determined by 'stimulus_waveform(t)' at each time step.
        try:
            # Get the VariableView for the target current variable
            variable_to_set = getattr(target_ng, target_current_var)
            # Assign the TimedArray to the slice of neurons
            variable_to_set[target_neuron_indices] = stimulus_waveform
            
            print(f"Stimulus from electrode {electrode_id} assigned to '{target_current_var}' of {len(target_neuron_indices)} neurons in '{target_group_name}'.")
            self._stimulus_current_sources.append(stimulus_waveform) # Keep a reference
        except Exception as e:
            print(f"Error assigning TimedArray to subgroup for variable '{target_current_var}': {e}")
            print("Ensure that the variable is part of the NeuronGroup's equations and can be indexed "
                  "(e.g., 'I_input : amp' in the model string).")
            raise # Re-raise the exception so it's not silently ignored.
        # --- END OF MODIFIED SECTION ---