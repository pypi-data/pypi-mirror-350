# pyneurorg/organoid/organoid.py

"""
Defines the main Organoid class for pyneurorg simulations.

The Organoid class acts as a container and manager for Brian2 NeuronGroup
and Synapses objects, along with their spatial properties.
"""

import brian2 as b2
import numpy as np
# Importar modelos e funções espaciais dos outros módulos do pyneurorg
from ..core import neuron_models as pbg_neuron_models # Usando alias para evitar conflito de nomes
from ..core import synapse_models as pbg_synapse_models
from . import spatial as pbg_spatial


class Organoid:
    """
    Represents a brain organoid structure with neuronal populations and synapses.

    Manages the underlying Brian2 NeuronGroup and Synapses objects,
    along with their spatial arrangement and connectivity.

    Parameters
    ----------
    name : str, optional
        A descriptive name for the organoid instance (default: "pyneurorg_organoid").
    default_brian2_prefs : dict, optional
        A dictionary of Brian2 preferences to apply at the start of simulations
        involving this organoid. E.g., {'core.default_float_dtype': float64}.
        If None, no specific preferences are set by this class.

    Attributes
    ----------
    name : str
        Name of the organoid.
    neuron_groups : dict
        Dictionary storing `brian2.NeuronGroup` objects, keyed by their names.
    synapses : dict
        Dictionary storing `brian2.Synapses` objects, keyed by their names.
    positions : dict
        Dictionary storing NumPy arrays of neuron positions (N, 3) for each
        neuron group, keyed by neuron group names. Unit is um by default.
    brian2_objects : list
        A list containing all Brian2 objects (NeuronGroup, Synapses, Monitors etc.)
        that belong to this organoid. This list can be directly passed to
        a `brian2.Network` object.
    """

    def __init__(self, name="pyneurorg_organoid", default_brian2_prefs=None):
        """
        Initializes a new Organoid instance.
        """
        self.name = name
        self.neuron_groups = {}
        self.synapses = {}
        self.positions = {} # Stores positions as np.ndarray (value) with um as implicit unit
                            # or brian2.Quantity directly. Let's store Brian2 Quantity for consistency.
        self.brian2_objects = []

        if default_brian2_prefs:
            for key, value in default_brian2_prefs.items():
                b2.prefs[key] = value
        
        self._neuron_id_counter = 0 # For assigning unique global IDs if needed later

    def add_neurons(self, name, num_neurons, model_name, model_params=None,
                    positions=None, spatial_distribution_func=None, spatial_params=None,
                    initial_values=None, **kwargs):
        """
        Adds a population of neurons (a NeuronGroup) to the organoid.

        Parameters
        ----------
        name : str
            A unique name for this neuron group (e.g., "excitatory_layer1").
        num_neurons : int
            The number of neurons in this group.
        model_name : str
            The name of the neuron model function to use from `pyneurorg.core.neuron_models`
            (e.g., "LIFNeuron", "IzhikevichNeuron").
        model_params : dict, optional
            A dictionary of parameters to pass to the neuron model function.
            If None, default parameters of the model will be used.
        positions : brian2.units.fundamentalunits.Quantity, optional
            A (num_neurons, 3) Quantity array of pre-defined (x,y,z) coordinates.
            If provided, `spatial_distribution_func` and `spatial_params` are ignored.
            Must have length units (e.g., b2.um).
        spatial_distribution_func : str, optional
            The name of the spatial distribution function to use from
            `pyneurorg.organoid.spatial` (e.g., "random_positions_in_cube").
            Ignored if `positions` is provided.
        spatial_params : dict, optional
            A dictionary of parameters to pass to the `spatial_distribution_func`.
            Required if `spatial_distribution_func` is specified.
            Must include 'N': num_neurons.
        initial_values : dict, optional
            A dictionary to set initial values for state variables of the neurons,
            e.g., {'v': -65*b2.mV, 'u': 0*b2.pA}. Keys should match variable names
            in the neuron model. Values can be single quantities (same for all)
            or arrays/Quantities of length `num_neurons`.
        **kwargs :
            Additional keyword arguments to pass to the `brian2.NeuronGroup`
            constructor (e.g., `method`).

        Returns
        -------
        brian2.NeuronGroup
            The created Brian2 NeuronGroup object.

        Raises
        ------
        ValueError
            If a neuron group with the given name already exists, or if
            model/spatial function is not found, or if parameters are invalid.
        TypeError
            If positions are not Brian2 Quantities with length units.
        """
        if name in self.neuron_groups:
            raise ValueError(f"Neuron group with name '{name}' already exists.")
        if model_params is None:
            model_params = {}

        # Get neuron model definition
        try:
            model_func = getattr(pbg_neuron_models, model_name)
        except AttributeError:
            raise ValueError(f"Neuron model function '{model_name}' not found in pyneurorg.core.neuron_models.")
        
        model_def = model_func(**model_params)

        # Generate or validate positions
        if positions is not None:
            if not (hasattr(positions, 'unit') and positions.unit.has_dimension(b2.meter.dim)):
                raise TypeError("Provided positions must be a Brian2 Quantity with length units.")
            if positions.shape != (num_neurons, 3):
                raise ValueError(f"Provided positions shape {positions.shape} does not match ({num_neurons}, 3).")
            neuron_positions = positions
        elif spatial_distribution_func is not None:
            if spatial_params is None:
                spatial_params = {}
            if 'N' not in spatial_params: # Ensure N is passed
                spatial_params['N'] = num_neurons
            elif spatial_params['N'] != num_neurons:
                raise ValueError("N in spatial_params must match num_neurons.")

            try:
                spatial_func = getattr(pbg_spatial, spatial_distribution_func)
            except AttributeError:
                raise ValueError(f"Spatial distribution function '{spatial_distribution_func}' not found in pyneurorg.organoid.spatial.")
            neuron_positions = spatial_func(**spatial_params)
        else:
            # Default: place at origin if no spatial info given (or raise error)
            # Forcing spatial info might be better for an "organoid"
            raise ValueError("Either 'positions' or 'spatial_distribution_func' must be provided.")

        # Create NeuronGroup
        # The namespace from model_def contains default parameters
        # The model_def['model'] contains the equations string
        # The model_def also contains threshold, reset, refractory, method
        
        # Handle initial values from model_def namespace (e.g. v_default_init)
        # and override with user-provided initial_values
        current_initial_values = {}
        if 'namespace' in model_def:
            for key, val in model_def['namespace'].items():
                if key.endswith('_default_init'):
                    var_name = key.replace('_default_init', '')
                    current_initial_values[var_name] = val
        
        if initial_values:
            current_initial_values.update(initial_values)


        ng = b2.NeuronGroup(
            N=num_neurons,
            model=model_def['model'],
            threshold=model_def.get('threshold'),
            reset=model_def.get('reset'),
            refractory=model_def.get('refractory', False), # False if not specified
            method=kwargs.pop('method', model_def.get('method', 'auto')),
            namespace=model_def.get('namespace', {}),
            name=name, # Brian2 internal name
            **kwargs
        )

        # Set initial values
        for var_name, value in current_initial_values.items():
            if hasattr(ng, var_name):
                setattr(ng, var_name, value)
            else:
                print(f"Warning: Initial value for '{var_name}' provided, but not found in model equations for group '{name}'.")


        self.neuron_groups[name] = ng
        self.positions[name] = neuron_positions
        self.brian2_objects.append(ng)
        return ng

    def add_synapses(self, name, pre_group_name, post_group_name,
                     model_name, model_params=None,
                     connect_condition=None, connect_prob=None, connect_n=None,
                     on_pre_params=None, on_post_params=None,
                     synaptic_params=None, **kwargs):
        """
        Adds a set of synapses (a Synapses object) connecting two neuron groups.

        Parameters
        ----------
        name : str
            A unique name for this synapse group.
        pre_group_name : str
            Name of the presynaptic neuron group.
        post_group_name : str
            Name of the postsynaptic neuron group.
        model_name : str
            Name of the synapse model function from `pyneurorg.core.synapse_models`.
        model_params : dict, optional
            Parameters to pass to the synapse model function.
        connect_condition : str, optional
            A Brian2 string condition for creating synapses (e.g., 'i != j').
            Evaluated for each pair of (pre_idx, post_idx).
        connect_prob : float, optional
            Probability (0 to 1) of connecting any pair of pre/post neurons.
            If specified, `connect_condition` might be combined or this takes precedence.
        connect_n : int, optional
            Connect exactly `n` synapses, chosen randomly from all possible pairs
            (respecting `connect_condition` if also provided).
        on_pre_params : dict, optional
            Parameters to set for the `on_pre` pathway, e.g., initial weights.
            Example: {'w_inc': 0.5*b2.nS, 'delay': 2*b2.ms}.
            These are per-synapse values.
        on_post_params : dict, optional
            Parameters for the `on_post` pathway (less common for simple synapses).
        synaptic_params : dict, optional
            A dictionary to set values for synaptic state variables after connection.
            E.g., {'w_syn': 0.1*b2.nS} or {'w_syn': 'rand()*0.1*nS'}.
            These are applied to the created S.w_syn, S.w_inc etc.
        **kwargs :
            Additional keyword arguments for the `brian2.Synapses` constructor.

        Returns
        -------
        brian2.Synapses
            The created Brian2 Synapses object.

        Raises
        ------
        ValueError
            If synapse group name exists, neuron groups not found, or model not found.
        """
        if name in self.synapses:
            raise ValueError(f"Synapse group with name '{name}' already exists.")
        if pre_group_name not in self.neuron_groups:
            raise ValueError(f"Presynaptic neuron group '{pre_group_name}' not found.")
        if post_group_name not in self.neuron_groups:
            raise ValueError(f"Postsynaptic neuron group '{post_group_name}' not found.")

        if model_params is None:
            model_params = {}
        if on_pre_params is None:
            on_pre_params = {} # e.g. for initial weights or delays
        if on_post_params is None:
            on_post_params = {}
        if synaptic_params is None:
            synaptic_params = {}


        pre_ng = self.neuron_groups[pre_group_name]
        post_ng = self.neuron_groups[post_group_name]

        try:
            model_func = getattr(pbg_synapse_models, model_name)
        except AttributeError:
            raise ValueError(f"Synapse model function '{model_name}' not found in pyneurorg.core.synapse_models.")

        model_def = model_func(**model_params)

        syn = b2.Synapses(
            source=pre_ng,
            target=post_ng,
            model=model_def['model'],
            on_pre=model_def.get('on_pre'),
            on_post=model_def.get('on_post'),
            namespace=model_def.get('namespace', {}),
            method=kwargs.pop('method', model_def.get('method', 'auto')),
            name=name, # Brian2 internal name
            **kwargs
        )

        # Connection logic
        if connect_condition is not None:
            syn.connect(condition=connect_condition)
        elif connect_prob is not None:
            syn.connect(p=connect_prob)
        elif connect_n is not None:
            syn.connect(n=connect_n)
        else:
            # Default to all-to-all if no connection rule specified
            # Consider if this is the best default or if an error should be raised.
            # For now, let's make it explicit that a rule is needed for non-trivial cases.
            if len(pre_ng) * len(post_ng) > 0 : # only connect if groups are not empty
                 print(f"Warning: No connection rule specified for synapses '{name}'. Defaulting to all-to-all if not too large, or consider specifying a rule.")
                 if len(pre_ng) * len(post_ng) < 100000: # Avoid huge all-to-all by default
                     syn.connect() # All-to-all
                 else:
                     print(f"Skipping default all-to-all for '{name}' due to large potential number of synapses. Please specify a connection rule.")
            # else: no connections if one group is empty


        # Set initial values for synaptic parameters (e.g., weights, delays)
        # These are for parameters defined in the synapse model string, like 'w_syn' or 'w_inc'
        for param_name, value in synaptic_params.items():
            if hasattr(syn, param_name):
                setattr(syn, param_name, value)
            else:
                print(f"Warning: Synaptic parameter '{param_name}' not found in model for synapses '{name}'.")

        # Set parameters for on_pre pathway (e.g., initial values for variables used in on_pre string)
        # This is more for things like delay which is a special parameter for on_pre
        for param_name, value in on_pre_params.items():
             if param_name == 'delay': # Special handling for delay
                 syn.delay = value
             # For other on_pre specific parameters, if they were variables (not common)
             # elif hasattr(syn, param_name):
             #    setattr(syn, param_name, value)

        self.synapses[name] = syn
        self.brian2_objects.append(syn)
        return syn

    def get_neuron_group(self, name):
        """Retrieves a NeuronGroup by its name."""
        if name not in self.neuron_groups:
            raise KeyError(f"Neuron group '{name}' not found.")
        return self.neuron_groups[name]

    def get_synapses(self, name):
        """Retrieves a Synapses object by its name."""
        if name not in self.synapses:
            raise KeyError(f"Synapses group '{name}' not found.")
        return self.synapses[name]

    def get_positions(self, neuron_group_name):
        """Retrieves the positions of neurons in a named group."""
        if neuron_group_name not in self.positions:
            raise KeyError(f"Positions for neuron group '{neuron_group_name}' not found.")
        return self.positions[neuron_group_name]

    def __str__(self):
        return (f"<Organoid '{self.name}' with {len(self.neuron_groups)} neuron group(s) "
                f"and {len(self.synapses)} synapse group(s)>")

    def __repr__(self):
        return self.__str__()
