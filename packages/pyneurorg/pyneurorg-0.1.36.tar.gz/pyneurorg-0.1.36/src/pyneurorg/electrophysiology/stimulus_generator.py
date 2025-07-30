# src/pyneurorg/electrophysiology/stimulus_generator.py

"""
Functions for generating various time-varying stimulus waveforms for pyneurorg
simulations, typically returned as Brian2 TimedArray objects.

These waveforms are intended to be used as input currents to NeuronGroup objects.
All generated TimedArrays will have their values in Amperes.
"""

import numpy as np
import brian2 as b2
from brian2.units.fundamentalunits import DIMENSIONLESS # For checking dimensionless quantities

def create_pulse_train(amplitude, frequency, pulse_width, duration, dt, 
                       delay_start=0*b2.ms, name=None):
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
    name : str, optional
        A name for the created TimedArray object (default: None).

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

    # Convert to numerical SI base units for calculation
    amplitude_A = float(amplitude / b2.amp)
    frequency_Hz = float(frequency / b2.Hz)
    pulse_width_s = float(pulse_width / b2.second)
    duration_s = float(duration / b2.second)
    dt_s = float(dt / b2.second)
    delay_start_s = float(delay_start / b2.second)

    if frequency_Hz > 0 and pulse_width_s >= (1.0 / frequency_Hz):
        raise ValueError("pulse_width must be less than the inter-pulse interval (1/frequency).")
    if delay_start_s < 0:
        raise ValueError("delay_start cannot be negative.")
    if duration_s <= 0: # If total duration is zero or less, return an empty or minimal array
        return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt, name=name)
    if dt_s <= 0:
        raise ValueError("dt must be positive.")

    total_time_points = int(round(duration_s / dt_s))
    # Ensure at least one point if duration is very small but positive
    if total_time_points == 0 and duration_s > 0: total_time_points = 1 
    if total_time_points == 0: # Still zero, means duration_s was effectively zero for this dt
        return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt, name=name)

    waveform_np_A = np.zeros(total_time_points) # Values will be in Amperes

    current_time_s = delay_start_s
    period_s = (1.0 / frequency_Hz) if frequency_Hz > 1e-9 else (duration_s + dt_s) # Avoid division by zero for freq=0

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
        
        if frequency_Hz <= 1e-9: # Effectively a single pulse if frequency is zero or very small
            break 
        current_time_s += period_s
        # Check if the *start* of the next pulse would be beyond or exactly at the duration
        if current_time_s >= duration_s - 1e-9: # Add small epsilon for float comparison
            break
            
    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt, name=name)


def create_current_step(amplitude, onset, offset, total_duration, dt, name=None):
    """
    Generates a Brian2 TimedArray representing a single rectangular current step.
    Values in the TimedArray are in Amperes.
    """
    if not isinstance(amplitude, b2.Quantity) or amplitude.dimensions != b2.amp.dimensions:
        raise ValueError("amplitude must be a Brian2 Quantity with current dimensions.")
    for q, var_name in [(onset, "onset"), (offset, "offset"), 
                        (total_duration, "total_duration"), (dt, "dt")]:
        if not isinstance(q, b2.Quantity) or q.dimensions != b2.second.dimensions:
            raise ValueError(f"{var_name} must be a Brian2 Quantity with time dimensions.")

    onset_s = float(onset / b2.second)
    offset_s = float(offset / b2.second)
    total_duration_s = float(total_duration / b2.second)
    dt_s = float(dt / b2.second)
    amplitude_A = float(amplitude / b2.amp)

    if offset_s <= onset_s:
        raise ValueError("offset must be greater than onset.")
    if total_duration_s <= 0:
        return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt, name=name)
    if dt_s <= 0:
        raise ValueError("dt must be positive.")

    total_time_points = int(round(total_duration_s / dt_s))
    if total_time_points == 0 and total_duration_s > 0: total_time_points = 1
    if total_time_points == 0: return b2.TimedArray(np.array([0.0]) * b2.amp, dt=dt, name=name)
    
    waveform_np_A = np.zeros(total_time_points)

    onset_idx = int(round(onset_s / dt_s))
    offset_idx = int(round(offset_s / dt_s))

    actual_start_idx = max(0, onset_idx)
    actual_end_idx = min(total_time_points, offset_idx)

    if actual_start_idx < actual_end_idx:
        waveform_np_A[actual_start_idx:actual_end_idx] = amplitude_A
        
    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt, name=name)


