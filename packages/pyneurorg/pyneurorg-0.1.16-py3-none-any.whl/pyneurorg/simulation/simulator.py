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
        print("--- DEBUG: Simulator.__init__ called ---")
        if not isinstance(organoid, Organoid):
            print(f"DEBUG: Error - organoid is not an instance of Organoid. Type: {type(organoid)}")
            raise TypeError("organoid must be an instance of pybrainorg.organoid.Organoid.")
        print(f"DEBUG: Organoid received: {organoid.name}")

        self.organoid = organoid
        self.brian_network = None
        self.monitors = {} 
        
        if brian2_dt is not None:
            print(f"DEBUG: User provided brian2_dt: {brian2_dt}")
            if not isinstance(brian2_dt, b2.Quantity) or not (brian2_dt.dimensions == b2.second.dimensions):
                print(f"DEBUG: Error - brian2_dt type or dimension mismatch. Type: {type(brian2_dt)}, Dims: {getattr(brian2_dt, 'dimensions', 'N/A')}")
                raise TypeError("brian2_dt must be a Brian2 Quantity with time units.")
            self.brian_dt = brian2_dt
            b2.defaultclock.dt = self.brian_dt 
            print(f"DEBUG: b2.defaultclock.dt set to: {b2.defaultclock.dt}")
        else:
            self.brian_dt = b2.defaultclock.dt 
            print(f"DEBUG: Using default b2.defaultclock.dt: {self.brian_dt}")
        
        self._network_objects = list(self.organoid.brian2_objects)
        print(f"DEBUG: Initial _network_objects from organoid: {[obj.name for obj in self._network_objects if hasattr(obj, 'name')]}")
        print(f"--- DEBUG: Simulator.__init__ finished. self.monitors is currently: {self.monitors} ---")


    def add_recording(self, monitor_name: str, monitor_type: str, target_group_name: str, **kwargs):
        """
        Adds a Brian2 monitor to record activity from a specified neuron group.
        """
        print(f"--- DEBUG: Simulator.add_recording called with: ---")
        print(f"  monitor_name='{monitor_name}'")
        print(f"  monitor_type='{monitor_type}'")
        print(f"  target_group_name='{target_group_name}'")
        print(f"  kwargs: {kwargs}")
        
        if monitor_name in self.monitors:
            print(f"DEBUG: Error - Monitor name '{monitor_name}' already exists in self.monitors: {list(self.monitors.keys())}")
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        
        try:
            target_group = self.organoid.get_neuron_group(target_group_name)
            print(f"DEBUG: Found target_group: {target_group.name} (type: {type(target_group)})")
        except KeyError as e:
            print(f"DEBUG: Error - Target group '{target_group_name}' not found in organoid: {e}")
            raise
        
        monitor_object = None
        # Ensure the monitor created by Brian2 has a unique internal name
        brian2_monitor_internal_name = kwargs.pop('name', f"pyb_mon_{monitor_name}_{target_group.name}")
        print(f"DEBUG: Attempting to create Brian2 monitor with internal name: {brian2_monitor_internal_name}")

        try:
            if monitor_type.lower() == "spike":
                monitor_object = pbg_monitors.setup_spike_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
                print(f"DEBUG: pbg_monitors.setup_spike_monitor returned: {monitor_object} (type: {type(monitor_object)})")
            elif monitor_type.lower() == "state":
                if 'variables' not in kwargs:
                    print("DEBUG: Error - 'variables' missing for state monitor.")
                    raise KeyError("Argument 'variables' (str or list of str) is required for 'state' monitor.")
                monitor_object = pbg_monitors.setup_state_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
                print(f"DEBUG: pbg_monitors.setup_state_monitor returned: {monitor_object} (type: {type(monitor_object)})")
            elif monitor_type.lower() == "population_rate":
                monitor_object = pbg_monitors.setup_population_rate_monitor(target_group, name=brian2_monitor_internal_name, **kwargs)
                print(f"DEBUG: pbg_monitors.setup_population_rate_monitor returned: {monitor_object} (type: {type(monitor_object)})")
            else:
                print(f"DEBUG: Error - Unsupported monitor_type: '{monitor_type}'.")
                raise ValueError(f"Unsupported monitor_type: '{monitor_type}'. "
                                 "Supported types are 'spike', 'state', 'population_rate'.")
        except Exception as e_setup:
            print(f"DEBUG: Exception during pbg_monitors setup function call for '{monitor_name}': {e_setup}")
            # For debugging, we might not re-raise immediately to see subsequent prints
            # raise # Uncomment to re-raise and stop execution here

        print(f"DEBUG: Value of monitor_object before 'if monitor_object:': {monitor_object}")
        if monitor_object: # Checks if monitor_object is not None and not False (though monitors shouldn't be False)
            self.monitors[monitor_name] = monitor_object
            print(f"DEBUG: Successfully added '{monitor_name}' (object: {monitor_object.name}) to self.monitors.")
            print(f"DEBUG: self.monitors now contains keys: {list(self.monitors.keys())}")
            if monitor_object not in self._network_objects:
                self._network_objects.append(monitor_object)
                print(f"DEBUG: Added monitor object '{monitor_object.name}' to self._network_objects.")
            else:
                print(f"DEBUG: Monitor object '{monitor_object.name}' was already in self._network_objects.")
        else:
            print(f"DEBUG: monitor_object is None or False. NOT adding to self.monitors for monitor_name='{monitor_name}'.")
        
        print(f"--- DEBUG: Simulator.add_recording finished for '{monitor_name}' ---")
        return monitor_object

    def build_network(self, **network_kwargs):
        print("--- DEBUG: Simulator.build_network called ---")
        print(f"DEBUG: Building network with _network_objects: {[obj.name for obj in self._network_objects if hasattr(obj, 'name')]}")
        self.brian_network = b2.Network(self._network_objects, **network_kwargs)
        print(f"DEBUG: Brian2 Network built: {self.brian_network}")
        print("--- DEBUG: Simulator.build_network finished ---")


    def run(self, duration: b2.units.fundamentalunits.Quantity, report=None, report_period=10*b2.second, **run_kwargs):
        print(f"--- DEBUG: Simulator.run called with duration: {duration} ---")
        if not isinstance(duration, b2.Quantity) or not (duration.dimensions == b2.second.dimensions):
            print(f"DEBUG: Error - duration type or dimension mismatch. Type: {type(duration)}, Dims: {getattr(duration, 'dimensions', 'N/A')}")
            raise TypeError("duration must be a Brian2 Quantity with time units.")

        if self.brian_network is None:
            print("DEBUG: Brian2 Network is None, calling build_network().")
            self.build_network(**run_kwargs.pop('network_kwargs', {})) # Pass network_kwargs if provided via run_kwargs

        if self.brian_network is None:
            print("DEBUG: Error - Brian2 Network could not be built or is still None after calling build_network().")
            raise RuntimeError("Brian2 Network could not be built or is still None.")
        
        print(f"DEBUG: Executing brian_network.run({duration}, report='{report}', report_period={report_period})")
        self.brian_network.run(duration, report=report, report_period=report_period, **run_kwargs)
        print(f"--- DEBUG: Simulator.run finished for duration: {duration} ---")

    def get_data(self, monitor_name: str):
        print(f"--- DEBUG: Simulator.get_data called for monitor_name='{monitor_name}' ---")
        print(f"DEBUG: Current self.monitors keys: {list(self.monitors.keys())}")
        if monitor_name not in self.monitors:
            print(f"DEBUG: Error - Monitor '{monitor_name}' not found in self.monitors.")
            raise KeyError(f"Monitor with name '{monitor_name}' not found. Available monitors: {list(self.monitors.keys())}")
        
        monitor_to_return = self.monitors[monitor_name]
        print(f"DEBUG: Returning data for monitor '{monitor_name}': {monitor_to_return}")
        print(f"--- DEBUG: Simulator.get_data finished for '{monitor_name}' ---")
        return monitor_to_return

    def store_simulation(self, filename="pybrainorg_sim_state"):
        print(f"--- DEBUG: Simulator.store_simulation called for filename='{filename}' ---")
        if self.brian_network is None:
            print("DEBUG: Warning - Network not built yet. Nothing to store.")
            return
        self.brian_network.store(name=filename)
        print(f"DEBUG: Simulation state stored in '{filename}.bri'")
        print(f"--- DEBUG: Simulator.store_simulation finished ---")


    def restore_simulation(self, filename="pybrainorg_sim_state"):
        print(f"--- DEBUG: Simulator.restore_simulation called for filename='{filename}' ---")
        if self.brian_network is None: # This check might be less relevant as b2.restore handles the network
            print("DEBUG: Warning - Network not explicitly built locally before restore. Brian2 will handle network object.")
        
        b2.restore(name=filename)
        print(f"DEBUG: Brian2 state restored from '{filename}.bri'.")
        # After restore, Brian2's defaultclock and potentially objects are restored globally.
        # The Simulator's internal Network object might be stale if it was built before restore.
        self.brian_network = None # Force rebuild on next run to use restored state/objects
        self.brian_dt = b2.defaultclock.dt # Update dt from restored clock
        print(f"DEBUG: self.brian_network set to None. self.brian_dt updated to {self.brian_dt}.")
        print(f"--- DEBUG: Simulator.restore_simulation finished ---")


    def __str__(self):
        status = "Built" if self.brian_network else "Not Built"
        num_monitors = len(self.monitors)
        return (f"<Simulator for Organoid '{self.organoid.name}' "
                f"with {num_monitors} user-defined monitor(s). Network Status: {status}>")

    def __repr__(self):
        return self.__str__()