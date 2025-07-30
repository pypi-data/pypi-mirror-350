# src/pyneurorg/electrophysiology/stimulus_generator.py

"""
Functions for generating various time-varying stimulus waveforms for pyneurorg
simulations, typically returned as Brian2 TimedArray objects.

These waveforms are intended to be used as input currents to NeuronGroup objects.
"""

import numpy as np
import brian2 as b2
from brian2.units.fundamentalunits import DIMENSIONLESS # For checking dimensionless quantities

def create_pulse_train(amplitude, frequency, pulse_width, duration, dt, delay_start=0*b2.ms):
    """
    Generates a Brian2 TimedArray representing a train of rectangular current pulses.

    Parameters
    ----------
    amplitude : brian2.units.fundamentalunits.Quantity
        The amplitude of each current pulse (e.g., 1*b2.nA).
    frequency : brian2.units.fundamentalunits.Quantity
        The frequency of the pulses (e.g., 10*b2.Hz). This determines the
        inter-pulse interval (1/frequency).
    pulse_width : brian2.units.fundamentalunits.Quantity
        The duration of each individual pulse (e.g., 2*b2.ms).
        Must be less than 1/frequency if frequency > 0.
    duration : brian2.units.fundamentalunits.Quantity
        The total duration of the stimulus waveform to be generated (e.g., 100*b2.ms).
        This defines the length of the output TimedArray. Pulses will only be
        generated up to this duration.
    dt : brian2.units.fundamentalunits.Quantity
        The time step for discretizing the TimedArray (e.g., 0.1*b2.ms).
    delay_start : brian2.units.fundamentalunits.Quantity, optional
        An initial delay before the first pulse starts (default: 0*b2.ms).

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the pulse train, with values in Amperes.

    Raises
    ------
    ValueError
        If pulse_width >= 1/frequency (for frequency > 0), if parameters have
        incorrect dimensions, or if essential durations are non-positive.
    """
    # Parameter validation
    if not isinstance(amplitude, b2.Quantity) or amplitude.dimensions != b2.amp.dimensions:
        raise ValueError("amplitude must be a Brian2 Quantity with current dimensions (e.g., b2.nA).")
    if not isinstance(frequency, b2.Quantity) or frequency.dimensions != b2.Hz.dimensions:
        raise ValueError("frequency must be a Brian2 Quantity with frequency dimensions (e.g., b2.Hz).")
    if not isinstance(pulse_width, b2.Quantity) or pulse_width.dimensions != b2.second.dimensions:
        raise ValueError("pulse_width must be a Brian2 Quantity with time dimensions (e.g., b2.ms).")
    if not isinstance(duration, b2.Quantity) or duration.dimensions != b2.second.dimensions:
        raise ValueError("duration must be a Brian2 Quantity with time dimensions (e.g., b2.ms).")
    if not isinstance(dt, b2.Quantity) or dt.dimensions != b2.second.dimensions:
        raise ValueError("dt must be a Brian2 Quantity with time dimensions (e.g., b2.ms).")
    if not isinstance(delay_start, b2.Quantity) or delay_start.dimensions != b2.second.dimensions:
        raise ValueError("delay_start must be a Brian2 Quantity with time dimensions (e.g., b2.ms).")

    if float(frequency / b2.Hz) > 0 and float(pulse_width / b2.second) >= float(1.0 / (frequency / b2.Hz)):
        raise ValueError("pulse_width must be less than the inter-pulse interval (1/frequency).")
    if float(delay_start / b2.second) < 0:
        raise ValueError("delay_start cannot be negative.")
    if float(duration / b2.second) <= 0:
        return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt) # Return empty or zero array if duration is zero/negative
    if float(dt / b2.second) <= 0:
        raise ValueError("dt must be positive.")

    # Convert all to SI base units for calculation
    amplitude_A = float(amplitude / b2.amp)
    frequency_Hz = float(frequency / b2.Hz)
    pulse_width_s = float(pulse_width / b2.second)
    duration_s = float(duration / b2.second)
    dt_s = float(dt / b2.second)
    delay_start_s = float(delay_start / b2.second)

    total_time_points = int(round(duration_s / dt_s))
    if total_time_points == 0 and duration_s > 0: total_time_points = 1 # Ensure at least one point if duration > 0
    if total_time_points == 0: return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt)

    waveform_np_A = np.zeros(total_time_points) # Values in Amperes

    current_time_s = delay_start_s
    period_s = (1.0 / frequency_Hz) if frequency_Hz > 0 else (duration_s + dt_s) # Avoid division by zero

    while current_time_s < duration_s:
        pulse_actual_start_time_s = current_time_s
        pulse_actual_end_time_s = current_time_s + pulse_width_s

        # Determine indices for this pulse within the total waveform
        idx_start = int(round(pulse_actual_start_time_s / dt_s))
        idx_end = int(round(pulse_actual_end_time_s / dt_s)) # Exclusive end for slicing

        # Clip indices to the bounds of the waveform array
        idx_start_clipped = max(0, idx_start)
        idx_end_clipped = min(total_time_points, idx_end)
        
        if idx_start_clipped < idx_end_clipped: # If any part of the pulse is within the duration
            waveform_np_A[idx_start_clipped:idx_end_clipped] = amplitude_A
        
        if frequency_Hz <= 0: # Single pulse case
            break 
        current_time_s += period_s
        # Check if the *start* of the next pulse would be beyond the duration
        if current_time_s >= duration_s:
            break
            
    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt)


