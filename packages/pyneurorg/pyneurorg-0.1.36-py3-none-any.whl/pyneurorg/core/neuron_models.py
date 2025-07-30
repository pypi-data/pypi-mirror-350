# src/pyneurorg/core/neuron_models.py

"""
Collection of predefined neuron models for use with Brian2 in pyneurorg simulations.

Each function in this module returns a dictionary containing the necessary
components (equations, parameters, threshold, reset conditions, refractory period,
and integration method) to define a `brian2.NeuronGroup`.

All models include 'I_synaptic : amp' and 'I_stimulus_sum : amp' to allow for
separate inputs from synaptic connections and external stimuli (like MEA).
They also include boolean flags 'is_targeted_by_stimX : boolean' for targeted stimulation.
"""

import brian2 as b2

# Helper function to generate flag equations and namespace entries
def _add_stimulus_flags_and_currents(base_eqs, base_namespace, num_stimulus_flags=16):
    """
    Appends stimulus summation current and boolean flags to model equations
    and corresponding default initializers to the namespace.
    """
    stim_eqs_parts = [
        "I_stimulus_sum : amp # Sum of all external timed stimuli for this neuron"
    ]
    
    flag_eqs_list = []
    default_flags_init = {}
    for i in range(num_stimulus_flags):
        flag_name = f"is_targeted_by_stim{i}"
        flag_eqs_list.append(f"{flag_name} : boolean")
        default_flags_init[f"{flag_name}_default_init"] = False 

    # I_synaptic is assumed to be driven by Synapses objects
    # I_stimulus_sum will be driven by Simulator.add_stimulus via run_regularly
    # I_tonic_val is a parameter for intrinsic drive
    # We need a way to combine these. Let's assume a total current variable if not already present.
    
    # Check if a total current summation variable (like I_total_input or I_summed) is already in base_eqs.
    # If not, we might need to assume one or add it.
    # For simplicity, let's assume the base models will now use I_stimulus_sum and I_synaptic
    # in conjunction with I_tonic_val.

    full_eqs = base_eqs + "\n" + "\n".join(stim_eqs_parts) + "\n" + "\n".join(flag_eqs_list)
    
    # Add default initializers for the new current terms if not already in base_namespace
    # (NeuronGroup will default them to 0*amp and False if not set, but good for clarity)
    updated_namespace = base_namespace.copy()
    if 'I_stimulus_sum_default_init' not in updated_namespace:
        updated_namespace['I_stimulus_sum_default_init'] = 0*b2.amp
    if 'I_synaptic_default_init' not in updated_namespace: # Assuming models will also have I_synaptic
        updated_namespace['I_synaptic_default_init'] = 0*b2.amp
        if "I_synaptic : amp" not in full_eqs: # Add I_synaptic if not in base_eqs
             full_eqs = "I_synaptic : amp # For synaptic currents\n" + full_eqs


    updated_namespace.update(default_flags_init)
    
    return full_eqs, updated_namespace


def LIFNeuron(tau_m=10*b2.ms, v_rest=0*b2.mV, v_reset=0*b2.mV,
              v_thresh=20*b2.mV, R_m=100*b2.Mohm, I_tonic=0*b2.nA,
              refractory_period=2*b2.ms, num_stimulus_flags=16):
    """
    Defines a Leaky Integrate-and-Fire (LIF) neuron model with stimulus capabilities.
    Includes I_synaptic, I_stimulus_sum, and boolean flags for targeted stimuli.
    """
    # Base LIF equations, now using I_total which will include I_stimulus_sum
    base_eqs = """
    dv/dt = (-(v - v_rest_val) + R_m_val * (I_synaptic + I_stimulus_sum + I_tonic_val)) / tau_m_val : volt (unless refractory)
    I_input_placeholder : amp # Original I_input, now effectively replaced by I_synaptic + I_stimulus_sum
    """
    # Note: I_input_placeholder is kept for backward compatibility if old code used it,
    # but new stimuli should target I_stimulus_sum and synapses I_synaptic.
    # For cleaner models, one might remove I_input_placeholder and directly use I_synaptic & I_stimulus_sum.
    # Let's make it cleaner:
    base_eqs_clean = """
    dv/dt = (-(v - v_rest_val) + R_m_val * (I_synaptic + I_stimulus_sum + I_tonic_val)) / tau_m_val : volt (unless refractory)
    """

    base_namespace = {
        'tau_m_val': tau_m,
        'v_rest_val': v_rest,
        'R_m_val': R_m,
        'I_tonic_val': I_tonic,
        'v_default_init': v_rest, # Default initial value for v
    }

    full_eqs, full_namespace = _add_stimulus_flags_and_currents(
        base_eqs_clean, base_namespace, num_stimulus_flags
    )

    return {
        'model': full_eqs,
        'threshold': f'v > {v_thresh!r}',
        'reset': f'v = {v_reset!r}',
        'refractory': refractory_period,
        'namespace': full_namespace,
        'method': 'exact'
    }


