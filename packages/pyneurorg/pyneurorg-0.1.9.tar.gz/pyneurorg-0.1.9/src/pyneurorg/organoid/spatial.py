# pyneurorg/organoid/spatial.py

"""
Functions for generating and manipulating spatial coordinates of neurons
within a pybrainorg organoid.

All coordinate and size inputs are either Brian2 Quantities with length
dimensions or are assumed to be in micrometers (um) if provided as raw numbers.
All outputs representing coordinates or distances are Brian2 Quantities in um.
"""

import numpy as np
import brian2 as b2
from brian2.units.fundamentalunits import DIMENSIONLESS

def _ensure_um_quantity(value, name="value"):
    """Converts a value to a Brian2 Quantity in micrometers (um)."""
    if isinstance(value, b2.Quantity):
        if value.dimensions == b2.metre.dimensions:
            return value.in_units(b2.um) # Convert to um
        else:
            raise TypeError(f"{name} must be a Brian2 Quantity with length dimensions or a number (assumed um).")
    elif isinstance(value, (int, float, np.number)):
        return value * b2.um # Assume um if raw number
    else:
        raise TypeError(f"{name} must be a Brian2 Quantity with length dimensions or a number (assumed um).")

def _ensure_um_tuple(value_tuple, name="value_tuple"):
    """Converts a 3-tuple to Brian2 Quantities in um."""
    if not (isinstance(value_tuple, (tuple, list)) and len(value_tuple) == 3):
        raise TypeError(f"{name} must be a 3-tuple of numbers (assumed um) or Brian2 Quantities with length.")
    return tuple(_ensure_um_quantity(v, f"{name}_component") for v in value_tuple)


def random_positions_in_cube(N, side_length=100, center=(0,0,0)):
    """
    Generates N random 3D positions uniformly distributed within a cube.

    Parameters are assumed to be in micrometers (um) if raw numbers.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    side_length : float or brian2.units.fundamentalunits.Quantity, optional
        The length of each side of the cube. If a number, assumed um.
        (default: 100, interpreted as 100 um).
    center : tuple of float or tuple of brian2.units.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the cube.
        If numbers, assumed um. (default: (0,0,0), interpreted as (0,0,0) um).

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, 3) Quantity array where each row is (x, y, z) coordinates
        in micrometers (um).
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")

    side_length_um = _ensure_um_quantity(side_length, "side_length")
    center_um = _ensure_um_tuple(center, "center")

    side_length_val = float(side_length_um / b2.um)
    center_val = np.array([float(c / b2.um) for c in center_um])

    # Generate random numbers between -0.5 and +0.5, then scale
    positions_val = (np.random.rand(N, 3) - 0.5) * side_length_val

    # Shift by center
    positions_val += center_val

    return positions_val * b2.um


def random_positions_in_sphere(N, radius=100, center=(0,0,0)):
    """
    Generates N random 3D positions uniformly distributed within a sphere.

    Parameters are assumed to be in micrometers (um) if raw numbers.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    radius : float or brian2.units.fundamentalunits.Quantity, optional
        The radius of the sphere. If a number, assumed um. (default: 100).
    center : tuple of float or tuple of brian2.units.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the sphere.
        If numbers, assumed um. (default: (0,0,0)).

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, 3) Quantity array with coordinates in micrometers (um).
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")

    radius_um = _ensure_um_quantity(radius, "radius")
    center_um = _ensure_um_tuple(center, "center")

    radius_val = float(radius_um / b2.um)
    center_val = np.array([float(c / b2.um) for c in center_um])
    positions_val = np.zeros((N, 3))
    count = 0

    while count < N:
        x, y, z = (np.random.rand(3) * 2 - 1) * radius_val
        if x**2 + y**2 + z**2 <= radius_val**2:
            positions_val[count, :] = [x, y, z]
            count += 1
    
    positions_val += center_val
    return positions_val * b2.um


