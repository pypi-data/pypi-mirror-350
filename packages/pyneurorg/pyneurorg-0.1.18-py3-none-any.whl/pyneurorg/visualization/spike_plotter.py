# pyneurorg/visualization/spike_plotter.py

"""
Functions for visualizing spike train data and membrane potential traces
from pyneurorg simulations, using Matplotlib.
"""

import matplotlib.pyplot as plt
import numpy as np
import brian2 as b2

def plot_raster(spike_indices, spike_times, duration=None, ax=None,
                marker_size=2, marker_color='black', title="Raster Plot",
                time_unit_display=b2.ms, ylabel="Neuron Index"):
    """
    Generates a raster plot of spike activity.

    Parameters
    ----------
    spike_indices : array-like
        Array of neuron indices corresponding to each spike.
        Typically `SpikeMonitor.i`.
    spike_times : brian2.units.fundamentalunits.Quantity or array-like
        Array of spike times. Typically `SpikeMonitor.t`.
        If a Brian2 Quantity, it will be converted to `time_unit_display`.
        If not a Quantity, it's assumed to be in units matching `time_unit_display`.
    duration : brian2.units.fundamentalunits.Quantity or float, optional
        Total duration for the x-axis limit. If a Brian2 Quantity, it's converted
        to `time_unit_display`. If a float, it's assumed to be in `time_unit_display`.
        If None, limits are set based on min/max spike times. (default: None).
    ax : matplotlib.axes.Axes, optional
        An existing Matplotlib Axes object to plot on. If None, a new
        figure and axes are created. (default: None).
    marker_size : int, optional
        Size of the markers for spikes (default: 2).
    marker_color : str, optional
        Color of the spike markers (default: 'black').
    title : str, optional
        Title for the plot (default: "Raster Plot").
    time_unit_display : brian2.units.fundamentalunits.UnitSymbol, optional
        The Brian2 unit to use for displaying time on the x-axis (default: b2.ms).
    ylabel : str, optional
        Label for the y-axis (default: "Neuron Index").

    Returns
    -------
    matplotlib.axes.Axes
        The Matplotlib Axes object containing the plot.

    Examples
    --------
    >>> import brian2 as b2
    >>> import matplotlib.pyplot as plt
    >>> from pyneurorg.visualization.spike_plotter import plot_raster # Assuming pyneurorg is importable
    >>> # Example NeuronGroup and SpikeMonitor setup
    >>> G = b2.NeuronGroup(5, 'dv/dt=-v/(10*b2.ms) : 1', threshold='v>1', reset='v=0', method='exact')
    >>> G.v = [1.1, 0.5, 1.2, 0.1, 1.3] # Make some spike
    >>> spikemon = b2.SpikeMonitor(G)
    >>> net = b2.Network(G, spikemon)
    >>> simulation_time = 10*b2.ms
    >>> net.run(simulation_time)
    >>> # Create figure and axes for plotting
    >>> fig, ax_plot = plt.subplots()
    >>> plot_raster(spikemon.i, spikemon.t, duration=simulation_time, ax=ax_plot, time_unit_display=b2.ms)
    >>> # plt.show() # Uncomment in a script or use in Jupyter for display
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4)) # Default figure size

    # Convert spike_times to numerical values in the desired display unit
    if isinstance(spike_times, b2.Quantity):
        if spike_times.dimensions != b2.second.dimensions:
            raise TypeError("spike_times must have time dimensions if it's a Brian2 Quantity.")
        plot_times_val = np.asarray(spike_times / time_unit_display)
    elif isinstance(spike_times, (np.ndarray, list)):
        plot_times_val = np.asarray(spike_times) # Assume already in correct scale for time_unit_display
    else:
        raise TypeError("spike_times must be a Brian2 Quantity or array-like.")

    plot_duration_val = None
    if duration is not None:
        if isinstance(duration, b2.Quantity):
            if duration.dimensions != b2.second.dimensions:
                raise TypeError("duration must have time dimensions if it's a Brian2 Quantity.")
            plot_duration_val = float(duration / time_unit_display)
        elif isinstance(duration, (int, float)):
            plot_duration_val = float(duration) # Assume already in correct scale for time_unit_display
        else:
            raise TypeError("duration must be a Brian2 Quantity, a number, or None.")

    if len(plot_times_val) > 0 or plot_duration_val is not None : # Only plot if there's data or a duration to set xlim
        ax.plot(plot_times_val, spike_indices, '|', markersize=marker_size, color=marker_color)

        ax.set_xlabel(f"Time ({time_unit_display!s})") # Label with the unit used
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        if plot_duration_val is not None:
            ax.set_xlim([0, plot_duration_val])
        elif len(plot_times_val) > 0: # Auto-scale if duration not given but spikes exist
            min_t, max_t = np.min(plot_times_val), np.max(plot_times_val)
            # Add some padding to the x-axis
            padding = 0.05 * (max_t - min_t) if (max_t - min_t) > 1e-9 else 0.05 * max_t # Avoid zero padding if all spikes at same time
            if padding == 0 and max_t == 0 : padding = 1.0 # Handle all zero case for padding
            ax.set_xlim([max(0, min_t - padding), max_t + padding])
        else: # No spikes and no duration, set a default small range
            ax.set_xlim([0, 1])

        if len(spike_indices) > 0:
            ax.set_ylim([np.min(spike_indices) - 0.5, np.max(spike_indices) + 0.5])
        else: # Handle case with no spikes for y-axis as well
            ax.set_ylim([-0.5, 0.5]) # Default if no neurons to show
    else: # No data to plot and no duration
        ax.set_xlabel(f"Time ({time_unit_display!s})")
        ax.set_ylabel(ylabel)
        ax.set_title(title + " (No data)")
        ax.set_xlim([0,1])
        ax.set_ylim([-0.5, 0.5])


    ax.grid(True, linestyle=':', alpha=0.7)
    return ax


def plot_vm_traces(state_monitor, neuron_indices=None, time_unit_display=b2.ms, voltage_unit_display=b2.mV,
                   ax=None, title="Membrane Potential Traces",
                   xlabel=None, ylabel=None, legend_loc="best", alpha=0.8):
    """
    Plots membrane potential (Vm) traces for selected neurons from a StateMonitor.

    Parameters
    ----------
    state_monitor : brian2.monitors.statemonitor.StateMonitor
        The Brian2 StateMonitor object containing the Vm recordings.
    neuron_indices : int, list of int, or slice, optional
        The index or indices of neurons whose Vm traces to plot, relative to the
        neurons recorded by the monitor. If None, and the StateMonitor recorded
        few neurons (e.g., <= 5), all recorded traces are plotted. If many
        neurons were recorded, this must be specified. (default: None).
    time_unit_display : brian2.units.fundamentalunits.UnitSymbol, optional
        The Brian2 unit to use for displaying time on the x-axis (default: b2.ms).
    voltage_unit_display : brian2.units.fundamentalunits.UnitSymbol, optional
        The Brian2 unit to use for displaying voltage on the y-axis (default: b2.mV).
    ax : matplotlib.axes.Axes, optional
        An existing Matplotlib Axes object to plot on.
    title : str, optional
        Title for the plot.
    xlabel : str, optional
        Label for the x-axis. If None, defaults to "Time (unit)".
    ylabel : str, optional
        Label for the y-axis. If None, defaults to "Vm (unit)".
    legend_loc : str or int or None, optional
        Location for the legend (default: "best"). Set to None to hide.
    alpha : float, optional
        Alpha transparency for the plot lines (default: 0.8).

    Returns
    -------
    matplotlib.axes.Axes
        The Matplotlib Axes object containing the plot.

    Raises
    ------
    AttributeError
        If the StateMonitor does not have a recorded variable 'v' or another
        suitable voltage variable.
    ValueError
        If `neuron_indices` are out of bounds for the recorded data.

    Examples
    --------
    >>> import brian2 as b2
    >>> import matplotlib.pyplot as plt
    >>> from pyneurorg.visualization.spike_plotter import plot_vm_traces
    >>> G = b2.NeuronGroup(3, 'dv/dt = (0.5-v)/(10*b2.ms) : 1', threshold='v>1', reset='v=0', method='exact')
    >>> G.v = [0, 0.1, 0.2] # Initial values
    >>> statemon = b2.StateMonitor(G, 'v', record=[0,1,2], dt=0.1*b2.ms) # Record Vm for all 3
    >>> net = b2.Network(G, statemon)
    >>> net.run(20*b2.ms)
    >>> fig, ax_plot = plt.subplots()
    >>> plot_vm_traces(statemon, neuron_indices=[0,1,2], ax=ax_plot) # Plot selected (or all recorded)
    >>> # plt.show()
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    # Determine which variable to plot as Vm
    voltage_data_to_plot = None
    voltage_var_name_recorded = ""
    if hasattr(state_monitor, 'v'):
        voltage_data_to_plot = state_monitor.v
        voltage_var_name_recorded = 'v'
    elif state_monitor.variables: # Check the dict of recorded variables
        # Prefer 'v' if it's among them, otherwise take the first one
        if 'v' in state_monitor.variables:
            voltage_data_to_plot = getattr(state_monitor, 'v')
            voltage_var_name_recorded = 'v'
        else:
            first_var_key = list(state_monitor.variables.keys())[0]
            voltage_data_to_plot = getattr(state_monitor, first_var_key)
            voltage_var_name_recorded = first_var_key
            print(f"Info: Plotting variable '{voltage_var_name_recorded}' as Vm from StateMonitor.")
    else:
        raise AttributeError("StateMonitor does not seem to have recorded 'v' or any other variables.")
    
    if voltage_data_to_plot is None: # Should be caught above
        raise AttributeError("Could not extract voltage data from StateMonitor.")

    # Ensure voltage_data_to_plot is a Quantity with voltage dimensions
    if not (isinstance(voltage_data_to_plot, b2.Quantity) and voltage_data_to_plot.dimensions == b2.volt.dimensions):
        raise TypeError(f"Recorded variable '{voltage_var_name_recorded}' does not have voltage dimensions.")

    times_qty = state_monitor.t
    if not (isinstance(times_qty, b2.Quantity) and times_qty.dimensions == b2.second.dimensions):
        raise TypeError("StateMonitor.t does not have time dimensions.")

    # Convert data to numerical values in desired display units
    times_val = np.asarray(times_qty / time_unit_display)
    voltages_val = np.asarray(voltage_data_to_plot / voltage_unit_display)

    # Determine which neurons to plot (indices relative to the monitor's recorded data)
    num_actually_recorded_neurons = voltages_val.shape[0]
    indices_in_monitor_to_plot = []

    if neuron_indices is None:
        if num_actually_recorded_neurons <= 5: # Plot all if few are recorded by the monitor
            indices_in_monitor_to_plot = list(range(num_actually_recorded_neurons))
        elif num_actually_recorded_neurons > 0: # More than 5 recorded, user must specify
            raise ValueError(f"{num_actually_recorded_neurons} neurons recorded by StateMonitor. "
                             "Please specify `neuron_indices` (relative to recorded neurons) to plot, or record fewer neurons.")
        # If num_actually_recorded_neurons is 0, indices_in_monitor_to_plot remains empty.
    elif isinstance(neuron_indices, int):
        if not (0 <= neuron_indices < num_actually_recorded_neurons):
            raise ValueError(f"neuron_index {neuron_indices} out of bounds for monitor's recorded data (0 to {num_actually_recorded_neurons-1}).")
        indices_in_monitor_to_plot = [neuron_indices]
    elif isinstance(neuron_indices, (list, slice, np.ndarray)):
        if isinstance(neuron_indices, slice):
            indices_in_monitor_to_plot = list(range(*neuron_indices.indices(num_actually_recorded_neurons)))
        else: # list or ndarray
            indices_in_monitor_to_plot = list(neuron_indices)
        for idx_mon in indices_in_monitor_to_plot: # Validate each index
            if not (0 <= idx_mon < num_actually_recorded_neurons):
                raise ValueError(f"Neuron index {idx_mon} in `neuron_indices` is out of bounds "
                                 f"for monitor's recorded data (0 to {num_actually_recorded_neurons-1}).")
    else:
        raise TypeError("neuron_indices must be None, int, list, slice, or np.ndarray.")

    if not indices_in_monitor_to_plot and num_actually_recorded_neurons > 0:
        # This case should ideally be caught by neuron_indices=None logic above if many are recorded
        print("Warning: No specific neuron indices selected for plotting Vm, but data was recorded.")
        # Optionally, could default to plotting the first one if this state is reached.
        # For now, it will plot nothing if list is empty.
    elif num_actually_recorded_neurons == 0:
        print("Warning: StateMonitor recorded no data or no neurons.")


    # Plotting the selected traces
    for monitor_idx_to_plot in indices_in_monitor_to_plot:
        # Get the original index of the neuron in the full NeuronGroup
        # state_monitor.record is True if all neurons in source were recorded,
        # or it's a list/array of indices, or a slice object.
        original_neuron_label = ""
        if isinstance(state_monitor.record, (list, np.ndarray)):
            original_neuron_label = f"Neuron {state_monitor.record[monitor_idx_to_plot]}"
        elif isinstance(state_monitor.record, slice):
            # This reconstructs the original index if record was a slice
            start = state_monitor.record.start if state_monitor.record.start is not None else 0
            step = state_monitor.record.step if state_monitor.record.step is not None else 1
            original_neuron_label = f"Neuron {start + monitor_idx_to_plot * step}"
        elif state_monitor.record is True: # All neurons recorded
            original_neuron_label = f"Neuron {monitor_idx_to_plot}"
        else: # Unclear how to get original index, use monitor index
             original_neuron_label = f"Trace {monitor_idx_to_plot}"


        ax.plot(times_val, voltages_val[monitor_idx_to_plot, :],
                label=original_neuron_label, alpha=alpha)

    ax.set_title(title)
    ax.set_xlabel(xlabel if xlabel is not None else f"Time ({time_unit_display!s})")
    ax.set_ylabel(ylabel if ylabel is not None else f"Vm ({voltage_unit_display!s})")

    if legend_loc and len(indices_in_monitor_to_plot) > 0:
        ax.legend(loc=legend_loc, fontsize='small')

    ax.grid(True, linestyle=':', alpha=0.7)
    return ax