# pyneurorg/organoid/spatial.py

"""
Functions for generating and manipulating spatial coordinates of neurons
within a pyneurorg organoid.

These functions typically return NumPy arrays of coordinates, which can then
be assigned to `brian2.NeuronGroup` objects. Brian2 units are used where
appropriate for physical dimensions.
"""

import numpy as np
import brian2 as b2

def random_positions_in_cube(N, side_length=100*b2.um, center=(0,0,0)*b2.um):
    """
    Generates N random 3D positions uniformly distributed within a cube.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    side_length : brian2.dimensionss.fundamentalunits.Quantity, optional
        The length of each side of the cube (default: 100 um).
    center : tuple of brian2.dimensionss.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the cube
        (default: (0,0,0) um).

    Returns
    -------
    brian2.dimensionss.fundamentalunits.Quantity
        A (N, 3) Quantity array where each row is (x, y, z) coordinates
        of a point, with the specified Brian2 length unit.

    Examples
    --------
    >>> import brian2 as b2
    >>> positions = random_positions_in_cube(5, side_length=50*b2.um)
    >>> print(positions.shape)
    (5, 3)
    >>> print(positions.dimensions)
    um
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if not hasattr(side_length, 'dimensions') or not side_length.has_same_dimensions(b2.meter):
        raise TypeError("side_length must be a Brian2 Quantity with length units.")
    if not (isinstance(center, (tuple, list)) and len(center) == 3 and
            all(hasattr(c, 'dimensions') and c.has_same_dimensions(b2.meter) for c in center)):
        raise TypeError("center must be a 3-tuple of Brian2 Quantities with length units.")

    half_side = side_length / 2.0
    unit = side_length.dimensions # Preserve the unit

    # Generate random numbers between -half_side and +half_side
    # np.random.rand(N, 3) gives values in [0, 1)
    # So, (np.random.rand(N, 3) - 0.5) gives values in [-0.5, 0.5)
    # Multiply by side_length to scale
    positions_val = (np.random.rand(N, 3) - 0.5) * side_length.item() # Get scalar value for multiplication

    # Shift by center
    positions_val[:, 0] += center[0].item()
    positions_val[:, 1] += center[1].item()
    positions_val[:, 2] += center[2].item()

    return positions_val * unit


def random_positions_in_sphere(N, radius=100*b2.um, center=(0,0,0)*b2.um):
    """
    Generates N random 3D positions uniformly distributed within a sphere.

    Uses the method of picking points in a cube and rejecting those outside
    the sphere, or a more direct method by transforming uniform random variables.
    The direct method (Marsaglia, 1972, for points in a ball) is more efficient.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    radius : brian2.dimensionss.fundamentalunits.Quantity, optional
        The radius of the sphere (default: 100 um).
    center : tuple of brian2.dimensionss.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the sphere
        (default: (0,0,0) um).

    Returns
    -------
    brian2.dimensionss.fundamentalunits.Quantity
        A (N, 3) Quantity array where each row is (x, y, z) coordinates
        of a point, with the specified Brian2 length unit.

    Examples
    --------
    >>> import brian2 as b2
    >>> positions = random_positions_in_sphere(5, radius=50*b2.um)
    >>> print(positions.shape)
    (5, 3)
    >>> print(positions.dimensions)
    um
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if not hasattr(radius, 'dimensions') or not radius.has_same_dimensions(b2.meter):
        raise TypeError("radius must be a Brian2 Quantity with length units.")
    if not (isinstance(center, (tuple, list)) and len(center) == 3 and
            all(hasattr(c, 'dimensions') and c.has_same_dimensions(b2.meter) for c in center)):
        raise TypeError("center must be a 3-tuple of Brian2 Quantities with length units.")

    unit = radius.dimensions
    radius_val = radius.item()
    positions_val = np.zeros((N, 3))
    count = 0

    while count < N:
        # Generate points in a cube that bounds the sphere
        x, y, z = (np.random.rand(3) * 2 - 1) * radius_val # [-radius_val, radius_val)
        if x**2 + y**2 + z**2 <= radius_val**2:
            positions_val[count, :] = [x, y, z]
            count += 1

    # Shift by center
    positions_val[:, 0] += center[0].item()
    positions_val[:, 1] += center[1].item()
    positions_val[:, 2] += center[2].item()

    return positions_val * unit


