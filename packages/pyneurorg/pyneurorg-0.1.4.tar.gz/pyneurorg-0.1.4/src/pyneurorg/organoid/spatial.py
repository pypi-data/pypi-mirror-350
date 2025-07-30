# pyneurorg/organoid/spatial.py

"""
Functions for generating and manipulating spatial coordinates of neurons
within a pybrainorg organoid.

These functions typically return NumPy arrays of coordinates, which can then
be assigned to `brian2.NeuronGroup` objects. Brian2 units are used where
appropriate for physical dimensions.
"""

import numpy as np
import brian2 as b2
from brian2.units.fundamentalunits import DIMENSIONLESS # For checking dimensionless quantities

def random_positions_in_cube(N, side_length=100*b2.um, center=(0,0,0)*b2.um):
    """
    Generates N random 3D positions uniformly distributed within a cube.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    side_length : brian2.units.fundamentalunits.Quantity, optional
        The length of each side of the cube (default: 100 um).
    center : tuple of brian2.units.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the cube
        (default: (0,0,0) um).

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, 3) Quantity array where each row is (x, y, z) coordinates
        of a point, with the unit derived from `side_length`.

    Examples
    --------
    >>> import brian2 as b2
    >>> from pybrainorg.organoid.spatial import random_positions_in_cube
    >>> positions = random_positions_in_cube(5, side_length=50*b2.um)
    >>> print(positions.shape)
    (5, 3)
    >>> print(positions.dimensions == b2.metre.dimensions) # Check dimensions
    True
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if not isinstance(side_length, b2.Quantity) or not (side_length.dimensions == b2.metre.dimensions):
        raise TypeError("side_length must be a Brian2 Quantity with length dimensions.")
    if not (isinstance(center, (tuple, list)) and len(center) == 3 and
            all(isinstance(c, b2.Quantity) and c.dimensions == b2.metre.dimensions for c in center)):
        raise TypeError("center must be a 3-tuple of Brian2 Quantities with length dimensions.")

    # Extract numerical value and unit for calculations
    side_length_val = float(side_length) # Value in base SI units
    unit_of_side_length = b2.Quantity(1.0, dimensions=side_length.dimensions).get_best_unit().get_unit()

    # Generate random numbers between -0.5 and +0.5
    # Then scale by side_length_val
    positions_val = (np.random.rand(N, 3) - 0.5) * side_length_val

    # Shift by center values (also in base SI units)
    positions_val[:, 0] += float(center[0])
    positions_val[:, 1] += float(center[1])
    positions_val[:, 2] += float(center[2])

    return positions_val * unit_of_side_length


def random_positions_in_sphere(N, radius=100*b2.um, center=(0,0,0)*b2.um):
    """
    Generates N random 3D positions uniformly distributed within a sphere.

    Uses a rejection sampling method. For very large N, more direct methods
    are more efficient.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    radius : brian2.units.fundamentalunits.Quantity, optional
        The radius of the sphere (default: 100 um).
    center : tuple of brian2.units.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the sphere
        (default: (0,0,0) um).

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, 3) Quantity array with the unit derived from `radius`.
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if not isinstance(radius, b2.Quantity) or not (radius.dimensions == b2.metre.dimensions):
        raise TypeError("radius must be a Brian2 Quantity with length dimensions.")
    if not (isinstance(center, (tuple, list)) and len(center) == 3 and
            all(isinstance(c, b2.Quantity) and c.dimensions == b2.metre.dimensions for c in center)):
        raise TypeError("center must be a 3-tuple of Brian2 Quantities with length dimensions.")

    radius_val = float(radius) # Value in base SI units
    unit_of_radius = b2.Quantity(1.0, dimensions=radius.dimensions).get_best_unit().get_unit()
    positions_val = np.zeros((N, 3))
    count = 0

    center_val = np.array([float(c) for c in center])

    while count < N:
        x, y, z = (np.random.rand(3) * 2 - 1) * radius_val # Point in bounding cube
        if x**2 + y**2 + z**2 <= radius_val**2:
            positions_val[count, :] = [x, y, z]
            count += 1

    # Shift by center
    positions_val += center_val # Broadcasting adds center to each row

    return positions_val * unit_of_radius


