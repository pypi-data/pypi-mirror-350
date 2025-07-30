# src/pyneurorg/mea/mea.py

"""
Defines the MEA (Microelectrode Array) class for pyneurorg simulations.

This class represents the MEA geometry and provides utility functions for
interacting with electrodes and neurons in an Organoid.
"""

import numpy as np
import brian2 as b2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # For 3D plotting

# For type hinting if Organoid class is used in methods
from ..organoid.organoid import Organoid
from ..organoid.spatial import _ensure_um_quantity, _extract_value_in_um # Helper from spatial

class MEA:
    """
    Represents a Microelectrode Array (MEA) geometry.

    Stores electrode positions and provides methods to interact with them,
    such as finding nearby neurons from an Organoid.

    Parameters
    ----------
    electrode_positions : array-like or brian2.units.fundamentalunits.Quantity
        A list, tuple, NumPy array, or Brian2 Quantity representing the
        3D coordinates of each electrode.
        If a list/tuple/array of numbers, units are assumed to be micrometers (um).
        If a Brian2 Quantity, it must have length dimensions.
        Expected shape is (N_electrodes, 3) for (x, y, z).
    name : str, optional
        A descriptive name for the MEA instance (default: "pyneurorg_MEA").

    Attributes
    ----------
    name : str
        Name of the MEA.
    electrode_positions : brian2.units.fundamentalunits.Quantity
        A (N_electrodes, 3) Quantity array storing the (x,y,z) coordinates
        of each electrode in micrometers (um).
    num_electrodes : int
        The total number of electrodes in the MEA.
    """

    def __init__(self, electrode_positions, name="pyneurorg_MEA"):
        """
        Initializes a new MEA instance.
        """
        self.name = name
        
        if electrode_positions is None:
            raise ValueError("electrode_positions must be provided.")

        processed_positions = []
        if isinstance(electrode_positions, b2.Quantity):
            if electrode_positions.dimensions != b2.metre.dimensions:
                raise TypeError("If electrode_positions is a Brian2 Quantity, it must have length dimensions.")
            # Convert to um for internal consistency
            val_in_um_array = np.asarray(electrode_positions / b2.um)
            processed_positions = val_in_um_array * b2.um
        elif isinstance(electrode_positions, (list, tuple, np.ndarray)):
            try:
                # Assume um if raw numbers/array
                pos_array = np.asarray(electrode_positions, dtype=float)
                if pos_array.ndim == 1 and pos_array.shape[0] == 3: # Single electrode
                    pos_array = pos_array.reshape(1, 3)
                elif pos_array.ndim != 2 or pos_array.shape[1] != 3:
                    raise ValueError("electrode_positions must be N x 3 or a single 3-element list/array.")
                processed_positions = pos_array * b2.um
            except Exception as e:
                raise TypeError(f"Could not interpret electrode_positions as coordinate array (assumed um): {e}")
        else:
            raise TypeError("electrode_positions must be a Brian2 Quantity, list, tuple, or NumPy array.")

        if not processed_positions.shape[0] > 0:
            raise ValueError("electrode_positions cannot be empty.")
            
        self.electrode_positions = processed_positions
        self.num_electrodes = self.electrode_positions.shape[0]

    def get_electrode_position(self, electrode_id):
        """
        Retrieves the 3D coordinates of a specific electrode.

        Parameters
        ----------
        electrode_id : int
            The index of the electrode (0 to num_electrodes - 1).

        Returns
        -------
        brian2.units.fundamentalunits.Quantity
            A (3,) Quantity array representing the (x, y, z) coordinates
            of the specified electrode in micrometers (um).

        Raises
        ------
        IndexError
            If electrode_id is out of bounds.
        """
        if not (0 <= electrode_id < self.num_electrodes):
            raise IndexError(f"electrode_id {electrode_id} is out of bounds "
                             f"(0 to {self.num_electrodes - 1}).")
        return self.electrode_positions[electrode_id, :]

    def get_neurons_near_electrode(self, organoid: Organoid, neuron_group_name: str,
                                   electrode_id: int, radius):
        """
        Finds neurons from a specified group in an Organoid that are within
        a given radius of a specific electrode.

        Parameters
        ----------
        organoid : pyneurorg.organoid.organoid.Organoid
            The Organoid instance containing the neurons.
        neuron_group_name : str
            The name of the NeuronGroup within the organoid to search.
        electrode_id : int
            The index of the electrode.
        radius : float or brian2.units.fundamentalunits.Quantity
            The search radius around the electrode. If a raw number,
            assumed to be in micrometers (um).

        Returns
        -------
        numpy.ndarray
            An array of integer indices of the neurons within the specified
            NeuronGroup that are within the given radius of the electrode.
            Indices are relative to the NeuronGroup.

        Raises
        ------
        KeyError
            If `neuron_group_name` is not found in the organoid.
        IndexError
            If `electrode_id` is out of bounds.
        TypeError
            If `radius` is not a number or Brian2 Quantity with length dimensions.
        """
        if not isinstance(organoid, Organoid):
            raise TypeError("organoid must be an instance of pyneurorg.organoid.Organoid.")
        
        neuron_positions_um_qty = organoid.get_positions(neuron_group_name) # Returns Quantity in um
        electrode_pos_um_qty = self.get_electrode_position(electrode_id)   # Returns Quantity in um
        radius_um_qty = _ensure_um_quantity(radius, "radius")             # Returns Quantity in um

        # Perform calculations with numerical values (already in um)
        neuron_pos_vals_um = np.asarray(neuron_positions_um_qty / b2.um)
        electrode_pos_val_um = np.asarray(electrode_pos_um_qty / b2.um) # Should be 1x3
        radius_val_um = float(radius_um_qty / b2.um)

        # Calculate squared distances to avoid sqrt until the end
        distances_sq = np.sum((neuron_pos_vals_um - electrode_pos_val_um)**2, axis=1)
        
        nearby_neuron_indices = np.where(distances_sq <= radius_val_um**2)[0]
        return nearby_neuron_indices

    @staticmethod
    def generate_grid_layout(rows, cols, spacing=50, z_plane=0, center_origin=True):
        """
        Generates electrode positions for a 2D grid layout.

        Parameters are assumed to be in micrometers (um) if raw numbers.

        Parameters
        ----------
        rows : int
            Number of rows in the grid.
        cols : int
            Number of columns in the grid.
        spacing : float or brian2.units.fundamentalunits.Quantity, optional
            Distance between adjacent electrodes. If a number, assumed um.
            (default: 50).
        z_plane : float or brian2.units.fundamentalunits.Quantity, optional
            The z-coordinate for all electrodes. If a number, assumed um.
            (default: 0).
        center_origin : bool, optional
            If True, the grid will be centered around (0,0) in the xy-plane.
            If False, the bottom-left electrode will be at (0,0) or near it.
            (default: True).

        Returns
        -------
        brian2.units.fundamentalunits.Quantity
            A (rows*cols, 3) Quantity array of electrode positions in um.
        """
        if not (isinstance(rows, int) and rows > 0 and isinstance(cols, int) and cols > 0):
            raise ValueError("rows and cols must be positive integers.")

        spacing_um_qty = _ensure_um_quantity(spacing, "spacing")
        z_plane_um_qty = _ensure_um_quantity(z_plane, "z_plane")

        spacing_val_um = float(spacing_um_qty / b2.um)
        z_plane_val_um = float(z_plane_um_qty / b2.um)

        positions = []
        for r in range(rows):
            for c in range(cols):
                positions.append([c * spacing_val_um, r * spacing_val_um, z_plane_val_um])
        
        positions_arr_um = np.array(positions)

        if center_origin:
            max_x = (cols - 1) * spacing_val_um
            max_y = (rows - 1) * spacing_val_um
            positions_arr_um[:, 0] -= max_x / 2.0
            positions_arr_um[:, 1] -= max_y / 2.0
            # z_plane remains as is relative to the shift

        return positions_arr_um * b2.um

    def plot_layout(self, ax=None, organoid_positions=None, organoid_group_name="",
                    electrode_color='blue', electrode_size=50,
                    neuron_color='gray', neuron_size=5, alpha_neurons=0.3):
        """
        (Optional) Plots the 2D or 3D layout of the MEA electrodes.

        If organoid_positions are provided, they are plotted as well.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            An existing Matplotlib Axes object to plot on. If None, a new
            figure and 3D axes are created.
        organoid_positions : brian2.units.fundamentalunits.Quantity, optional
            A (N, 3) Quantity array of neuron positions (in um) from an Organoid
            to plot alongside the MEA.
        organoid_group_name : str, optional
            Name of the organoid group, used for legend if plotting neurons.
        electrode_color : str, optional
            Color for the MEA electrode markers.
        electrode_size : int, optional
            Size for the MEA electrode markers.
        neuron_color : str, optional
            Color for the neuron markers.
        neuron_size : int, optional
            Size for the neuron markers.
        alpha_neurons : float, optional
            Alpha transparency for neuron markers.
        """
        is_3d = True # Assume 3D plot by default
        if ax is None:
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection='3d')
        elif not hasattr(ax, 'plot_surface'): # Crude check if it's a 3D Axes
            print("Warning: Provided 'ax' is not a 3D Axes. Plotting in 2D (XY plane).")
            is_3d = False


        # Electrode positions (numerical values in um)
        e_pos_um = np.asarray(self.electrode_positions / b2.um)

        if is_3d:
            ax.scatter(e_pos_um[:, 0], e_pos_um[:, 1], e_pos_um[:, 2],
                       c=electrode_color, s=electrode_size, label=f"{self.name} Electrodes",
                       depthshade=True)
        else: # 2D plot
            ax.scatter(e_pos_um[:, 0], e_pos_um[:, 1],
                       c=electrode_color, s=electrode_size, label=f"{self.name} Electrodes")


        if organoid_positions is not None:
            # Assuming organoid_positions is already a Quantity in um from Organoid.get_positions()
            n_pos_um = np.asarray(organoid_positions / b2.um)
            label_n = f"Neurons ({organoid_group_name})" if organoid_group_name else "Neurons"
            if is_3d:
                ax.scatter(n_pos_um[:, 0], n_pos_um[:, 1], n_pos_um[:, 2],
                           c=neuron_color, s=neuron_size, label=label_n, alpha=alpha_neurons,
                           depthshade=False) # Neurons usually don't need depthshade
            else:
                ax.scatter(n_pos_um[:, 0], n_pos_um[:, 1],
                           c=neuron_color, s=neuron_size, label=label_n, alpha=alpha_neurons)


        ax.set_xlabel("X (µm)")
        ax.set_ylabel("Y (µm)")
        if is_3d:
            ax.set_zlabel("Z (µm)")
        ax.set_title(f"MEA Layout: {self.name}")
        ax.legend()
        ax.grid(True)
        
        # Try to make aspect ratio equal for 3D plots if possible
        if is_3d:
            try:
                all_x = e_pos_um[:,0]
                all_y = e_pos_um[:,1]
                all_z = e_pos_um[:,2]
                if organoid_positions is not None:
                    all_x = np.concatenate((all_x, n_pos_um[:,0]))
                    all_y = np.concatenate((all_y, n_pos_um[:,1]))
                    all_z = np.concatenate((all_z, n_pos_um[:,2]))
                
                max_range = np.array([all_x.max()-all_x.min(), 
                                      all_y.max()-all_y.min(), 
                                      all_z.max()-all_z.min()]).max() / 2.0
                if max_range == 0: max_range = np.max(np.abs(e_pos_um)) # Handle single point or flat cases
                if max_range == 0: max_range = 10 # Default if still zero

                mid_x = (all_x.max()+all_x.min()) * 0.5
                mid_y = (all_y.max()+all_y.min()) * 0.5
                mid_z = (all_z.max()+all_z.min()) * 0.5
                ax.set_xlim(mid_x - max_range, mid_x + max_range)
                ax.set_ylim(mid_y - max_range, mid_y + max_range)
                ax.set_zlim(mid_z - max_range, mid_z + max_range)
            except Exception: # In case of issues with calculating range (e.g., no points)
                pass # Keep default matplotlib scaling

        return ax

    def __str__(self):
        return f"<MEA '{self.name}' with {self.num_electrodes} electrodes>"

    def __repr__(self):
        return self.__str__()