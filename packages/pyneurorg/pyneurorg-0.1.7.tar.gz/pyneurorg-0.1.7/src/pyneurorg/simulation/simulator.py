# pyneurorg/simulation/simulator.py

"""
Defines the Simulator class for orchestrating pyneurorg simulations.

The Simulator class takes an Organoid instance, allows adding monitors,
constructs a Brian2 Network, and runs the simulation.
"""

import brian2 as b2
# Importar módulos pyneurorg
from ..organoid.organoid import Organoid # Para type hinting
from ..electrophysiology import brian_monitors as pbg_monitors

class Simulator:
    """
    Orchestrates Brian2 simulations for a given pyneurorg Organoid.

    This class manages the collection of Brian2 objects from an Organoid,
    allows for the addition of monitors, builds a Brian2 Network,
    runs simulations, and provides access to recorded data.

    Parameters
    ----------
    organoid : pyneurorg.organoid.organoid.Organoid
        The pyneurorg Organoid instance to be simulated.
    brian2_dt : brian2.units.fundamentalunits.Quantity, optional
        The default clock dt for the simulation. If None, Brian2's default
        (0.1*ms) will be used or inherited. (default: None).

    Attributes
    ----------
    organoid : pyneurorg.organoid.organoid.Organoid
        The associated Organoid object.
    brian_network : brian2.Network or None
        The constructed Brian2 Network object. Initially None.
    monitors : dict
        A dictionary to store added monitor objects, keyed by their user-defined names.
    brian_dt : brian2.units.fundamentalunits.Quantity
        The simulation time step.
    """

    def __init__(self, organoid: Organoid, brian2_dt=None):
        """
        Initializes a new Simulator instance.
        """
        if not isinstance(organoid, Organoid):
            raise TypeError("organoid must be an instance of pyneurorg.organoid.Organoid.")

        self.organoid = organoid
        self.brian_network = None
        self.monitors = {} # User-defined name -> monitor object
        
        if brian2_dt is not None:
            if not (hasattr(brian2_dt, 'unit') and brian2_dt.unit.has_dimension(b2.second.dim)):
                raise TypeError("brian2_dt must be a Brian2 Quantity with time units.")
            self.brian_dt = brian2_dt
            b2.defaultclock.dt = self.brian_dt
        else:
            self.brian_dt = b2.defaultclock.dt # Use Brian2's default or previously set dt

        self._network_objects = list(self.organoid.brian2_objects) # Start with objects from organoid

    def add_recording(self, monitor_name: str, monitor_type: str, target_group_name: str, **kwargs):
        """
        Adds a Brian2 monitor to record activity from a specified neuron group.

        Parameters
        ----------
        monitor_name : str
            A unique name to identify this monitor (e.g., "exc_spikes", "inh_vm").
        monitor_type : str
            The type of monitor to add. Supported types: "spike", "state", "population_rate".
        target_group_name : str
            The name of the NeuronGroup within the organoid to monitor.
        **kwargs :
            Additional keyword arguments to pass to the specific monitor setup function
            from `pyneurorg.electrophysiology.brian_monitors`.
            For "state" monitor, `variables` (str or list) is required.
            For "spike" or "state", `record` (bool or list/slice) can be provided.

        Returns
        -------
        brian2.monitors.Monitor
            The created Brian2 monitor object.

        Raises
        ------
        ValueError
            If `monitor_name` already exists, `target_group_name` is not found,
            or `monitor_type` is unsupported.
        KeyError
            If required arguments for a monitor type (like `variables` for 'state') are missing.
        """
        if monitor_name in self.monitors:
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        
        target_group = self.organoid.get_neuron_group(target_group_name) # Raises KeyError if not found

        monitor = None
        # Ensure the monitor has a unique Brian2 name if user doesn't provide one in kwargs
        brian2_monitor_name = kwargs.pop('name', f"{monitor_name}_{target_group.name}")


        if monitor_type.lower() == "spike":
            monitor = pbg_monitors.setup_spike_monitor(target_group, name=brian2_monitor_name, **kwargs)
        elif monitor_type.lower() == "state":
            if 'variables' not in kwargs:
                raise KeyError("Argument 'variables' (str or list of str) is required for 'state' monitor.")
            monitor = pbg_monitors.setup_state_monitor(target_group, name=brian2_monitor_name, **kwargs)
        elif monitor_type.lower() == "population_rate":
            monitor = pbg_monitors.setup_population_rate_monitor(target_group, name=brian2_monitor_name, **kwargs)
        else:
            raise ValueError(f"Unsupported monitor_type: '{monitor_type}'. "
                             "Supported types are 'spike', 'state', 'population_rate'.")

        if monitor:
            self.monitors[monitor_name] = monitor
            if monitor not in self._network_objects: # Avoid duplicates if monitor was somehow already there
                self._network_objects.append(monitor)
        return monitor

    def build_network(self, **network_kwargs):
        """
        Constructs the Brian2 Network object from all components.

        This method should typically be called internally by `run()` if the
        network hasn't been built yet, but can be called explicitly.

        Parameters
        ----------
        **network_kwargs :
            Additional keyword arguments to pass to the `brian2.Network`
            constructor.
        """
        # self._network_objects should already contain all NeuronGroups, Synapses from organoid,
        # and any added monitors.
        self.brian_network = b2.Network(self._network_objects, **network_kwargs)
        # print(f"Network built with objects: {[obj.name for obj in self.brian_network.objects if hasattr(obj, 'name')]}")


    def run(self, duration: b2.units.fundamentalunits.Quantity, report=None, report_period=10*b2.second, **run_kwargs):
        """
        Runs the simulation for the specified duration.

        If the Brian2 Network has not been built yet, it will be built first.

        Parameters
        ----------
        duration : brian2.units.fundamentalunits.Quantity
            The duration for which to run the simulation (e.g., 100*b2.ms).
        report : str or None, optional
            How to report simulation progress (e.g., 'text', 'stdout', or a function).
            (default: None).
        report_period : brian2.units.fundamentalunits.Quantity, optional
            How often to report progress if `report` is specified (default: 10*second).
        **run_kwargs :
            Additional keyword arguments to pass to the `brian_network.run()`
            method (e.g., `level` for managing object hierarchy in multiple runs).
        """
        if not (hasattr(duration, 'unit') and duration.unit.has_dimension(b2.second.dim)):
            raise TypeError("duration must be a Brian2 Quantity with time units.")

        if self.brian_network is None:
            self.build_network()

        if self.brian_network is None: # Should not happen if build_network worked
            raise RuntimeError("Brian2 Network could not be built or is still None.")

        self.brian_network.run(duration, report=report, report_period=report_period, **run_kwargs)

    def get_data(self, monitor_name: str):
        """
        Retrieves the data recorded by a specified monitor.

        Parameters
        ----------
        monitor_name : str
            The user-defined name of the monitor whose data is to be retrieved.

        Returns
        -------
        object
            The data object from the monitor. The type of this object depends
            on the monitor type (e.g., for SpikeMonitor, it contains .i, .t;
            for StateMonitor, it contains recorded variables as attributes).

        Raises
        ------
        KeyError
            If `monitor_name` is not found in the registered monitors.
        """
        if monitor_name not in self.monitors:
            raise KeyError(f"Monitor with name '{monitor_name}' not found. "
                           f"Available monitors: {list(self.monitors.keys())}")
        return self.monitors[monitor_name]

    def store_simulation(self, filename="pyneurorg_sim_state"):
        """
        Stores the current state of the simulation network.

        Parameters
        ----------
        filename : str, optional
            The filename (without extension) to store the state.
            (default: "pyneurorg_sim_state").
        """
        if self.brian_network is None:
            print("Warning: Network not built yet. Nothing to store.")
            return
        self.brian_network.store(name=filename) # Brian2 will append .bri
        print(f"Simulation state stored in '{filename}.bri'")


    def restore_simulation(self, filename="pyneurorg_sim_state"):
        """
        Restores the state of the simulation network from a file.

        Note: The network structure (NeuronGroups, Synapses, Monitors)
        must be identical to the one that was stored. This typically means
        re-creating the Simulator and Organoid with the same parameters
        before calling restore.

        Parameters
        ----------
        filename : str, optional
            The filename (without extension) to restore the state from.
            (default: "pyneurorg_sim_state").
        """
        if self.brian_network is None:
            # It's possible to restore even if network isn't explicitly built here,
            # if all objects are already in self._network_objects.
            # However, Brian2's store/restore typically works on a Network instance.
            # For safety, let's assume the network should be conceptually defined.
            # The actual `Network` object is created by brian2.restore.
            print("Warning: Network not explicitly built. Ensure all objects are defined before restoring.")

        # Brian2's restore function re-creates the Network object
        # We need to capture it.
        # It also restores the defaultclock.
        b2.restore(name=filename) # Restores into the global Brian namespace / current device
        
        # After restoring, the objects in self._network_objects are now the restored ones if they had names.
        # It's tricky to re-assign self.brian_network perfectly without knowing how brian2.restore
        # handles the existing object references.
        # A common pattern is to call restore *before* creating the Network object
        # if you're starting a script from scratch.
        # If restoring an *existing* Simulator instance, it's more complex.
        # For now, let's assume this method is called in a context where the objects
        # are correctly picked up by the restored state.
        # A more robust way would be if Brian2 allowed restoring *into* an existing Network instance,
        # or if we re-fetch objects by name after restore.
        print(f"Simulation state restored from '{filename}.bri'. You might need to rebuild the Network object if it was already built.")
        # To be safe, nullify the old network so it gets rebuilt with restored objects on next run.
        self.brian_network = None
        # Also, update the defaultclock.dt to the restored value
        self.brian_dt = b2.defaultclock.dt


    def __str__(self):
        status = "Built" if self.brian_network else "Not Built"
        return (f"<Simulator for Organoid '{self.organoid.name}' "
                f"with {len(self.monitors)} monitor(s). Network Status: {status}>")

    def __repr__(self):
        return self.__str__()