def create_ramp_current(start_amplitude, end_amplitude, duration, dt, 
                        delay_start=0*b2.ms, name=None):
    """
    Generates a Brian2 TimedArray representing a linearly ramping current.
    The total length of the TimedArray will be delay_start + duration.
    Values in the TimedArray are in Amperes.
    """
    for q, var_name, dim in [(start_amplitude, "start_amplitude", b2.amp.dimensions),
                             (end_amplitude, "end_amplitude", b2.amp.dimensions),
                             (duration, "duration", b2.second.dimensions),
                             (dt, "dt", b2.second.dimensions),
                             (delay_start, "delay_start", b2.second.dimensions)]:
        if not isinstance(q, b2.Quantity) or q.dimensions != dim:
            raise ValueError(f"{var_name} must be a Brian2 Quantity with appropriate dimensions ({dim}).")

    start_amplitude_A = float(start_amplitude / b2.amp)
    end_amplitude_A = float(end_amplitude / b2.amp)
    duration_s = float(duration / b2.second)
    dt_s = float(dt / b2.second)
    delay_start_s = float(delay_start / b2.second)

    if duration_s <= 0: raise ValueError("duration must be positive.")
    if delay_start_s < 0: raise ValueError("delay_start cannot be negative.")
    if dt_s <= 0: raise ValueError("dt must be positive.")

    total_waveform_duration_s = delay_start_s + duration_s
    total_time_points = int(round(total_waveform_duration_s / dt_s))
    if total_time_points == 0 and total_waveform_duration_s > 0: total_time_points = 1
    # If total duration is 0 (e.g. delay=0, duration effectively 0 for this dt)
    if total_time_points == 0: 
        return b2.TimedArray(np.array([start_amplitude_A]) * b2.amp, dt=dt, name=name) if delay_start_s == 0 and duration_s == 0 else b2.TimedArray(np.array([]) * b2.amp, dt=dt, name=name)

    waveform_np_A = np.zeros(total_time_points)
    
    delay_points_idx = int(round(delay_start_s / dt_s))
    if delay_points_idx > 0:
        waveform_np_A[:delay_points_idx] = start_amplitude_A # Hold start_amplitude during delay

    ramp_duration_points = int(round(duration_s / dt_s))
    if ramp_duration_points == 0 and duration_s > 0 : ramp_duration_points = 1
    
    if ramp_duration_points > 0:
        ramp_values = np.linspace(start_amplitude_A, end_amplitude_A, ramp_duration_points)
        
        actual_ramp_start_idx_in_waveform = delay_points_idx
        num_ramp_points_to_assign = min(ramp_duration_points, total_time_points - actual_ramp_start_idx_in_waveform)

        if num_ramp_points_to_assign > 0:
            waveform_np_A[actual_ramp_start_idx_in_waveform : actual_ramp_start_idx_in_waveform + num_ramp_points_to_assign] = \
                ramp_values[:num_ramp_points_to_assign]
            
            # If ramp was cut short by total_waveform_duration, or if ramp finished before end of array
            if actual_ramp_start_idx_in_waveform + num_ramp_points_to_assign < total_time_points:
                waveform_np_A[actual_ramp_start_idx_in_waveform + num_ramp_points_to_assign:] = end_amplitude_A
    elif delay_points_idx < total_time_points: # No ramp duration, but there's space after delay
        waveform_np_A[delay_points_idx:] = start_amplitude_A # Hold at start_amplitude

    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt, name=name)