def random_positions_on_sphere_surface(N, radius=100*b2.um, center=(0,0,0)*b2.um):
    """
    Generates N random 3D positions uniformly distributed on the surface of a sphere.

    Uses Marsaglia's method for picking a random point on a sphere surface
    or by generating Gaussian-distributed coordinates and normalizing.

    Parameters
    ----------
    N : int
        The number of positions to generate.
    radius : brian2.dimensionss.fundamentalunits.Quantity, optional
        The radius of the sphere (default: 100 um).
    center : tuple of brian2.dimensionss.fundamentalunits.Quantity, optional
        A 3-tuple (x, y, z) representing the center of the sphere
        (default: (0,0,0) um).

    Returns
    -------
    brian2.dimensionss.fundamentalunits.Quantity
        A (N, 3) Quantity array where each row is (x, y, z) coordinates
        of a point, with the specified Brian2 length unit.

    Examples
    --------
    >>> import brian2 as b2
    >>> positions = random_positions_on_sphere_surface(5, radius=50*b2.um)
    >>> print(positions.shape)
    (5, 3)
    >>> # Check if points are on the surface (approximately)
    >>> distances = np.sqrt(np.sum(positions**2, axis=1))
    >>> np.allclose(distances, 50*b2.um)
    True
    """
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if not hasattr(radius, 'dimensions') or not radius.has_same_dimensions(b2.meter):
        raise TypeError("radius must be a Brian2 Quantity with length units.")
    if not (isinstance(center, (tuple, list)) and len(center) == 3 and
            all(hasattr(c, 'dimensions') and c.has_same_dimensions(b2.meter) for c in center)):
        raise TypeError("center must be a 3-tuple of Brian2 Quantities with length units.")

    unit = radius.dimensions
    radius_val = radius.item()

    # Generate N random points from a 3D Gaussian distribution
    # The direction of these vectors is uniformly random on the sphere.
    gauss_points = np.random.normal(size=(N, 3))

    # Normalize each point to lie on the unit sphere
    norm = np.linalg.norm(gauss_points, axis=1, keepdims=True)
    unit_sphere_points = gauss_points / norm

    # Scale by the desired radius
    positions_val = unit_sphere_points * radius_val

    # Shift by center
    positions_val[:, 0] += center[0].item()
    positions_val[:, 1] += center[1].item()
    positions_val[:, 2] += center[2].item()

    return positions_val * unit


def distance_matrix(positions1, positions2=None):
    """
    Calculates the Euclidean distance matrix between two sets of 3D points.

    Parameters
    ----------
    positions1 : brian2.dimensionss.fundamentalunits.Quantity or np.ndarray
        A (N, 3) array of N points. If units are not Brian2 Quantities,
        they are assumed to be consistent.
    positions2 : brian2.dimensionss.fundamentalunits.Quantity or np.ndarray, optional
        A (M, 3) array of M points. If None, calculates the distance
        matrix for `positions1` with itself (default: None).

    Returns
    -------
        A (N, M) distance matrix. The unit will be the same as the input
        positions if they are Brian2 Quantities.

    Raises
    ------
    ValueError
        If input arrays do not have 3 columns.
    """
    p1_val = positions1
    unit = None
    if hasattr(positions1, 'dimensions'):
        unit = positions1.dimensions
        p1_val = positions1.item() # Get numerical values

    if p1_val.shape[1] != 3:
        raise ValueError("positions1 must be an N x 3 array.")

    if positions2 is None:
        p2_val = p1_val
    else:
        p2_val = positions2
        if hasattr(positions2, 'unit'):
            if unit is not None and positions2.dimensions != dimensions:
                # For simplicity, require same units or handle conversion
                raise ValueError("positions1 and positions2 must have the same units if using Brian2 Quantities.")
            elif unit is None: # p1 was raw numpy, p2 has units
                unit = positions2.dimensions # inherit unit from p2
            p2_val = positions2.item()
        elif unit is not None: # p1 has units, p2 is raw numpy
             pass # p2_val is already numerical, result will have unit of p1

        if p2_val.shape[1] != 3:
            raise ValueError("positions2 must be an M x 3 array.")

    # Efficiently calculate squared Euclidean distances
    # dist_sq[i,j] = sum_k ( (p1[i,k] - p2[j,k])^2 )
    #            = sum_k ( p1[i,k]^2 - 2*p1[i,k]*p2[j,k] + p2[j,k]^2 )
    #            = sum_k p1[i,k]^2 + sum_k p2[j,k]^2 - 2 * sum_k p1[i,k]*p2[j,k]
    #            = sum_k p1[i,k]^2 + sum_k p2[j,k]^2 - 2 * p1[i,:] @ p2[j,:].T
    p1_sq_sum = np.sum(p1_val**2, axis=1, keepdims=True) # Shape (N, 1)
    p2_sq_sum = np.sum(p2_val**2, axis=1)              # Shape (M,)
    dot_product = np.dot(p1_val, p2_val.T)             # Shape (N, M)

    dist_sq_val = p1_sq_sum + p2_sq_sum - 2 * dot_product
    dist_sq_val = np.maximum(dist_sq_val, 0) # Ensure non-negative due to precision issues
    dist_val = np.sqrt(dist_sq_val)

    if unit is not None:
        return dist_val * unit
    else:
        return dist_val

# Add more spatial utility functions as needed, e.g., for finding neighbors within a radius.
