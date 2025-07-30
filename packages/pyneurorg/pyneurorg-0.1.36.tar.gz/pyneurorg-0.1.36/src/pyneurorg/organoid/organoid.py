# src/pyneurorg/organoid/organoid.py

import brian2 as b2
import numpy as np
from ..core import neuron_models as pbg_neuron_models
from ..core import synapse_models as pbg_synapse_models # Mantido para completude da classe
from . import spatial as pbg_spatial
from .spatial import _ensure_um_quantity # Importando helper de spatial.py

class Organoid:
    def __init__(self, name="pyneurorg_organoid", default_brian2_prefs=None):
        self.name = name
        self.neuron_groups = {}
        self.synapses = {}
        self.positions = {} 
        self.brian2_objects = []

        if default_brian2_prefs:
            for key, value in default_brian2_prefs.items():
                b2.prefs[key] = value
        
        self._neuron_id_counter = 0 # Not currently used, but for future global IDing

    def add_neurons(self, name, num_neurons, model_name, model_params=None,
                    positions=None, spatial_distribution_func=None, spatial_params=None,
                    initial_values=None, **kwargs):
        """
        Adds a population of neurons (a NeuronGroup) to the organoid.

        Parameters
        ----------
        name : str
            A unique name for this neuron group.
        num_neurons : int
            The number of neurons in this group.
        model_name : str
            Name of the neuron model function from `pyneurorg.core.neuron_models`.
        model_params : dict, optional
            Parameters for the neuron model function. This can include
            `num_stimulus_flags` to specify how many stimulus flag variables
            should be created in the model.
        positions : brian2.units.fundamentalunits.Quantity or array-like, optional
            A (num_neurons, 3) array of (x,y,z) coordinates.
            If a Brian2 Quantity, must have length dimensions.
            If an array-like of numbers, assumed to be in micrometers (um).
            If provided, `spatial_distribution_func` is ignored.
        spatial_distribution_func : str, optional
            Name of the spatial distribution function from `pyneurorg.organoid.spatial`.
        spatial_params : dict, optional
            Parameters for `spatial_distribution_func`.
        initial_values : dict, optional
            Initial values for neuron state variables (e.g., {'v': -65*b2.mV}).
            These will override any defaults from the model's namespace or pyneurorg.
        **kwargs :
            Additional arguments for `brian2.NeuronGroup`.

        Returns
        -------
        brian2.NeuronGroup
            The created Brian2 NeuronGroup object.
        """
        if name in self.neuron_groups:
            raise ValueError(f"Neuron group with name '{name}' already exists.")
        
        # Ensure model_params is a dict even if None is passed
        current_model_params = model_params.copy() if model_params is not None else {}

        # Get neuron model definition by calling the function from neuron_models
        try:
            model_func = getattr(pbg_neuron_models, model_name)
        except AttributeError:
            raise ValueError(f"Neuron model function '{model_name}' not found in pyneurorg.core.neuron_models.")
        
        # Call the model function with its parameters (which might include num_stimulus_flags)
        model_def = model_func(**current_model_params)

        # --- Position generation/validation (assumes spatial functions return Quantity in um) ---
        neuron_positions_um_qty = None
        if positions is not None:
            # Convert/validate provided positions to ensure they are Quantity in um
            if isinstance(positions, b2.Quantity):
                if positions.dimensions == b2.metre.dimensions:
                    neuron_positions_um_qty = (positions / b2.um) * b2.um # Ensure it's in um
                else:
                    raise TypeError("Provided 'positions' Quantity must have length dimensions.")
            elif isinstance(positions, (np.ndarray, list, tuple)):
                try:
                    positions_arr = np.asarray(positions, dtype=float)
                    if positions_arr.ndim == 1 and positions_arr.shape[0] == 3 and num_neurons == 1: # Single neuron
                        positions_arr = positions_arr.reshape(1,3)
                    elif positions_arr.ndim != 2 or positions_arr.shape[1] != 3:
                        raise ValueError("If 'positions' is array/list, it must be N x 3 or 1x3 for single neuron.")
                    neuron_positions_um_qty = positions_arr * b2.um
                except Exception as e:
                    raise TypeError(f"Could not interpret 'positions' as coordinate array (assumed um): {e}")
            else:
                raise TypeError("Provided 'positions' must be a Brian2 Quantity, or array-like (assumed um).")

            if neuron_positions_um_qty.shape[0] != num_neurons:
                 raise ValueError(f"Provided positions shape ({neuron_positions_um_qty.shape[0]},3) "
                                  f"first dimension does not match num_neurons ({num_neurons}).")
        elif spatial_distribution_func is not None:
            current_spatial_params = spatial_params.copy() if spatial_params is not None else {}
            current_spatial_params['N'] = num_neurons
            try:
                spatial_func = getattr(pbg_spatial, spatial_distribution_func)
            except AttributeError:
                raise ValueError(f"Spatial function '{spatial_distribution_func}' not found.")
            neuron_positions_um_qty = spatial_func(**current_spatial_params) # Expected to return Quantity in um
            if not (isinstance(neuron_positions_um_qty, b2.Quantity) and neuron_positions_um_qty.dimensions == b2.metre.dimensions):
                 raise TypeError(f"Spatial function '{spatial_distribution_func}' must return Quantity with length dimensions.")
            if neuron_positions_um_qty.shape != (num_neurons, 3):
                raise ValueError(f"Spatial function '{spatial_distribution_func}' returned incorrect shape.")
        else:
            raise ValueError("Either 'positions' or 'spatial_distribution_func' must be provided.")
        # --- End of position processing ---

        # --- Prepare initial values for NeuronGroup state variables ---
        # Order of precedence:
        # 1. User-provided `initial_values` dict.
        # 2. `_default_init` values from the model's namespace (e.g., v_default_init, I_stimulus_sum_default_init).
        # 3. Brian2's own defaults (e.g., 0 for numerical, False for boolean if not in namespace).
        
        final_initial_values = {}
        model_namespace_defaults = model_def.get('namespace', {})

        # Start with defaults from the model's namespace (stripping '_default_init')
        for key, val in model_namespace_defaults.items():
            if key.endswith('_default_init'):
                var_name = key[:-len('_default_init')] # Remove suffix
                final_initial_values[var_name] = val
        
        # Add pyneurorg defaults for key current variables if not already set by model's _default_init
        # and if they are present in the model equations.
        # This ensures they are initialized even if the model definition doesn't specify a _default_init for them.
        model_eqs_str = model_def.get('model', '')
        if 'I_stimulus_sum' in model_eqs_str and 'I_stimulus_sum' not in final_initial_values:
            final_initial_values['I_stimulus_sum'] = 0*b2.amp
        if 'I_synaptic' in model_eqs_str and 'I_synaptic' not in final_initial_values:
            final_initial_values['I_synaptic'] = 0*b2.amp
        
        # Boolean flags from the model (e.g., is_targeted_by_stimX) should have their
        # _default_init (False) already in final_initial_values from the model_namespace_defaults.
        # Brian2 will default uninitialized booleans in equations to False anyway.

        # Override with user-provided initial_values
        if initial_values:
            final_initial_values.update(initial_values)
        # --- End of initial value preparation ---

        ng = b2.NeuronGroup(
            N=num_neurons,
            model=model_def['model'],
            threshold=model_def.get('threshold'),
            reset=model_def.get('reset'),
            refractory=model_def.get('refractory', False),
            method=kwargs.pop('method', model_def.get('method', 'auto')),
            namespace=model_namespace_defaults, # Pass the full model namespace
            name=name,
            **kwargs
        )

        # Apply the determined initial values
        for var_name, value in final_initial_values.items():
            if hasattr(ng, var_name): # Check if it's a settable attribute/variable on the NeuronGroup
                try:
                    setattr(ng, var_name, value)
                except Exception as e:
                    print(f"Warning: Could not set initial value for '{var_name}' on NeuronGroup '{name}'. Error: {e}")
            # else:
                # This variable might be in the model string but not directly settable as ng.varname
                # (e.g., if it's only used internally in multi-line equations).
                # Brian2 typically initializes variables defined in equations to 0 (with units if specified) or False.
                # print(f"Note: Variable '{var_name}' from initial_values/defaults not a direct attribute of NeuronGroup '{name}'. "
                #       "It will rely on Brian2's default initialization if it's part of the model equations.")

        self.neuron_groups[name] = ng
        self.positions[name] = neuron_positions_um_qty # Already in um Quantity
        self.brian2_objects.append(ng)
        return ng

    # ... (add_synapses, getters, __str__, __repr__ methods as before) ...
    # Ensure these methods are present from the previous complete Organoid class implementation.
    def add_synapses(self, name, pre_group_name, post_group_name,
                     model_name, model_params=None,
                     connect_condition=None, connect_prob=None, connect_n=None,
                     on_pre_params=None, on_post_params=None,
                     synaptic_params=None, **kwargs):
        if name in self.synapses:
            raise ValueError(f"Synapse group with name '{name}' already exists.")
        if pre_group_name not in self.neuron_groups:
            raise ValueError(f"Presynaptic neuron group '{pre_group_name}' not found.")
        if post_group_name not in self.neuron_groups:
            raise ValueError(f"Postsynaptic neuron group '{post_group_name}' not found.")

        current_model_params = model_params.copy() if model_params is not None else {}
        current_on_pre_params = on_pre_params.copy() if on_pre_params is not None else {}
        current_on_post_params = on_post_params.copy() if on_post_params is not None else {}
        current_synaptic_params = synaptic_params.copy() if synaptic_params is not None else {}


        pre_ng = self.neuron_groups[pre_group_name]
        post_ng = self.neuron_groups[post_group_name]

        try:
            model_func = getattr(pbg_synapse_models, model_name)
        except AttributeError:
            raise ValueError(f"Synapse model function '{model_name}' not found in pyneurorg.core.synapse_models.")

        model_def = model_func(**current_model_params)

        syn = b2.Synapses(
            source=pre_ng,
            target=post_ng,
            model=model_def['model'],
            on_pre=model_def.get('on_pre'),
            on_post=model_def.get('on_post'),
            namespace=model_def.get('namespace', {}),
            method=kwargs.pop('method', model_def.get('method', 'auto')),
            name=name, 
            **kwargs
        )

        if connect_condition is not None: syn.connect(condition=connect_condition)
        elif connect_prob is not None: syn.connect(p=connect_prob)
        elif connect_n is not None: syn.connect(n=connect_n)
        else:
            if len(pre_ng) * len(post_ng) > 0 : 
                 print(f"Warning: No connection rule specified for synapses '{name}'. Defaulting to all-to-all if not too large.")
                 if len(pre_ng) * len(post_ng) < 100000: 
                     syn.connect() 
                 else:
                     print(f"Skipping default all-to-all for '{name}' due to large potential number of synapses.")
        
        for param_name, value in current_synaptic_params.items():
            if hasattr(syn, param_name):
                setattr(syn, param_name, value)
            else:
                print(f"Warning: Synaptic parameter '{param_name}' not found in model for synapses '{name}'.")
        
        for param_name, value in current_on_pre_params.items():
             if param_name == 'delay': 
                 syn.delay = value
        
        self.synapses[name] = syn
        self.brian2_objects.append(syn)
        return syn

    def get_neuron_group(self, name):
        if name not in self.neuron_groups:
            raise KeyError(f"Neuron group '{name}' not found.")
        return self.neuron_groups[name]

    def get_synapses(self, name):
        if name not in self.synapses:
            raise KeyError(f"Synapses group '{name}' not found.")
        return self.synapses[name]

    def get_positions(self, neuron_group_name):
        if neuron_group_name not in self.positions:
            raise KeyError(f"Positions for neuron group '{neuron_group_name}' not found.")
        return self.positions[neuron_group_name]

    def __str__(self):
        return (f"<Organoid '{self.name}' with {len(self.neuron_groups)} neuron group(s) "
                f"and {len(self.synapses)} synapse group(s)>")

    def __repr__(self):
        return self.__str__()