def create_sinusoidal_current(amplitude, frequency, phase, duration, dt, 
                              delay_start=0*b2.ms, offset_current=0*b2.nA, name=None):
    """
    Generates a Brian2 TimedArray representing a sinusoidal current.
    I(t) = offset_current + amplitude * sin(2*pi*frequency*(t_eff) + phase)
    where t_eff is time relative to the start of the sinusoidal part.
    Values in the TimedArray are in Amperes.
    """
    for q, var_name, dim in [(amplitude, "amplitude", b2.amp.dimensions),
                             (frequency, "frequency", b2.Hz.dimensions),
                             (duration, "duration", b2.second.dimensions),
                             (dt, "dt", b2.second.dimensions),
                             (delay_start, "delay_start", b2.second.dimensions),
                             (offset_current, "offset_current", b2.amp.dimensions)]:
        if not isinstance(q, b2.Quantity) or q.dimensions != dim:
            raise ValueError(f"{var_name} must be a Brian2 Quantity with appropriate dimensions ({dim}).")
    if isinstance(phase, b2.Quantity):
        if phase.dimensions != DIMENSIONLESS:
            raise ValueError("phase must be a dimensionless Quantity (radians) or a float.")
        phase_val_rad = float(phase)
    elif isinstance(phase, (int, float)):
        phase_val_rad = float(phase)
    else:
        raise TypeError("phase must be a number or a dimensionless Brian2 Quantity.")

    amplitude_A = float(amplitude / b2.amp)
    frequency_Hz = float(frequency / b2.Hz)
    duration_s = float(duration / b2.second)
    dt_s = float(dt / b2.second)
    delay_start_s = float(delay_start / b2.second)
    offset_current_A = float(offset_current / b2.amp)

    if duration_s <= 0: raise ValueError("duration must be positive.")
    if delay_start_s < 0: raise ValueError("delay_start cannot be negative.")
    if dt_s <= 0: raise ValueError("dt must be positive.")

    total_waveform_duration_s = delay_start_s + duration_s
    total_time_points = int(round(total_waveform_duration_s / dt_s))
    if total_time_points == 0 and total_waveform_duration_s > 0: total_time_points = 1
    if total_time_points == 0:
        return b2.TimedArray(np.array([offset_current_A]) * b2.amp, dt=dt, name=name) if delay_start_s == 0 and duration_s == 0 else b2.TimedArray(np.array([]) * b2.amp, dt=dt, name=name)

    waveform_np_A = np.full(total_time_points, offset_current_A) # Initialize with offset

    num_sinusoid_points = int(round(duration_s / dt_s))
    if num_sinusoid_points == 0 and duration_s > 0: num_sinusoid_points = 1
    
    if num_sinusoid_points > 0:
        t_sinusoid_part_s = np.arange(num_sinusoid_points) * dt_s # Time vector for the sine wave itself
        omega_rad_s = 2 * np.pi * frequency_Hz
        sinusoid_values = amplitude_A * np.sin(omega_rad_s * t_sinusoid_part_s + phase_val_rad)
        
        delay_points_idx = int(round(delay_start_s / dt_s))
        
        actual_sinusoid_start_idx_in_waveform = delay_points_idx
        num_points_to_assign = min(num_sinusoid_points, total_time_points - actual_sinusoid_start_idx_in_waveform)

        if num_points_to_assign > 0:
            waveform_np_A[actual_sinusoid_start_idx_in_waveform : actual_sinusoid_start_idx_in_waveform + num_points_to_assign] += \
                sinusoid_values[:num_points_to_assign] # Add sinusoidal part to the offset
            
    return b2.TimedArray(waveform_np_A * b2.amp, dt=dt, name=name)


