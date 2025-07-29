"""
surface.py
==========

.. module:: surface
:platform: Unix
:synopsis: Surface plotting and manipulation module for the hsi-wizard package.

Module Overview
--------------

This module provides functionalities for manipulating and visualizing data cubes.
It includes utilities for slicing, cutting, and plotting 3D surfaces interactively
using sliders.

"""

from wizard import DataCube
import numpy as np
import copy
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider


def dc_cut_by_value(z: np.array, val: int, type: str) -> np.array:
    """
    Cut a data cube slice by a defined value.

    This function normalizes the input array, applies a threshold cut-off, and
    replaces values below the cut-off with the minimum value of the array.

    :param z: 2D numpy array representing a data cube slice
    :param val: Cut-off value for thresholding
    :param type: Type of cut-off operation (currently unused)
    :return: Modified 2D numpy array after applying the cut-off
    """
    new_z = copy.deepcopy(z)
    new_z /= new_z.max()
    new_z[new_z <= val] = new_z.min()
    return new_z


def get_z_surface(cube: np.array, v: int) -> np.array:
    """
    Calculate the surface for plotting from a data cube.

    This function extracts a slice from the data cube at the specified
    index and generates a 2D surface array for plotting.

    :param cube: 3D numpy array representing the data cube
    :param v: Index of the slice to extract
    :return: 2D numpy array representing the surface for plotting
    """
    z = np.zeros((cube.shape[1], cube.shape[2]))
    slice_v = cube[v, :, :]
    mask = slice_v > 0
    z[mask] = slice_v[mask]
    return z


def plot_surface(dc: DataCube, index: int = 0):
    """
    Plot a 3D surface from a DataCube slice with interactive sliders.

    This function creates an interactive 3D surface plot of a DataCube slice.
    Users can adjust the slice index and cut-off value using sliders.

    :param dc: DataCube object containing the data to plot
    :param index: Initial index value for the DataCube slice (default is 0)
    """
    def update(val):
        idx = int(slider.val)  # Ensure integer values
        cut_val = slider_cut.val  # Get cut value

        ax.clear()
        z = get_z_surface(dc, idx)

        # Apply the cut before getting the surface data
        z = dc_cut_by_value(z, cut_val, type="")

        x, y = np.meshgrid(range(dc.shape[1]), range(dc.shape[2]))
        ax.plot_surface(x, y, z.T, cmap=cm.coolwarm)
        ax.set_title(f'{dc.name if dc.name else ""} @{dc.wavelengths[idx]:.2f} {dc.notation if dc.notation else ""}')
        ax.set(xlabel='x', ylabel='y', zlabel='counts')
        fig.canvas.draw_idle()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Wavelength slider
    slider_ax = fig.add_axes([0.2, 0.02, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    tick_positions = np.linspace(0, len(dc.wavelengths) - 1, min(5, len(dc.wavelengths))).astype(int)
    slider = Slider(slider_ax, 'Wavelength', 0, dc.shape[0] - 1, valinit=index, valstep=1)
    slider.ax.set_xticks(tick_positions)
    slider.ax.set_xticklabels([f'{dc.wavelengths[i]:.2f}' for i in tick_positions])
    slider.on_changed(update)

    # Cut value slider
    slider_cut_ax = fig.add_axes([0.2, 0.06, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    slider_cut = Slider(slider_cut_ax, 'Cut Value', 0, 1, valinit=0, valstep=0.01)  # Cut value from 0 to 1
    slider_cut.on_changed(update)

    update(index)  # Initial plot
    plt.show()