def IzhikevichNeuron(a=0.02/b2.ms, b=0.2*b2.nS, c=-65*b2.mV, d=2*b2.pA,
                     v_init=-70*b2.mV, u_init=None, C_m=100*b2.pF,
                     k=0.7*b2.nS/b2.mV, v_rest_iz=-60*b2.mV, v_thresh_iz=-40*b2.mV,
                     v_peak=30*b2.mV, I_tonic=0*b2.pA, num_stimulus_flags=16):
    """
    Defines an Izhikevich neuron model with stimulus capabilities.
    """
    if u_init is None:
        u_init_val = b * (v_init - v_rest_iz)
    else:
        u_init_val = u_init

    # Original I_input is now split into I_synaptic + I_stimulus_sum
    base_eqs = """
    dv/dt = (k_val * (v - v_rest_iz_val) * (v - v_thresh_iz_val) - u + I_synaptic + I_stimulus_sum + I_tonic_val) / C_m_val : volt
    du/dt = a_val * (b_val * (v - v_rest_iz_val) - u) : amp / second
    """
    base_namespace = {
        'a_val': a, 'b_val': b, 'k_val': k, 'C_m_val': C_m,
        'v_rest_iz_val': v_rest_iz, 'v_thresh_iz_val': v_thresh_iz,
        'I_tonic_val': I_tonic,
        'v_default_init': v_init,
        'u_default_init': u_init_val,
    }
    
    full_eqs, full_namespace = _add_stimulus_flags_and_currents(
        base_eqs, base_namespace, num_stimulus_flags
    )

    return {
        'model': full_eqs,
        'threshold': f'v >= {v_peak!r}',
        'reset': f'v = {c!r}; u += {d!r}', # d needs to be Quantity with current units
        'namespace': full_namespace,
        'method': 'euler'
    }


def AdExNeuron(C_m=281*b2.pF, g_L=30*b2.nS, E_L=-70.6*b2.mV,
               V_T=-50.4*b2.mV, Delta_T=2*b2.mV, tau_w=144*b2.ms,
               a=4*b2.nS, adex_b_param=0.0805*b2.nA, V_reset=-70.6*b2.mV, # Renamed 'b' to 'adex_b_param'
               V_peak=0*b2.mV, I_tonic=0*b2.nA, refractory_period=0*b2.ms,
               num_stimulus_flags=16):
    """
    Defines an Adaptive Exponential Integrate-and-Fire (AdEx) neuron model with stimulus capabilities.
    Parameter 'b' from original model is 'adex_b_param' here to avoid conflict.
    """
    # Original I_input is now split
    base_eqs = """
    dv/dt = (g_L_val * (E_L_val - v) + g_L_val * Delta_T_val * exp((v - V_T_val)/Delta_T_val) - w + I_synaptic + I_stimulus_sum + I_tonic_val) / C_m_val : volt (unless refractory)
    dw/dt = (a_val * (v - E_L_val) - w) / tau_w_val : amp (unless refractory)
    """
    base_namespace = {
        'C_m_val': C_m, 'g_L_val': g_L, 'E_L_val': E_L, 'V_T_val': V_T,
        'Delta_T_val': Delta_T, 'tau_w_val': tau_w, 'a_val': a,
        'I_tonic_val': I_tonic,
        'v_default_init': E_L,
        'w_default_init': 0*b2.nA, # Or a_val * (E_L_val - E_L_val)
    }

    full_eqs, full_namespace = _add_stimulus_flags_and_currents(
        base_eqs, base_namespace, num_stimulus_flags
    )

    return {
        'model': full_eqs,
        'threshold': f'v > {V_peak!r}',
        'reset': f'v = {V_reset!r}; w += {adex_b_param!r}', # Use adex_b_param
        'refractory': refractory_period,
        'namespace': full_namespace,
        'method': 'euler'
    }


def QIFNeuron(tau_m=20*b2.ms, v_rest=0*b2.mV, v_c=10*b2.mV,
              v_reset=-10*b2.mV, v_peak=30*b2.mV, R_m=100*b2.Mohm,
              I_tonic=0*b2.nA, refractory_period=1*b2.ms, num_stimulus_flags=16):
    """
    Defines a Quadratic Integrate-and-Fire (QIF) neuron model with stimulus capabilities.
    """
    # Original I_input is now split
    base_eqs = """
    dv/dt = ( (v - v_rest_val) * (v - v_critical_val) / (1*volt) + R_m_val * (I_synaptic + I_stimulus_sum + I_tonic_val) ) / tau_m_val : volt (unless refractory)
    """
    base_namespace = {
        'tau_m_val': tau_m, 'v_rest_val': v_rest, 'v_critical_val': v_c,
        'R_m_val': R_m, 'I_tonic_val': I_tonic,
        'v_default_init': v_rest,
    }
    
    full_eqs, full_namespace = _add_stimulus_flags_and_currents(
        base_eqs, base_namespace, num_stimulus_flags
    )

    return {
        'model': full_eqs,
        'threshold': f'v >= {v_peak!r}',
        'reset': f'v = {v_reset!r}',
        'refractory': refractory_period,
        'namespace': full_namespace,
        'method': 'euler'
    }