def create_current_step(amplitude, onset, offset, total_duration, dt):
    """
    Generates a Brian2 TimedArray representing a single rectangular current step.

    Parameters
    ----------
    amplitude : brian2.units.fundamentalunits.Quantity
        The amplitude of the current step.
    onset : brian2.units.fundamentalunits.Quantity
        The time at which the current step begins.
    offset : brian2.units.fundamentalunits.Quantity
        The time at which the current step ends. Must be greater than onset.
    total_duration : brian2.units.fundamentalunits.Quantity
        The total duration of the stimulus waveform. The TimedArray will have this length.
    dt : brian2.units.fundamentalunits.Quantity
        The time step for discretizing the TimedArray.

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the current step, with values in Amperes.
    """
    # Parameter validation (as in create_pulse_train for similar types)
    if not isinstance(amplitude, b2.Quantity) or amplitude.dimensions != b2.amp.dimensions:
        raise ValueError("amplitude must be a Brian2 Quantity with current dimensions.")
    for q, name in [(onset, "onset"), (offset, "offset"), 
                    (total_duration, "total_duration"), (dt, "dt")]:
        if not isinstance(q, b2.Quantity) or q.dimensions != b2.second.dimensions:
            raise ValueError(f"{name} must be a Brian2 Quantity with time dimensions.")

    if float(offset / b2.second) <= float(onset / b2.second):
        raise ValueError("offset must be greater than onset.")
    if float(total_duration / b2.second) <= 0:
        return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt)
    if float(dt / b2.second) <= 0:
        raise ValueError("dt must be positive.")

    # Convert to SI base units
    amplitude_A = float(amplitude / b2.amp)
    onset_s = float(onset / b2.second)
    offset_s = float(offset / b2.second)
    total_duration_s = float(total_duration / b2.second)
    dt_s = float(dt / b2.second)

    total_time_points = int(round(total_duration_s / dt_s))
    if total_time_points == 0 and total_duration_s > 0: total_time_points = 1
    if total_time_points == 0: return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt)
    
    waveform_np_A = np.zeros(total_time_points)

    onset_idx = int(round(onset_s / dt_s))
    offset_idx = int(round(offset_s / dt_s))

    actual_start_idx = max(0, onset_idx)
    actual_end_idx = min(total_time_points, offset_idx)

    if actual_start_idx < actual_end_idx:
        waveform_np_A[actual_start_idx:actual_end_idx] = amplitude_A
        
    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt)


