# pybrainorg/simulation/simulator.py

import brian2 as b2
from ..organoid.organoid import Organoid
from ..electrophysiology import brian_monitors as pbg_monitors

class Simulator:
    def __init__(self, organoid: Organoid, brian2_dt=None):
        if not isinstance(organoid, Organoid):
            raise TypeError("organoid must be an instance of pybrainorg.organoid.Organoid.")
        self.organoid = organoid
        self.brian_network = None
        self.monitors = {} # User-defined name -> monitor object
        
        if brian2_dt is not None:
            if not isinstance(brian2_dt, b2.Quantity) or not (brian2_dt.dimensions == b2.second.dimensions):
                raise TypeError("brian2_dt must be a Brian2 Quantity with time units.")
            self.brian_dt = brian2_dt
            b2.defaultclock.dt = self.brian_dt
        else:
            self.brian_dt = b2.defaultclock.dt
        self._network_objects = list(self.organoid.brian2_objects)

   def add_recording(self, monitor_name: str, monitor_type: str, target_group_name: str, **kwargs):
        print(f"--- DEBUG: add_recording called with monitor_name='{monitor_name}', monitor_type='{monitor_type}', target_group_name='{target_group_name}' ---")
        if monitor_name in self.monitors:
            print(f"DEBUG: Error - Monitor name '{monitor_name}' already exists.")
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        
        try:
            target_group = self.organoid.get_neuron_group(target_group_name)
            print(f"DEBUG: Found target_group: {target_group.name}")
        except KeyError as e:
            print(f"DEBUG: Error - Target group '{target_group_name}' not found: {e}")
            raise
        
        monitor_object = None
        brian2_monitor_name = kwargs.pop('name', f"{monitor_name}_{target_group.name}")
        print(f"DEBUG: Attempting to create Brian2 monitor named: {brian2_monitor_name}")

        try:
            if monitor_type.lower() == "spike":
                monitor_object = pbg_monitors.setup_spike_monitor(target_group, name=brian2_monitor_name, **kwargs)
                print(f"DEBUG: setup_spike_monitor returned: {monitor_object}")
            elif monitor_type.lower() == "state":
                if 'variables' not in kwargs:
                    print("DEBUG: Error - 'variables' missing for state monitor.")
                    raise KeyError("Argument 'variables' (str or list of str) is required for 'state' monitor.")
                monitor_object = pbg_monitors.setup_state_monitor(target_group, name=brian2_monitor_name, **kwargs)
                print(f"DEBUG: setup_state_monitor returned: {monitor_object}")
            elif monitor_type.lower() == "population_rate":
                monitor_object = pbg_monitors.setup_population_rate_monitor(target_group, name=brian2_monitor_name, **kwargs)
                print(f"DEBUG: setup_population_rate_monitor returned: {monitor_object}")
            else:
                print(f"DEBUG: Error - Unsupported monitor_type: '{monitor_type}'.")
                raise ValueError(f"Unsupported monitor_type: '{monitor_type}'. "
                                 "Supported types are 'spike', 'state', 'population_rate'.")
        except Exception as e_setup:
            print(f"DEBUG: Exception during monitor setup function call: {e_setup}")
            # Decida se quer relançar ou apenas definir monitor_object como None e continuar para ver o if
            # Para debug, pode ser útil não relançar imediatamente para ver o print abaixo.
            # raise # Descomente para relançar e parar aqui

        print(f"DEBUG: Value of monitor_object before 'if monitor_object:': {monitor_object}, type: {type(monitor_object)}")
        if monitor_object:
            self.monitors[monitor_name] = monitor_object
            print(f"DEBUG: Added '{monitor_name}' to self.monitors. Current keys: {list(self.monitors.keys())}")
            if monitor_object not in self._network_objects:
                self._network_objects.append(monitor_object)
                print(f"DEBUG: Added monitor object to self._network_objects.")
        else:
            print(f"DEBUG: monitor_object is None or False. NOT adding to self.monitors for monitor_name='{monitor_name}'.")
        
        print(f"--- DEBUG: add_recording finished for '{monitor_name}' ---")
        return monitor_object

    def build_network(self, **network_kwargs):
        self.brian_network = b2.Network(self._network_objects, **network_kwargs)

    def run(self, duration: b2.units.fundamentalunits.Quantity, report=None, report_period=10*b2.second, **run_kwargs):
        if not isinstance(duration, b2.Quantity) or not (duration.dimensions == b2.second.dimensions):
            raise TypeError("duration must be a Brian2 Quantity with time units.")
        if self.brian_network is None:
            self.build_network()
        if self.brian_network is None:
            raise RuntimeError("Brian2 Network could not be built or is still None.")
        self.brian_network.run(duration, report=report, report_period=report_period, **run_kwargs)

    def get_data(self, monitor_name: str):
        if monitor_name not in self.monitors:
            # Fornecer mais contexto no erro
            raise KeyError(f"Monitor with name '{monitor_name}' not found. Available monitors: {list(self.monitors.keys())}")
        return self.monitors[monitor_name]

    def store_simulation(self, filename="pybrainorg_sim_state"):
        if self.brian_network is None:
            print("Warning: Network not built yet. Nothing to store.")
            return
        self.brian_network.store(name=filename)
        print(f"Simulation state stored in '{filename}.bri'")

    def restore_simulation(self, filename="pybrainorg_sim_state"):
        if self.brian_network is None:
            print("Warning: Network not explicitly built. Ensure objects are defined before restoring.")
        b2.restore(name=filename)
        print(f"Simulation state restored from '{filename}.bri'. Network may need to be rebuilt.")
        self.brian_network = None
        self.brian_dt = b2.defaultclock.dt

    def __str__(self):
        status = "Built" if self.brian_network else "Not Built"
        return (f"<Simulator for Organoid '{self.organoid.name}' "
                f"with {len(self.monitors)} monitor(s). Network Status: {status}>")

    def __repr__(self):
        return self.__str__()