def create_custom_waveform(times, values, dt, name=None):
    """
    Generates a Brian2 TimedArray from custom time and value points.
    Linearly interpolates. Output current is in Amperes.
    """
    if not isinstance(dt, b2.Quantity) or dt.dimensions != b2.second.dimensions:
        raise ValueError("dt must be a Brian2 Quantity with time dimensions.")
    if float(dt/b2.second) <=0:
        raise ValueError("dt must be positive.")
    if not isinstance(times, (list, tuple, np.ndarray, b2.Quantity)):
        raise TypeError("'times' must be Quantity or array-like (assumed seconds).")
    if not isinstance(values, (list, tuple, np.ndarray, b2.Quantity)):
        raise TypeError("'values' must be Quantity or array-like (assumed Amperes).")

    if isinstance(times, b2.Quantity):
        if times.dimensions != b2.second.dimensions: raise ValueError("'times' Quantity must have time dims.")
        t_np_sec = np.atleast_1d(np.asarray(times / b2.second, dtype=float))
    else: t_np_sec = np.atleast_1d(np.asarray(times, dtype=float))

    if isinstance(values, b2.Quantity):
        if values.dimensions != b2.amp.dimensions: raise ValueError("'values' Quantity must have current dims.")
        v_np_amp = np.atleast_1d(np.asarray(values / b2.amp, dtype=float))
    else: v_np_amp = np.atleast_1d(np.asarray(values, dtype=float))

    if len(t_np_sec) != len(v_np_amp): raise ValueError("times and values must have the same length.")
    if len(t_np_sec) == 0: return b2.TimedArray(np.array([]) * b2.amp, dt=dt, name=name)
    if np.any(np.diff(t_np_sec) < 0): raise ValueError("Time points in `times` must be non-decreasing.")

    max_time_sec = t_np_sec[-1]
    if max_time_sec < 0: max_time_sec = 0 # Ensure duration is not negative if all times are <=0

    num_output_points = int(np.floor(max_time_sec / float(dt/b2.second))) + 1
    if num_output_points <= 0 : num_output_points = 1 
    output_times_sec = np.linspace(0, (num_output_points - 1) * float(dt/b2.second), num_output_points, endpoint=True)
    
    if len(t_np_sec) == 1:
        interpolated_values_amp = np.full_like(output_times_sec, v_np_amp[0])
        # Value is v_np_amp[0] for output_times_sec >= t_np_sec[0]
        # and also for output_times_sec < t_np_sec[0] due to np.interp default left fill.
        # This makes it constant from t=0 if t_np_sec[0] is also 0.
        # If t_np_sec[0] > 0, it will be v_np_amp[0] from t=0 up to t_np_sec[0], then continues.
        # A more step-like behavior for a single point (t1, v1) would be:
        # val = 0 for t < t1; val = v1 for t >= t1. np.interp doesn't do this by default.
        # For simplicity, np.interp's behavior is used.
        interpolated_values_amp = np.interp(output_times_sec, t_np_sec, v_np_amp,
                                            left=v_np_amp[0] if t_np_sec[0] == 0 else 0.0, # Value before first time point
                                            right=v_np_amp[-1]) # Value after last time point
    else:
        # np.interp requires xp to be increasing. Handle non-strictly increasing cases by unique.
        unique_t, unique_indices = np.unique(t_np_sec, return_index=True)
        unique_v = v_np_amp[unique_indices]
        if len(unique_t) < 2 and len(unique_t) == 1 : # Effectively one unique time point
             interpolated_values_amp = np.full_like(output_times_sec, unique_v[0])
             interpolated_values_amp[output_times_sec < unique_t[0]] = 0.0 # If time point is not 0
        elif len(unique_t) < 2 and len(unique_t) == 0: # Should not happen due to earlier check
             interpolated_values_amp = np.zeros_like(output_times_sec)
        else:
             interpolated_values_amp = np.interp(output_times_sec, unique_t, unique_v,
                                                 left=unique_v[0] if unique_t[0] == 0 else 0.0,
                                                 right=unique_v[-1])
            
    return b2.TimedArray(interpolated_values_amp * b2.amp, dt=dt, name=name)