def create_ramp_current(start_amplitude, end_amplitude, duration, dt, delay_start=0*b2.ms):
    """
    Generates a Brian2 TimedArray representing a linearly ramping current.
    The total length of the TimedArray will be delay_start + duration.

    Parameters
    ----------
    start_amplitude : brian2.units.fundamentalunits.Quantity
        Current amplitude at the beginning of the ramp.
    end_amplitude : brian2.units.fundamentalunits.Quantity
        Current amplitude at the end of the ramp.
    duration : brian2.units.fundamentalunits.Quantity
        Duration of the ramp itself (excluding delay_start).
    dt : brian2.units.fundamentalunits.Quantity
        Time step for the TimedArray.
    delay_start : brian2.units.fundamentalunits.Quantity, optional
        Initial delay before the ramp starts (default: 0*b2.ms).

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray for the ramp current, values in Amperes.
    """
    for q, name, dim in [(start_amplitude, "start_amplitude", b2.amp.dimensions),
                         (end_amplitude, "end_amplitude", b2.amp.dimensions),
                         (duration, "duration", b2.second.dimensions),
                         (dt, "dt", b2.second.dimensions),
                         (delay_start, "delay_start", b2.second.dimensions)]:
        if not isinstance(q, b2.Quantity) or q.dimensions != dim:
            raise ValueError(f"{name} must be a Brian2 Quantity with appropriate dimensions ({dim}).")
    if float(duration / b2.second) <= 0:
        raise ValueError("duration must be positive.")
    if float(delay_start / b2.second) < 0:
        raise ValueError("delay_start cannot be negative.")
    if float(dt / b2.second) <= 0:
        raise ValueError("dt must be positive.")

    start_amplitude_A = float(start_amplitude / b2.amp)
    end_amplitude_A = float(end_amplitude / b2.amp)
    duration_s = float(duration / b2.second)
    dt_s = float(dt / b2.second)
    delay_start_s = float(delay_start / b2.second)

    total_waveform_duration_s = delay_start_s + duration_s
    total_time_points = int(round(total_waveform_duration_s / dt_s))
    if total_time_points == 0 and total_waveform_duration_s > 0: total_time_points = 1
    if total_time_points == 0: return b2.TimedArray(np.array([start_amplitude_A]) * b2.amp, dt=dt) if delay_start_s == 0 and duration_s == 0 else b2.TimedArray(np.array([]) * b2.amp, dt=dt)


    waveform_np_A = np.zeros(total_time_points)
    
    delay_points = int(round(delay_start_s / dt_s))
    if delay_points > 0: # Fill delay part if any
        waveform_np_A[:delay_points] = start_amplitude_A # Or 0, depending on desired behavior for delay

    ramp_duration_points = int(round(duration_s / dt_s))
    if ramp_duration_points == 0 and duration_s > 0 : ramp_duration_points = 1 # At least one point for the ramp if duration > 0
    
    if ramp_duration_points > 0:
        ramp_values = np.linspace(start_amplitude_A, end_amplitude_A, ramp_duration_points)
        
        # Place the ramp after the delay
        actual_ramp_start_idx_in_waveform = delay_points
        num_ramp_points_to_assign = min(ramp_duration_points, total_time_points - actual_ramp_start_idx_in_waveform)

        if num_ramp_points_to_assign > 0:
            waveform_np_A[actual_ramp_start_idx_in_waveform : actual_ramp_start_idx_in_waveform + num_ramp_points_to_assign] = \
                ramp_values[:num_ramp_points_to_assign]
            # If ramp was cut short by total_waveform_duration, fill remaining with end_amplitude
            if actual_ramp_start_idx_in_waveform + num_ramp_points_to_assign < total_time_points:
                waveform_np_A[actual_ramp_start_idx_in_waveform + num_ramp_points_to_assign:] = end_amplitude_A
    elif delay_points < total_time_points: # No ramp duration, but there's space after delay
        waveform_np_A[delay_points:] = start_amplitude_A # Hold at start_amplitude


    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt)


