# pybrainorg/visualization/spike_plotter.py

"""
Functions for visualizing spike train data and membrane potential traces
from pybrainorg simulations, using Matplotlib.
"""

import matplotlib.pyplot as plt
import numpy as np
import brian2 as b2

def plot_raster(spike_indices, spike_times, duration=None, ax=None,
                marker_size=2, marker_color='black', title="Raster Plot",
                xlabel="Time (ms)", ylabel="Neuron Index"):
    """
    Generates a raster plot of spike activity.

    Parameters
    ----------
    spike_indices : array-like
        Array of neuron indices corresponding to each spike.
        Typically `SpikeMonitor.i`.
    spike_times : brian2.units.fundamentalunits.Quantity or array-like
        Array of spike times. Typically `SpikeMonitor.t`.
        If not a Brian2 Quantity, units are assumed to be ms for the plot.
    duration : brian2.units.fundamentalunits.Quantity, optional
        Total duration of the simulation, used to set x-axis limits.
        If None, limits are set by min/max spike times. (default: None).
    ax : matplotlib.axes.Axes, optional
        An existing Matplotlib Axes object to plot on. If None, a new
        figure and axes are created. (default: None).
    marker_size : int, optional
        Size of the markers for spikes (default: 2).
    marker_color : str, optional
        Color of the spike markers (default: 'black').
    title : str, optional
        Title for the plot (default: "Raster Plot").
    xlabel : str, optional
        Label for the x-axis (default: "Time (ms)").
    ylabel : str, optional
        Label for the y-axis (default: "Neuron Index").

    Returns
    -------
    matplotlib.axes.Axes
        The Matplotlib Axes object containing the plot.

    Examples
    --------
    >>> from brian2 import SpikeMonitor, NeuronGroup, run, ms, Network
    >>> from pybrainorg.visualization.spike_plotter import plot_raster
    >>> G = NeuronGroup(5, 'dv/dt=-v/(10*ms) : 1', threshold='v>1', reset='v=0', method='exact')
    >>> G.v = [1.1, 0.5, 1.2, 0.1, 1.3] # Make some spike
    >>> spikemon = SpikeMonitor(G)
    >>> net = Network(G, spikemon)
    >>> net.run(10*ms)
    >>> fig, ax = plt.subplots() # Create figure and axes
    >>> plot_raster(spikemon.i, spikemon.t, duration=10*ms, ax=ax)
    >>> # plt.show() # Uncomment to display
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4)) # Default figure size

    # Convert spike_times to ms if they are Brian2 Quantities
    if hasattr(spike_times, 'unit'):
        plot_times = spike_times / b2.ms
        if duration is not None and hasattr(duration, 'unit'):
            plot_duration = duration / b2.ms
        elif duration is not None: # Assume ms if no unit but duration provided
            plot_duration = duration
        else:
            plot_duration = None
    else: # Assume already in ms or unitless
        plot_times = spike_times
        plot_duration = duration

    ax.plot(plot_times, spike_indices, '|', markersize=marker_size, color=marker_color)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if plot_duration is not None:
        ax.set_xlim([0, plot_duration])
    elif len(plot_times) > 0:
        ax.set_xlim([min(plot_times) - 0.1*max(plot_times) if len(plot_times)>0 else 0,
                     max(plot_times) + 0.1*max(plot_times) if len(plot_times)>0 else 1]) # Add some padding

    if len(spike_indices) > 0:
        ax.set_ylim([min(spike_indices) - 0.5, max(spike_indices) + 0.5])
    else:
        ax.set_ylim([-0.5, 0.5]) # Handle case with no spikes

    ax.grid(True, linestyle=':', alpha=0.7)
    return ax


def plot_vm_traces(state_monitor, neuron_indices=None, time_unit=b2.ms, voltage_unit=b2.mV,
                   ax=None, title="Membrane Potential Traces",
                   xlabel=None, ylabel=None, legend_loc="best", alpha=0.8):
    """
    Plots membrane potential (Vm) traces for selected neurons from a StateMonitor.

    Assumes the StateMonitor has recorded a variable named 'v' or one of the
    variables specified if `variables` (list) was used.

    Parameters
    ----------
    state_monitor : brian2.monitors.statemonitor.StateMonitor
        The Brian2 StateMonitor object containing the Vm recordings.
    neuron_indices : int, list of int, or slice, optional
        The index or indices of neurons whose Vm traces to plot.
        If None, and the StateMonitor recorded few neurons (e.g., <= 5),
        all recorded traces are plotted. If many neurons were recorded,
        this must be specified to avoid a cluttered plot. (default: None).
    time_unit : brian2.units.fundamentalunits.UnitSymbol, optional
        The unit to display time in on the x-axis (default: b2.ms).
    voltage_unit : brian2.units.fundamentalunits.UnitSymbol, optional
        The unit to display voltage in on the y-axis (default: b2.mV).
    ax : matplotlib.axes.Axes, optional
        An existing Matplotlib Axes object to plot on. If None, a new
        figure and axes are created. (default: None).
    title : str, optional
        Title for the plot (default: "Membrane Potential Traces").
    xlabel : str, optional
        Label for the x-axis. If None, defaults to "Time (unit)". (default: None).
    ylabel : str, optional
        Label for the y-axis. If None, defaults to "Vm (unit)". (default: None).
    legend_loc : str or int, optional
        Location for the legend (default: "best"). Set to None to hide legend.
    alpha : float, optional
        Alpha transparency for the plot lines (default: 0.8).

    Returns
    -------
    matplotlib.axes.Axes
        The Matplotlib Axes object containing the plot.

    Raises
    ------
    AttributeError
        If the StateMonitor does not have a recorded variable 'v' (or other
        primary voltage variable).
    ValueError
        If `neuron_indices` are out of bounds for the recorded data.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    if not hasattr(state_monitor, 'v') and not state_monitor.variables:
        raise AttributeError("StateMonitor does not seem to have recorded 'v' or any variables.")

    # Try to get 'v', or the first recorded variable if 'v' is not present
    if hasattr(state_monitor, 'v'):
        voltages = state_monitor.v
        voltage_var_name = 'v'
    elif state_monitor.variables: # variables is a dict {'varname': index_in_data_array}
        # Take the first variable recorded if 'v' is not explicitly an attribute
        first_var_name = list(state_monitor.variables.keys())[0]
        voltages = getattr(state_monitor, first_var_name)
        voltage_var_name = first_var_name
        print(f"Plotting variable '{voltage_var_name}' as Vm.")
    else: # Should have been caught by the first check
        raise AttributeError("Could not find voltage data in StateMonitor.")


    times = state_monitor.t

    # Determine which neurons to plot
    num_recorded_neurons = voltages.shape[0]
    plot_indices_in_monitor = [] # Indices relative to the `voltages` array

    if neuron_indices is None:
        if num_recorded_neurons <= 5: # Plot all if few are recorded
            plot_indices_in_monitor = list(range(num_recorded_neurons))
        else:
            raise ValueError("Many neurons recorded. Please specify `neuron_indices` to plot.")
    elif isinstance(neuron_indices, int):
        if not (0 <= neuron_indices < num_recorded_neurons):
            raise ValueError(f"neuron_index {neuron_indices} out of bounds for recorded data (0-{num_recorded_neurons-1}).")
        plot_indices_in_monitor = [neuron_indices]
    elif isinstance(neuron_indices, (list, slice, np.ndarray)):
        # Convert slice to list of indices
        if isinstance(neuron_indices, slice):
            plot_indices_in_monitor = list(range(*neuron_indices.indices(num_recorded_neurons)))
        else: # list or ndarray
            plot_indices_in_monitor = list(neuron_indices)

        for idx in plot_indices_in_monitor:
            if not (0 <= idx < num_recorded_neurons):
                raise ValueError(f"Neuron index {idx} out of bounds for recorded data (0-{num_recorded_neurons-1}).")
    else:
        raise TypeError("neuron_indices must be None, int, list, slice, or np.ndarray.")


    if not plot_indices_in_monitor:
        print("Warning: No neuron indices selected for plotting Vm.")
        return ax

    # Plotting
    for i, monitor_idx in enumerate(plot_indices_in_monitor):
        # Original index in the full NeuronGroup (if StateMonitor recorded a subset)
        # state_monitor.record will be True, or a list of original indices, or a slice
        original_idx = monitor_idx
        if isinstance(state_monitor.record, (list, np.ndarray)):
            original_idx = state_monitor.record[monitor_idx]
        elif isinstance(state_monitor.record, slice):
            # This is a bit more complex if slice has a step.
            # Assuming step is 1 for simplicity here.
            original_idx = (state_monitor.record.start or 0) + monitor_idx * (state_monitor.record.step or 1)

        ax.plot(times / time_unit, voltages[monitor_idx, :] / voltage_unit,
                label=f"Neuron {original_idx}", alpha=alpha)

    ax.set_title(title)
    ax.set_xlabel(xlabel if xlabel is not None else f"Time ({time_unit!s})")
    ax.set_ylabel(ylabel if ylabel is not None else f"Vm ({voltage_unit!s})")

    if legend_loc and len(plot_indices_in_monitor) > 0:
        ax.legend(loc=legend_loc)

    ax.grid(True, linestyle=':', alpha=0.7)
    return ax
