# pybrainorg/simulation/simulator.py

"""
Defines the Simulator class for orchestrating pybrainorg simulations.

The Simulator class takes an Organoid instance, allows adding monitors,
constructs a Brian2 Network, and runs the simulation.
"""

import brian2 as b2
# Importar módulos pybrainorg
from ..organoid.organoid import Organoid # Para type hinting
from ..electrophysiology import brian_monitors as pbg_monitors

class Simulator:
    """
    Orchestrates Brian2 simulations for a given pybrainorg Organoid.

    This class manages the collection of Brian2 objects from an Organoid,
    allows for the addition of monitors, builds a Brian2 Network,
    runs simulations, and provides access to recorded data.

    Parameters
    ----------
    organoid : pybrainorg.organoid.organoid.Organoid
        The pybrainorg Organoid instance to be simulated.
    brian2_dt : brian2.units.fundamentalunits.Quantity, optional
        The default clock dt for the simulation. If None, Brian2's default
        (currently 0.1*ms) will be used or inherited. (default: None).

    Attributes
    ----------
    organoid : pybrainorg.organoid.organoid.Organoid
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
            raise TypeError("organoid must be an instance of pybrainorg.organoid.Organoid.")

        self.organoid = organoid
        self.brian_network = None
        self.monitors = {} # User-defined name -> monitor object
        
        # --- CORREÇÃO DA VALIDAÇÃO DE brian2_dt ---
        if brian2_dt is not None:
            if not isinstance(brian2_dt, b2.Quantity) or not (brian2_dt.dimensions == b2.second.dimensions):
                raise TypeError("brian2_dt must be a Brian2 Quantity with time units.")
            self.brian_dt = brian2_dt
            b2.defaultclock.dt = self.brian_dt # Set the default clock for this simulation context
        else:
            self.brian_dt = b2.defaultclock.dt # Use Brian2's current default dt
        # --- FIM DA CORREÇÃO ---

        self._network_objects = list(self.organoid.brian2_objects) # Start with objects from organoid

    def add_recording(self, monitor_name: str, monitor_type: str, target_group_name: str, **kwargs):
        """
        Adds a Brian2 monitor to record activity from a specified neuron group.
        (Implementation details as before)
        """
        if monitor_name in self.monitors:
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        
        target_group = self.organoid.get_neuron_group(target_group_name)

        monitor = None
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
            raise ValueError(f"Unsupported monitor_type: '{monitor_type}'. ")

        if monitor:
            self.monitors[monitor_name] = monitor
            if monitor not in self._network_objects:
                self._network_objects.append(monitor)
        return monitor

    def build_network(self, **network_kwargs):
        """
        Constructs the Brian2 Network object from all components.
        (Implementation details as before)
        """
        self.brian_network = b2.Network(self._network_objects, **network_kwargs)

    def run(self, duration: b2.units.fundamentalunits.Quantity, report=None, report_period=10*b2.second, **run_kwargs):
        """
        Runs the simulation for the specified duration.
        (Implementation details as before - needs unit check for duration)
        """
        # --- CORREÇÃO DA VALIDAÇÃO DE duration ---
        if not isinstance(duration, b2.Quantity) or not (duration.dimensions == b2.second.dimensions):
            raise TypeError("duration must be a Brian2 Quantity with time units.")
        # --- FIM DA CORREÇÃO ---

        if self.brian_network is None:
            self.build_network()

        if self.brian_network is None:
            raise RuntimeError("Brian2 Network could not be built or is still None.")

        self.brian_network.run(duration, report=report, report_period=report_period, **run_kwargs)

    def get_data(self, monitor_name: str):
        """
        Retrieves the data recorded by a specified monitor.
        (Implementation details as before)
        """
        if monitor_name not in self.monitors:
            raise KeyError(f"Monitor with name '{monitor_name}' not found. ")
        return self.monitors[monitor_name]

    def store_simulation(self, filename="pybrainorg_sim_state"):
        """
        Stores the current state of the simulation network.
        (Implementation details as before)
        """
        if self.brian_network is None:
            print("Warning: Network not built yet. Nothing to store.")
            return
        self.brian_network.store(name=filename)
        print(f"Simulation state stored in '{filename}.bri'")

    def restore_simulation(self, filename="pybrainorg_sim_state"):
        """
        Restores the state of the simulation network from a file.
        (Implementation details as before)
        """
        if self.brian_network is None:
            print("Warning: Network not explicitly built. Ensure objects are defined before restoring.")
        
        b2.restore(name=filename)
        print(f"Simulation state restored from '{filename}.bri'. Network may need to be rebuilt.")
        self.brian_network = None # Force rebuild on next run
        self.brian_dt = b2.defaultclock.dt # Update dt from restored clock

    def __str__(self):
        status = "Built" if self.brian_network else "Not Built"
        return (f"<Simulator for Organoid '{self.organoid.name}' "
                f"with {len(self.monitors)} monitor(s). Network Status: {status}>")

    def __repr__(self):
        return self.__str__()