def create_sinusoidal_current(amplitude, frequency, phase, duration, dt, delay_start=0*b2.ms, offset_current=0*b2.nA):
    """
    Generates a Brian2 TimedArray representing a sinusoidal current.
    I(t) = offset_current + amplitude * sin(2*pi*frequency*(t-delay_start) + phase)
    The total length of the TimedArray will be delay_start + duration.

    Parameters
    ----------
    amplitude : brian2.units.fundamentalunits.Quantity
        Peak amplitude of the sinusoidal oscillation (around the offset).
    frequency : brian2.units.fundamentalunits.Quantity
        Frequency of the oscillation.
    phase : float or brian2.units.fundamentalunits.Quantity
        Phase offset in radians. If a Quantity, must be dimensionless.
    duration : brian2.units.fundamentalunits.Quantity
        Duration of the sinusoidal part itself (excluding delay_start).
    dt : brian2.units.fundamentalunits.Quantity
        Time step for the TimedArray.
    delay_start : brian2.units.fundamentalunits.Quantity, optional
        Initial delay before the sinusoid starts (default: 0*b2.ms).
    offset_current : brian2.units.fundamentalunits.Quantity, optional
        DC offset for the sinusoidal current (default: 0*b2.nA).

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray for the sinusoidal current, values in Amperes.
    """
    for q, name, dim in [(amplitude, "amplitude", b2.amp.dimensions),
                         (frequency, "frequency", b2.Hz.dimensions),
                         (duration, "duration", b2.second.dimensions),
                         (dt, "dt", b2.second.dimensions),
                         (delay_start, "delay_start", b2.second.dimensions),
                         (offset_current, "offset_current", b2.amp.dimensions)]:
        if not isinstance(q, b2.Quantity) or q.dimensions != dim:
            raise ValueError(f"{name} must be a Brian2 Quantity with appropriate dimensions ({dim}).")
    if isinstance(phase, b2.Quantity):
        if phase.dimensions != DIMENSIONLESS:
            raise ValueError("phase must be a dimensionless Quantity or a float.")
        phase_val_rad = float(phase)
    elif isinstance(phase, (int, float)):
        phase_val_rad = float(phase)
    else:
        raise TypeError("phase must be a number or a dimensionless Brian2 Quantity.")

    if float(duration / b2.second) <= 0: raise ValueError("duration must be positive.")
    if float(delay_start / b2.second) < 0: raise ValueError("delay_start cannot be negative.")
    if float(dt / b2.second) <= 0: raise ValueError("dt must be positive.")

    amplitude_A = float(amplitude / b2.amp)
    frequency_Hz = float(frequency / b2.Hz)
    duration_s = float(duration / b2.second)
    dt_s = float(dt / b2.second)
    delay_start_s = float(delay_start / b2.second)
    offset_current_A = float(offset_current / b2.amp)

    total_waveform_duration_s = delay_start_s + duration_s
    total_time_points = int(round(total_waveform_duration_s / dt_s))
    if total_time_points == 0 and total_waveform_duration_s > 0: total_time_points = 1
    if total_time_points == 0: return b2.TimedArray(np.array([offset_current_A]) * b2.amp, dt=dt) if delay_start_s == 0 and duration_s == 0 else b2.TimedArray(np.array([]) * b2.amp, dt=dt)

    waveform_np_A = np.full(total_time_points, offset_current_A) # Initialize with offset

    # Time vector for the sinusoidal part, starting from 0
    num_sinusoid_points = int(round(duration_s / dt_s))
    if num_sinusoid_points == 0 and duration_s > 0: num_sinusoid_points = 1
    
    if num_sinusoid_points > 0:
        t_sinusoid_part_s = np.arange(num_sinusoid_points) * dt_s
        omega_rad_s = 2 * np.pi * frequency_Hz
        sinusoid_values = amplitude_A * np.sin(omega_rad_s * t_sinusoid_part_s + phase_val_rad)
        
        delay_points_idx = int(round(delay_start_s / dt_s))
        
        # Place the sinusoid part (relative to offset) after the delay
        actual_sinusoid_start_idx_in_waveform = delay_points_idx
        num_points_to_assign = min(num_sinusoid_points, total_time_points - actual_sinusoid_start_idx_in_waveform)

        if num_points_to_assign > 0:
            waveform_np_A[actual_sinusoid_start_idx_in_waveform : actual_sinusoid_start_idx_in_waveform + num_points_to_assign] += \
                sinusoid_values[:num_points_to_assign] # Add to existing offset
            
    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt)