def random_positions_on_sphere_surface(N, radius=100*b2.um, center=(0,0,0)*b2.um):
    """
    Generates N random 3D positions uniformly distributed on the surface of a sphere.

    Uses the method of generating Gaussian-distributed coordinates and normalizing.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    radius : brian2.units.fundamentalunits.Quantity, optional
        The radius of the sphere (default: 100 um).
    center : tuple of brian2.units.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the sphere
        (default: (0,0,0) um).

    Returns
    -------
    brian2.units.fundamentalunits.Quantity
        A (N, 3) Quantity array with the unit derived from `radius`.
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if not isinstance(radius, b2.Quantity) or not (radius.dimensions == b2.metre.dimensions):
        raise TypeError("radius must be a Brian2 Quantity with length dimensions.")
    if not (isinstance(center, (tuple, list)) and len(center) == 3 and
            all(isinstance(c, b2.Quantity) and c.dimensions == b2.metre.dimensions for c in center)):
        raise TypeError("center must be a 3-tuple of Brian2 Quantities with length dimensions.")

    radius_val = float(radius) # Value in base SI units
    unit_of_radius = b2.Quantity(1.0, dimensions=radius.dimensions).get_best_unit().get_unit()
    center_val = np.array([float(c) for c in center])

    gauss_points = np.random.normal(size=(N, 3))
    norm = np.linalg.norm(gauss_points, axis=1, keepdims=True)
    norm[norm == 0] = 1 # Avoid division by zero
    unit_sphere_points = gauss_points / norm
    positions_val = unit_sphere_points * radius_val
    positions_val += center_val

    return positions_val * unit_of_radius


def distance_matrix(positions1, positions2=None):
    """
    Calculates the Euclidean distance matrix between two sets of 3D points.

    Parameters
    ----------
    positions1 : brian2.units.fundamentalunits.Quantity or np.ndarray
        A (N, 3) array of N points. If a Brian2 Quantity, must have length dimensions.
        If a NumPy array, units are assumed consistent or dimensionless.
    positions2 : brian2.units.fundamentalunits.Quantity or np.ndarray, optional
        A (M, 3) array of M points. If None, calculates the distance
        matrix for `positions1` with itself. Same unit rules as `positions1`.

    Returns
    -------
    brian2.units.fundamentalunits.Quantity or np.ndarray
        A (N, M) distance matrix. If inputs were Brian2 Quantities with length
        dimensions, the output will also be a Quantity with the same length unit.
        Otherwise, a NumPy array.

    Raises
    ------
    ValueError
        If input arrays do not have 3 columns or if units are incompatible.
    TypeError
        If inputs are not of expected types (Quantity or ndarray).
    """
    p1_val_num, p1_unit_obj = _extract_value_and_unit(positions1, b2.metre.dimensions)
    if p1_val_num.ndim != 2 or p1_val_num.shape[1] != 3:
        raise ValueError("positions1 must be an N x 3 array.")

    if positions2 is None:
        p2_val_num, p2_unit_obj = p1_val_num, p1_unit_obj
    else:
        p2_val_num, p2_unit_obj = _extract_value_and_unit(positions2, b2.metre.dimensions)
        if p2_val_num.ndim != 2 or p2_val_num.shape[1] != 3:
            raise ValueError("positions2 must be an M x 3 array.")

        # Check for unit consistency if both had units
        if p1_unit_obj is not None and p2_unit_obj is not None and p1_unit_obj != p2_unit_obj:
            # This check is simplified; proper unit conversion might be desired
            # For now, require them to be effectively the same for simplicity if both are Quantities.
            # Brian2 Quantities would handle this if we operated on them directly,
            # but for cdist, we pass numerical values.
            # A more robust check would compare their values in a common base unit.
            # However, _extract_value_and_unit already gives us the "best unit"
            # If they were different (e.g. um and mm), they would have different unit_obj.
            raise ValueError("positions1 and positions2 must have compatible length units if both are Brian2 Quantities.")
        elif p1_unit_obj is None and p2_unit_obj is not None:
            p1_unit_obj = p2_unit_obj # Inherit unit for result if p1 was raw
        # If p2_unit_obj is None and p1_unit_obj is not None, result will have p1_unit_obj.
        # If both are None, result is unitless numpy array.

    try:
        from scipy.spatial.distance import cdist
        dist_val = cdist(p1_val_num, p2_val_num, metric='euclidean')
    except ImportError:
        # Fallback manual calculation
        p1_sq_sum = np.sum(p1_val_num**2, axis=1, keepdims=True)
        p2_sq_sum = np.sum(p2_val_num**2, axis=1)
        dot_product = np.dot(p1_val_num, p2_val_num.T)
        dist_sq_val = p1_sq_sum + p2_sq_sum - 2 * dot_product
        dist_sq_val[dist_sq_val < 0] = 0 # Correct for precision errors leading to small negatives
        dist_val = np.sqrt(dist_sq_val)

    if p1_unit_obj is not None:
        return dist_val * p1_unit_obj
    else:
        return dist_val


def _extract_value_and_unit(quantity_or_array, expected_dimensions=DIMENSIONLESS):
    """
    Helper to extract numerical value and best unit from a Brian2 Quantity or NumPy array.

    If it's a Quantity, checks dimensions.
    If it's a NumPy array, unit is None.
    Returns numerical value (in base SI units if it was a Quantity) and the best_unit object.
    """
    if isinstance(quantity_or_array, b2.Quantity):
        if quantity_or_array.dimensions != expected_dimensions:
            raise TypeError(f"Input Quantity has dimensions {quantity_or_array.dimensions}, "
                            f"expected {expected_dimensions}.")
        # Get value in base SI units for consistent calculations
        value = float(quantity_or_array) # This gets the value in base SI units for non-dimensionless
        if expected_dimensions == DIMENSIONLESS: # For dimensionless, float() might be just the number
             value = np.array(quantity_or_array) # Keep as array if dimensionless
        else: # For dimensionful quantities, get value in base SI for calculation
             value_in_current_unit = np.array(quantity_or_array / b2.Quantity(1.0, dimensions=quantity_or_array.dimensions).get_best_unit().get_unit())
             # Actually, simpler: Brian2 handles SI conversion. float(quantity) should be SI.
             # However, for arrays, we need to be careful.
             # Let's get the value in its current "best unit" to avoid large/small numbers in intermediate calcs,
             # then re-apply the best unit at the end.
             # No, better to work with SI internally for np, then convert back to best unit.
             # Simplest for np arrays: work with values in the original unit's scale, then re-apply unit.
             # This is what float(quantity_array) would do if it were a scalar.
             # For an array:
             val_array = np.array(quantity_or_array) # Numerical part in current unit
             unit_object = b2.Quantity(1.0, dimensions=quantity_or_array.dimensions).get_best_unit().get_unit()
             return val_array, unit_object # Return numerical array and its unit object

        # Re-think: for calculations, we need the numerical part.
        # The unit will be re-applied at the end.
        # float(b2.Quantity) gives scalar in SI.
        # np.array(b2.Quantity) gives array of numbers in current display unit.
        
        val_array = np.asarray(quantity_or_array) # Gets the numerical part in current units
        unit_object = b2.Quantity(1.0, dimensions=quantity_or_array.dimensions).get_best_unit().get_unit()
        return val_array, unit_object

    elif isinstance(quantity_or_array, np.ndarray):
        if expected_dimensions != DIMENSIONLESS:
            # If we expect units but get a raw array, it's ambiguous.
            # For distance_matrix, if one input has units, we assume the raw array is compatible.
            # For functions creating positions, they always return Quantities.
            pass # Assume compatible for now, unit will be None
        return quantity_or_array, None
    else:
        raise TypeError("Input must be a Brian2 Quantity or a NumPy array.")
