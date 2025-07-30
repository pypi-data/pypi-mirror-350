# src/pyneurorg/electrophysiology/stimulus_generator.py

"""
Functions for generating various time-varying stimulus waveforms for pyneurorg
simulations, typically returned as Brian2 TimedArray objects.

These waveforms are intended to be used as input currents to NeuronGroup objects.
"""

import numpy as np
import brian2 as b2

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
        Must be less than 1/frequency.
    duration : brian2.units.fundamentalunits.Quantity
        The total duration of the stimulus waveform (e.g., 100*b2.ms).
    dt : brian2.units.fundamentalunits.Quantity
        The time step for discretizing the TimedArray (e.g., 0.1*b2.ms).
    delay_start : brian2.units.fundamentalunits.Quantity, optional
        An initial delay before the first pulse starts (default: 0*b2.ms).

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the pulse train.

    Raises
    ------
    ValueError
        If pulse_width >= 1/frequency or if parameters have incorrect dimensions.
    """
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

    if frequency > 0*b2.Hz and pulse_width >= (1 / frequency):
        raise ValueError("pulse_width must be less than the inter-pulse interval (1/frequency).")
    if delay_start < 0*b2.ms:
        raise ValueError("delay_start cannot be negative.")
    if duration <= 0*b2.ms:
        return b2.TimedArray(np.array([0]) * amplitude.unit, dt=dt) # Return empty or zero array

    total_time_points = int(round(float(duration / dt)))
    time_array_np = np.arange(total_time_points) * float(dt) # Time in seconds (Brian2 base unit)
    waveform_np = np.zeros(total_time_points) * float(amplitude) # Value in Amps

    current_time = float(delay_start)
    period = float(1/frequency) if frequency > 0*b2.Hz else float(duration) + float(dt) # Avoid division by zero

    while current_time < float(duration):
        pulse_start_idx = int(round(current_time / float(dt)))
        pulse_end_time = current_time + float(pulse_width)
        pulse_end_idx = int(round(pulse_end_time / float(dt)))

        # Apply pulse if it's within the total duration
        actual_start_idx = max(0, pulse_start_idx)
        actual_end_idx = min(total_time_points, pulse_end_idx)
        
        if actual_start_idx < actual_end_idx:
            waveform_np[actual_start_idx:actual_end_idx] = float(amplitude)
        
        if frequency <= 0*b2.Hz: # Single pulse case
            break
        current_time += period
        if current_time >= float(duration): # Ensure we don't schedule beyond duration
            break
            
    return b2.TimedArray(waveform_np, dt=dt)


def create_current_step(amplitude, onset, offset, total_duration, dt):
    """
    Generates a Brian2 TimedArray representing a single rectangular current step.

    Parameters
    ----------
    amplitude : brian2.units.fundamentalunits.Quantity
        The amplitude of the current step (e.g., 0.5*b2.nA).
    onset : brian2.units.fundamentalunits.Quantity
        The time at which the current step begins (e.g., 10*b2.ms).
    offset : brian2.units.fundamentalunits.Quantity
        The time at which the current step ends (e.g., 60*b2.ms).
        Must be greater than onset.
    total_duration : brian2.units.fundamentalunits.Quantity
        The total duration of the stimulus waveform (e.g., 100*b2.ms).
        The TimedArray will have this length.
    dt : brian2.units.fundamentalunits.Quantity
        The time step for discretizing the TimedArray (e.g., 0.1*b2.ms).

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the current step.

    Raises
    ------
    ValueError
        If offset <= onset or if parameters have incorrect dimensions.
    """
    if not isinstance(amplitude, b2.Quantity) or amplitude.dimensions != b2.amp.dimensions:
        raise ValueError("amplitude must be a Brian2 Quantity with current dimensions.")
    if not isinstance(onset, b2.Quantity) or onset.dimensions != b2.second.dimensions:
        raise ValueError("onset must be a Brian2 Quantity with time dimensions.")
    if not isinstance(offset, b2.Quantity) or offset.dimensions != b2.second.dimensions:
        raise ValueError("offset must be a Brian2 Quantity with time dimensions.")
    if not isinstance(total_duration, b2.Quantity) or total_duration.dimensions != b2.second.dimensions:
        raise ValueError("total_duration must be a Brian2 Quantity with time dimensions.")
    if not isinstance(dt, b2.Quantity) or dt.dimensions != b2.second.dimensions:
        raise ValueError("dt must be a Brian2 Quantity with time dimensions.")

    if offset <= onset:
        raise ValueError("offset must be greater than onset.")
    if total_duration <= 0*b2.ms:
        return b2.TimedArray(np.array([0]) * amplitude.unit, dt=dt)

    total_time_points = int(round(float(total_duration / dt)))
    waveform_np = np.zeros(total_time_points) * float(amplitude) # Value in Amps

    onset_idx = int(round(float(onset / dt)))
    offset_idx = int(round(float(offset / dt)))

    actual_start_idx = max(0, onset_idx)
    actual_end_idx = min(total_time_points, offset_idx)

    if actual_start_idx < actual_end_idx:
        waveform_np[actual_start_idx:actual_end_idx] = float(amplitude)
        
    return b2.TimedArray(waveform_np, dt=dt)


def create_ramp_current(start_amplitude, end_amplitude, duration, dt, delay_start=0*b2.ms):
    """
    Generates a Brian2 TimedArray representing a linearly ramping current.

    Parameters
    ----------
    start_amplitude : brian2.units.fundamentalunits.Quantity
        The current amplitude at the beginning of the ramp.
    end_amplitude : brian2.units.fundamentalunits.Quantity
        The current amplitude at the end of the ramp.
    duration : brian2.units.fundamentalunits.Quantity
        The total duration of the ramp itself (excluding delay_start).
    dt : brian2.units.fundamentalunits.Quantity
        The time step for discretizing the TimedArray.
    delay_start : brian2.units.fundamentalunits.Quantity, optional
        An initial delay before the ramp starts (default: 0*b2.ms).
        The total length of the TimedArray will be delay_start + duration.

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the ramp current.
    """
    # Parameter validation
    for q, name, dim in [(start_amplitude, "start_amplitude", b2.amp.dimensions),
                         (end_amplitude, "end_amplitude", b2.amp.dimensions),
                         (duration, "duration", b2.second.dimensions),
                         (dt, "dt", b2.second.dimensions),
                         (delay_start, "delay_start", b2.second.dimensions)]:
        if not isinstance(q, b2.Quantity) or q.dimensions != dim:
            raise ValueError(f"{name} must be a Brian2 Quantity with appropriate dimensions ({dim}).")
    if duration <= 0*b2.ms:
        raise ValueError("duration must be positive.")
    if delay_start < 0*b2.ms:
        raise ValueError("delay_start cannot be negative.")

    total_waveform_duration = delay_start + duration
    total_time_points = int(round(float(total_waveform_duration / dt)))
    
    # Time array for the entire waveform (including delay)
    time_values_for_array = np.arange(total_time_points) * float(dt) # seconds
    waveform_np = np.zeros(total_time_points) * float(start_amplitude) # Amps

    # Time points for the ramp segment itself
    ramp_start_time_sec = float(delay_start)
    ramp_end_time_sec = float(delay_start + duration)
    
    # Indices for the ramp segment
    ramp_start_idx = int(round(ramp_start_time_sec / float(dt)))
    ramp_end_idx = int(round(ramp_end_time_sec / float(dt))) # Exclusive end for linspace
    
    num_ramp_points = ramp_end_idx - ramp_start_idx

    if num_ramp_points > 0:
        ramp_values = np.linspace(float(start_amplitude), float(end_amplitude), num_ramp_points)
        
        # Ensure indices are within bounds of waveform_np
        actual_start = min(ramp_start_idx, total_time_points)
        actual_end = min(ramp_end_idx, total_time_points)
        
        if actual_start < actual_end:
            # Adjust ramp_values if the ramp segment is clipped by total_waveform_duration
            len_to_assign = actual_end - actual_start
            waveform_np[actual_start:actual_end] = ramp_values[:len_to_assign]
            
    return b2.TimedArray(waveform_np, dt=dt)


def create_sinusoidal_current(amplitude, frequency, phase, duration, dt, delay_start=0*b2.ms, offset_current=0*b2.nA):
    """
    Generates a Brian2 TimedArray representing a sinusoidal current.
    I(t) = offset_current + amplitude * sin(2*pi*frequency*t + phase)

    Parameters
    ----------
    amplitude : brian2.units.fundamentalunits.Quantity
        The peak amplitude of the sinusoidal oscillation (around the offset).
    frequency : brian2.units.fundamentalunits.Quantity
        The frequency of the oscillation (e.g., 10*b2.Hz).
    phase : float or brian2.units.fundamentalunits.Quantity
        The phase offset in radians (e.g., 0, np.pi/2). If a Quantity, must be dimensionless.
    duration : brian2.units.fundamentalunits.Quantity
        The total duration of the sinusoidal waveform (excluding delay_start).
    dt : brian2.units.fundamentalunits.Quantity
        The time step for discretizing the TimedArray.
    delay_start : brian2.units.fundamentalunits.Quantity, optional
        An initial delay before the sinusoid starts (default: 0*b2.ms).
        The total length of the TimedArray will be delay_start + duration.
    offset_current : brian2.units.fundamentalunits.Quantity, optional
        A DC offset for the sinusoidal current (default: 0*b2.nA).

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the sinusoidal current.
    """
    # Parameter validation
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
            raise ValueError("phase must be a dimensionless Quantity (e.g., representing radians) or a float.")
        phase_val = float(phase)
    elif isinstance(phase, (int, float)):
        phase_val = float(phase)
    else:
        raise TypeError("phase must be a number or a dimensionless Brian2 Quantity.")

    if duration <= 0*b2.ms:
        raise ValueError("duration must be positive.")
    if delay_start < 0*b2.ms:
        raise ValueError("delay_start cannot be negative.")

    total_waveform_duration = delay_start + duration
    total_time_points = int(round(float(total_waveform_duration / dt)))
    
    # Time array relative to the start of the sinusoid itself (after delay_start)
    # for calculating the sine wave part.
    sinusoid_time_points = int(round(float(duration / dt)))
    t_sinusoid_sec = np.arange(sinusoid_time_points) * float(dt) # seconds

    # Calculate sinusoidal part
    omega = 2 * np.pi * float(frequency) # angular frequency in rad/s
    sinusoid_values = float(amplitude) * np.sin(omega * t_sinusoid_sec + phase_val) + float(offset_current) # Amps

    # Create the full waveform including delay
    waveform_np = np.zeros(total_time_points) * float(amplitude) # Initialize with Amps unit base
    waveform_np += float(offset_current) # Apply DC offset to the whole waveform initially (if delay exists)

    delay_points = int(round(float(delay_start / dt)))
    
    # Place the sinusoid part after the delay
    # Ensure indices are within bounds
    actual_sinusoid_start_idx = delay_points
    num_sinusoid_points_to_assign = min(sinusoid_time_points, total_time_points - actual_sinusoid_start_idx)

    if num_sinusoid_points_to_assign > 0:
        waveform_np[actual_sinusoid_start_idx : actual_sinusoid_start_idx + num_sinusoid_points_to_assign] = \
            sinusoid_values[:num_sinusoid_points_to_assign]
            
    return b2.TimedArray(waveform_np, dt=dt)


def create_custom_waveform(times, values, dt):
    """
    Generates a Brian2 TimedArray from custom time and value points.

    Linearly interpolates between the provided (time, value) pairs to fill
    the TimedArray at the specified `dt`. The TimedArray will span from
    time 0 up to the maximum time in `times`.

    Parameters
    ----------
    times : array-like of float or brian2.units.fundamentalunits.Quantity
        An array of time points for the custom waveform. Must be sorted.
        If a Quantity, must have time dimensions. If numbers, assumed `dt` units.
    values : array-like of float or brian2.units.fundamentalunits.Quantity
        An array of current values corresponding to each time point in `times`.
        Must have the same length as `times`. If a Quantity, must have current
        dimensions. If numbers, assumed `ampere` base units.
    dt : brian2.units.fundamentalunits.Quantity
        The time step for the resulting TimedArray.

    Returns
    -------
    brian2.input.timedarray.TimedArray
        A TimedArray representing the custom waveform.

    Raises
    ------
    ValueError
        If `times` and `values` have different lengths, `times` is not sorted,
        or parameters have incorrect dimensions/types.
    """
    if not isinstance(dt, b2.Quantity) or dt.dimensions != b2.second.dimensions:
        raise ValueError("dt must be a Brian2 Quantity with time dimensions.")
    if len(times) != len(values):
        raise ValueError("times and values must have the same length.")
    if len(times) == 0:
        return b2.TimedArray(np.array([]) * b2.amp, dt=dt) # Empty TimedArray

    # Process times
    if isinstance(times, b2.Quantity):
        if times.dimensions != b2.second.dimensions:
            raise ValueError("times must have time dimensions if a Quantity.")
        t_np = np.asarray(times / dt) # Convert to multiples of dt
    elif isinstance(times, (np.ndarray, list)):
        t_np = np.asarray(times) # Assume already scaled appropriately for dt (e.g. if times are in ms, dt is in ms)
    else:
        raise TypeError("times must be a Brian2 Quantity or array-like.")

    # Process values
    val_unit = b2.amp # Default unit if values are raw numbers
    if isinstance(values, b2.Quantity):
        if values.dimensions != b2.amp.dimensions:
            raise ValueError("values must have current dimensions if a Quantity.")
        v_np = np.asarray(values / val_unit) # Convert to numerical values in base unit Amp
        val_unit = values.unit # Preserve the original unit if possible for the TimedArray
    elif isinstance(values, (np.ndarray, list)):
        v_np = np.asarray(values) # Assume base unit Amp
    else:
        raise TypeError("values must be a Brian2 Quantity or array-like.")

    # Check if times are sorted
    if not np.all(np.diff(t_np) >= 0):
        raise ValueError("times must be sorted in non-decreasing order.")

    # Determine the total duration and number of points for the TimedArray
    # Times are now numerical, scaled by dt (e.g., if times were [0*ms, 10*ms, 20*ms] and dt=1*ms, t_np=[0,10,20])
    # This interpretation was incorrect. t_np should be the actual time values, not scaled by dt yet.
    
    # Re-process times and values to be numerical in base SI units
    if isinstance(times, b2.Quantity): t_np_sec = np.asarray(times / b2.second)
    else: t_np_sec = np.asarray(times) # Assume seconds if raw array for times

    if isinstance(values, b2.Quantity): v_np_amp = np.asarray(values / b2.amp)
    else: v_np_amp = np.asarray(values) # Assume amperes if raw array for values
    
    if not np.all(np.diff(t_np_sec) >= 0):
         raise ValueError("Time points in `times` must be sorted and non-decreasing.")

    if len(t_np_sec) == 0:
        return b2.TimedArray(np.array([]) * b2.amp, dt=dt)

    total_duration_sec = t_np_sec[-1]
    if total_duration_sec < float(dt): # Ensure at least one dt point if there's any duration
        total_duration_sec = float(dt)
        
    num_output_points = int(round(total_duration_sec / float(dt)))
    if num_output_points == 0 and len(t_np_sec) > 0 : # Ensure at least one point if input had data
        num_output_points = 1
    elif num_output_points == 0 and len(t_np_sec) == 0:
        return b2.TimedArray(np.array([]) * b2.amp, dt=dt)


    output_times_sec = np.arange(num_output_points) * float(dt)
    
    # Interpolate
    # np.interp needs x-coordinates of data points (t_np_sec) to be increasing.
    if len(t_np_sec) == 1: # Single point, constant value
        interpolated_values_amp = np.full(num_output_points, v_np_amp[0])
    else:
        interpolated_values_amp = np.interp(output_times_sec, t_np_sec, v_np_amp)
        
    return b2.TimedArray(interpolated_values_amp * b2.amp, dt=dt)