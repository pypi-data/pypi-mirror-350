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
        """
        Adds a Brian2 monitor to record activity from a specified neuron group.
        """
        if monitor_name in self.monitors:
            raise ValueError(f"Monitor with name '{monitor_name}' already exists.")
        
        target_group = self.organoid.get_neuron_group(target_group_name)

        monitor_object = None 
        brian2_monitor_name = kwargs.pop('name', f"{monitor_name}_{target_group.name}")

        if monitor_type.lower() == "spike":
            monitor_object = pbg_monitors.setup_spike_monitor(target_group, name=brian2_monitor_name, **kwargs)
        elif monitor_type.lower() == "state":
            if 'variables' not in kwargs:
                raise KeyError("Argument 'variables' (str or list of str) is required for 'state' monitor.")
            monitor_object = pbg_monitors.setup_state_monitor(target_group, name=brian2_monitor_name, **kwargs)
        elif monitor_type.lower() == "population_rate":
            monitor_object = pbg_monitors.setup_population_rate_monitor(target_group, name=brian2_monitor_name, **kwargs)
        else:
            raise ValueError(f"Unsupported monitor_type: '{monitor_type}'. "
                             "Supported types are 'spike', 'state', 'population_rate'.")

        print(monitor_object)

        if monitor_object:
            # --- LINHA CRUCIAL DA CORREÇÃO ---
            self.monitors[monitor_name] = monitor_object
            # --- FIM DA CORREÇÃO ---
            if monitor_object not in self._network_objects:
                self._network_objects.append(monitor_object)
        
        return monitor_object # Retorna o objeto monitor criado

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