def create_custom_waveform(times, values, dt):
    """
    Generates a Brian2 TimedArray from custom time and value points.

    Linearly interpolates between the provided (time, value) pairs to fill
    the TimedArray at the specified `dt`. The TimedArray will span from
    time 0 up to the maximum time in `times`. Output current is in Amperes.

    Parameters
    ----------
    times : array-like of float or brian2.units.fundamentalunits.Quantity
        An array of time points for the custom waveform. Must be sorted non-decreasingly.
        If a Quantity, must have time dimensions. If numbers, assumed seconds.
    values : array-like of float or brian2.units.fundamentalunits.Quantity
        An array of current values corresponding to each time point in `times`.
        Must have the same length as `times`. If a Quantity, must have current
        dimensions. If numbers, assumed Amperes.
    dt : brian2.units.fundamentalunits.Quantity
        The time step for the resulting TimedArray.

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the custom waveform, with values in Amperes.
    """
    if not isinstance(dt, b2.Quantity) or dt.dimensions != b2.second.dimensions:
        raise ValueError("dt must be a Brian2 Quantity with time dimensions.")
    if float(dt/b2.second) <=0:
        raise ValueError("dt must be positive.")
        
    if not isinstance(times, (list, tuple, np.ndarray, b2.Quantity)):
        raise TypeError("'times' must be a Brian2 Quantity with time dimensions or an array-like of numbers (assumed seconds).")
    if not isinstance(values, (list, tuple, np.ndarray, b2.Quantity)):
        raise TypeError("'values' must be a Brian2 Quantity with current dimensions or an array-like of numbers (assumed Amperes).")

    # Convert times to a 1D NumPy array of seconds
    if isinstance(times, b2.Quantity):
        if times.dimensions != b2.second.dimensions:
            raise ValueError("'times' must have time dimensions if it's a Brian2 Quantity.")
        t_np_sec = np.atleast_1d(np.asarray(times / b2.second, dtype=float))
    else: # list, tuple, np.ndarray of numbers
        t_np_sec = np.atleast_1d(np.asarray(times, dtype=float))

    # Convert values to a 1D NumPy array of Amperes
    if isinstance(values, b2.Quantity):
        if values.dimensions != b2.amp.dimensions:
            raise ValueError("'values' must have current dimensions if it's a Brian2 Quantity.")
        v_np_amp = np.atleast_1d(np.asarray(values / b2.amp, dtype=float))
    else: # list, tuple, np.ndarray of numbers
        v_np_amp = np.atleast_1d(np.asarray(values, dtype=float))

    if len(t_np_sec) != len(v_np_amp):
        raise ValueError("times and values must have the same length.")
    if len(t_np_sec) == 0:
        return b2.TimedArray(np.array([]) * b2.amp, dt=dt)

    # Check if times are sorted (non-decreasingly)
    if np.any(np.diff(t_np_sec) < 0):
        raise ValueError("Time points in `times` must be sorted in non-decreasing order.")

    # Determine the duration and points for the output TimedArray
    # TimedArray starts at t=0 and goes up to the last time point in t_np_sec
    max_time_sec = t_np_sec[-1]
    
    # Ensure the array covers at least one dt, or up to max_time_sec
    num_output_points = int(np.floor(max_time_sec / float(dt/b2.second))) + 1
    if num_output_points <= 0: num_output_points = 1 # Ensure at least one point for interpolation

    output_times_sec = np.linspace(0, (num_output_points - 1) * float(dt/b2.second), num_output_points, endpoint=True)
    
    # Interpolate
    if len(t_np_sec) == 1: # Single (time, value) pair
        # Value is v_np_amp[0] for all output_times_sec >= t_np_sec[0]
        # Value is undefined or extrapolated for output_times_sec < t_np_sec[0]
        # np.interp with left=v_np_amp[0] (default) makes it constant from the start.
        interpolated_values_amp = np.interp(output_times_sec, t_np_sec, v_np_amp)
    else:
        # For np.interp, xp (t_np_sec) must be increasing.
        # If there are duplicate time points, np.interp uses the first occurrence.
        # This is okay for creating step-like changes if values at duplicate times differ.
        interpolated_values_amp = np.interp(output_times_sec, t_np_sec, v_np_amp)
            
    return b2.TimedArray(interpolated_values_amp * b2.amp, dt=dt)