def SimpleHHNeuron(C_m=1*b2.uF/b2.cm**2, E_Na=50*b2.mV, E_K=-77*b2.mV, E_L=-54.4*b2.mV,
                   g_Na_bar=120*b2.mS/b2.cm**2, g_K_bar=36*b2.mS/b2.cm**2, g_L_bar=0.3*b2.mS/b2.cm**2,
                   V_T_hh=-60*b2.mV, I_tonic=0*b2.uA/b2.cm**2, refractory_period=0*b2.ms,
                   num_stimulus_flags=16):
    """
    Defines a simplified Hodgkin-Huxley (HH) type neuron model with stimulus capabilities.
    Currents are per unit area. I_synaptic and I_stimulus_sum should also be provided as A/m^2.
    """
    numerical_spike_threshold = 0*b2.mV

    # Original I_input is now split and needs to be current density
    base_eqs = """
    # Membrane potential (I_synaptic, I_stimulus_sum, I_tonic_val are current densities A/m^2)
    dv/dt = (I_Na + I_K + I_L + I_synaptic + I_stimulus_sum + I_tonic_val) / C_m_val : volt (unless refractory)

    # Sodium current
    I_Na = g_Na_bar_val * m**3 * h * (E_Na_val - v) : amp/meter**2
    dm/dt = alpha_m * (1-m) - beta_m * m : 1
    dh/dt = alpha_h * (1-h) - beta_h * h : 1
    alpha_m = (0.1/mV) * (v - (V_T_hh_val + 25*mV)) / (1 - exp(-(v - (V_T_hh_val + 25*mV))/(10*mV))) / ms : Hz
    beta_m = (4.0) * exp(-(v - (V_T_hh_val + 0*mV))/(18*mV)) / ms : Hz
    alpha_h = (0.07) * exp(-(v - (V_T_hh_val + 0*mV))/(20*mV)) / ms : Hz
    beta_h = (1.0) / (1 + exp(-(v - (V_T_hh_val + 30*mV))/(10*mV))) / ms : Hz

    # Potassium current
    I_K = g_K_bar_val * n**4 * (E_K_val - v) : amp/meter**2
    dn/dt = alpha_n * (1-n) - beta_n * n : 1
    alpha_n = (0.01/mV) * (v - (V_T_hh_val + 10*mV)) / (1 - exp(-(v - (V_T_hh_val + 10*mV))/(10*mV))) / ms : Hz
    beta_n = (0.125) * exp(-(v - (V_T_hh_val + 0*mV))/(80*mV)) / ms : Hz

    # Leak current
    I_L = g_L_bar_val * (E_L_val - v) : amp/meter**2
    """
    base_namespace = {
        'C_m_val': C_m, 'E_Na_val': E_Na, 'E_K_val': E_K, 'E_L_val': E_L,
        'g_Na_bar_val': g_Na_bar, 'g_K_bar_val': g_K_bar, 'g_L_bar_val': g_L_bar,
        'V_T_hh_val': V_T_hh, 'I_tonic_val': I_tonic, # I_tonic is current density
        'v_default_init': E_L,
        'm_default_init': 0.05, 'h_default_init': 0.6, 'n_default_init': 0.32,
    }

    full_eqs, full_namespace = _add_stimulus_flags_and_currents(
        base_eqs, base_namespace, num_stimulus_flags
    )
    # Ensure I_synaptic and I_stimulus_sum have correct units (A/m^2) if base_eqs use them
    # The _add_stimulus_flags_and_currents adds them as 'amp'.
    # For HH model, these need to be current densities.
    # We need to ensure their definitions in full_eqs have units of amp/meter**2
    # if they are added by _add_stimulus_flags_and_currents helper.

    # Let's redefine how helper adds these for HH to ensure correct units
    if "I_synaptic : amp" in full_eqs: # If helper added it with 'amp'
        full_eqs = full_eqs.replace("I_synaptic : amp", "I_synaptic : amp/meter**2")
        full_namespace['I_synaptic_default_init'] = 0*b2.uA/b2.cm**2 # Default to current density
    if "I_stimulus_sum : amp" in full_eqs:
        full_eqs = full_eqs.replace("I_stimulus_sum : amp", "I_stimulus_sum : amp/meter**2")
        full_namespace['I_stimulus_sum_default_init'] = 0*b2.uA/b2.cm**2


    return {
        'model': full_eqs,
        'threshold': f'v > {numerical_spike_threshold!r}',
        'reset': '', 
        'refractory': refractory_period,
        'namespace': full_namespace,
        'method': ('exponential_euler', {'simplify': True, 'split_వ': True})
    }