def random_positions_on_sphere_surface(N, radius=100, center=(0,0,0)):
    """
    Generates N random 3D positions uniformly distributed on the surface of a sphere.

    Parameters are assumed to be in micrometers (um) if raw numbers.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    radius : float or brian2.units.fundamentalunits.Quantity, optional
        The radius of the sphere. If a number, assumed um. (default: 100).
    center : tuple of float or tuple of brian2.units.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the sphere.
        If numbers, assumed um. (default: (0,0,0)).

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, 3) Quantity array with coordinates in micrometers (um).
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")

    radius_um = _ensure_um_quantity(radius, "radius")
    center_um = _ensure_um_tuple(center, "center")
    
    radius_val = float(radius_um / b2.um)
    center_val = np.array([float(c / b2.um) for c in center_um])

    gauss_points = np.random.normal(size=(N, 3))
    norm = np.linalg.norm(gauss_points, axis=1, keepdims=True)
    norm[norm == 0] = 1
    unit_sphere_points = gauss_points / norm
    positions_val = unit_sphere_points * radius_val
    positions_val += center_val

    return positions_val * b2.um


def _extract_value_in_um(quantity_or_array, name="value"):
    """
    Helper to get the numerical value of a length quantity in micrometers.
    If input is a raw number, it's assumed to be in um.
    If input is a Brian2 Quantity with length dimensions, it's converted to um.
    """
    if isinstance(quantity_or_array, b2.Quantity):
        if quantity_or_array.dimensions == b2.metre.dimensions:
            return np.asarray(quantity_or_array / b2.um) # Value in um
        else:
            raise TypeError(f"{name} must be a Brian2 Quantity with length dimensions or a number (assumed um).")
    elif isinstance(quantity_or_array, (int, float, np.number, np.ndarray)):
        return np.asarray(quantity_or_array) # Assume um
    else:
        raise TypeError(f"{name} must be a Brian2 Quantity with length dimensions, a number, or a NumPy array (assumed um).")


def distance_matrix(positions1, positions2=None):
    """
    Calculates the Euclidean distance matrix between two sets of 3D points.

    Inputs are assumed to be in micrometers (um) if raw numbers, or are
    converted to um if Brian2 Quantities with length dimensions.
    The output distance matrix will be a Brian2 Quantity in um.

    Parameters
    ----------
    positions1 : array-like or brian2.units.fundamentalunits.Quantity
        A (N, 3) array of N points.
    positions2 : array-like or brian2.units.fundamentalunits.Quantity, optional
        A (M, 3) array of M points. If None, calculates the distance
        matrix for `positions1` with itself.

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, M) distance matrix in micrometers (um).

    Raises
    ------
    ValueError
        If input arrays do not have 3 columns.
    TypeError
        If inputs are not of expected types or have incompatible dimensions.
    """
    p1_val_um = _extract_value_in_um(positions1, "positions1")
    if p1_val_um.ndim != 2 or p1_val_um.shape[1] != 3:
        raise ValueError("positions1 must be an N x 3 array.")

    if positions2 is None:
        p2_val_um = p1_val_um
    else:
        p2_val_um = _extract_value_in_um(positions2, "positions2")
        if p2_val_um.ndim != 2 or p2_val_um.shape[1] != 3:
            raise ValueError("positions2 must be an M x 3 array.")

    try:
        from scipy.spatial.distance import cdist
        dist_val_um = cdist(p1_val_um, p2_val_um, metric='euclidean')
    except ImportError:
        p1_sq_sum = np.sum(p1_val_um**2, axis=1, keepdims=True)
        p2_sq_sum = np.sum(p2_val_um**2, axis=1)
        dot_product = np.dot(p1_val_um, p2_val_um.T)
        dist_sq_val = p1_sq_sum + p2_sq_sum - 2 * dot_product
        dist_sq_val[dist_sq_val < 0] = 0
        dist_val_um = np.sqrt(dist_sq_val)

    return dist_val_um * b2.um
