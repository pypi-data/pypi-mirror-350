"""
plotter.py
==========

.. module:: plotter
:platform: Unix
:synopsis: Interactive plotting module for the hsi-wizard package.

Module Overview
--------------

This module provides an interactive plotting interface to explore and analyze
data cubes. Users can visualize slices, define regions of interest (ROIs), and
inspect the spectral data interactively. It features saving, removing, and normalizing
plots, and allows ROI-based analysis.

Importing
--------

from .._utils.helper import find_nex_smaller_wave, normalize
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, RectangleSelector
from matplotlib.gridspec import GridSpec
import random

from .._utils.helper import find_nex_smaller_wave, normalize_spec

# State dictionary to manage the global variables locally
state = {
    'layer_id': 0,
    'normalize_flag': False
}

saved_plots = []  # To hold saved plot data (wave, spec, ROI info, color)
saved_lines = []  # To hold the actual line objects for plotting
saved_rois = []  # To hold ROI rectangles for display


def plotter(dc):
    """
    Interactive plotter function to explore the DataCube.

    This function provides an interactive visualization interface for a DataCube.
    Users can view slices, define and save regions of interest (ROIs), and inspect
    spectral data interactively.

    :param dc: DataCube object containing the data to be visualized
    """
    state['layer_id'] = 0  # Initialize layer ID

    # Initialize ROI coordinates
    roi_x_start, roi_x_end = 0, dc.cube.shape[2]
    roi_y_start, roi_y_end = 0, dc.cube.shape[1]

    def on_key(event):
        """
        Change layer_id using left/right arrow keys
        and refresh the plots.
        """
        if event.key == 'left':
            # step down, but not below 0
            state['layer_id'] = max(0, state['layer_id'] - 1)
            update_plot()
        elif event.key == 'right':
            # step up, but not beyond last index
            max_idx = dc.cube.shape[0] - 1
            state['layer_id'] = min(max_idx, state['layer_id'] + 1)
            update_plot()

    def update_plot(_=None):
        """
        Update the main plot with the current state.

        This function refreshes the displayed image slice, ROI mean spectrum,
        and saved plots based on the current state.
        """
        layer_index = state['layer_id']
        layer = dc.cube[layer_index]
        imshow.set_data(layer)
        imshow.set_clim(vmin=layer.min(), vmax=layer.max())
        layer_id = dc.wavelengths[state["layer_id"]]
        notation = dc.notation or ""
        ax[0].set_title(f'Image @{notation}{layer_id}')

        # Update the vertical line to the current wavelength layer
        line.set_xdata([dc.wavelengths[state['layer_id']]])

        # Update ROI mean plot
        update_roi_mean()

        # Update saved plots without re-adding lines
        for i, sp in enumerate(saved_plots):
            saved_spec = sp['spec']
            if state['normalize_flag']:
                saved_spec = normalize_spec(saved_spec)
            saved_lines[i].set_data(sp['wave'], saved_spec)
            saved_lines[i].set_color(sp['color'])  # Use saved color

        fig.canvas.draw_idle()

    def save_plot(_):
        """
        Save the current spectrum data and ROI coordinates.

        This function saves the mean spectrum of the current ROI along with
        its coordinates and a randomly assigned color for visualization.
        """
        roi_data = dc.cube[:, roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        mean_spec = np.mean(roi_data, axis=(1, 2))
        if state['normalize_flag']:
            mean_spec = normalize_spec(mean_spec)

        # Generate a random color for this ROI and save it with the plot
        color = (random.random(), random.random(), random.random())  # Random RGB color
        saved_plots.append({
            'wave': dc.wavelengths,
            'spec': mean_spec,
            'roi': (roi_x_start, roi_x_end, roi_y_start, roi_y_end),  # Save ROI coordinates
            'color': color
        })

        # Plot with the specific color for the saved ROI
        saved_line, = ax[1].plot(saved_plots[-1]['wave'], saved_plots[-1]['spec'], color=color, alpha=0.4)
        saved_lines.append(saved_line)

        # Draw the rectangle on the image to represent the ROI and save it
        roi_rect = plt.Rectangle((roi_x_start, roi_y_start), roi_x_end - roi_x_start, roi_y_end - roi_y_start,
                                 linewidth=2, edgecolor=color, facecolor=color, alpha=0.4)
        ax[0].add_patch(roi_rect)
        saved_rois.append(roi_rect)  # Store the rectangle so we can manage it later

        update_plot()

    def remove_last_plot(_):
        """
        Remove the last saved plot and its corresponding ROI rectangle.

        This function deletes the most recently saved plot and its associated
        ROI rectangle from the visualization.
        """
        if saved_plots:
            saved_plots.pop()
            saved_lines.pop().remove()

            # Remove the corresponding ROI rectangle
            if saved_rois:
                roi_rect = saved_rois.pop()
                roi_rect.remove()

            update_plot()

    def toggle_normalization(_):
        """
        Toggle normalization for the spectral data.

        This function switches the normalization flag and updates the plot
        to reflect the changes.
        """
        state['normalize_flag'] = not state['normalize_flag']
        update_plot()

    def update_roi_mean():
        """
        Compute and plot the mean spectrum over the selected ROI.

        This function calculates the mean spectrum for the current ROI and
        updates the plot accordingly.
        """
        roi_data = dc.cube[:, roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        mean_spec = np.mean(roi_data, axis=(1, 2))
        if state['normalize_flag']:
            mean_spec = normalize_spec(mean_spec)

        # Define range padding
        r = (mean_spec.max() - mean_spec.min()) * 0.1
        ax[1].set_ylim(0 if state['normalize_flag'] else mean_spec.min() - r,
                       1 if state['normalize_flag'] else mean_spec.max() + r)
        roi_line.set_data(dc.wavelengths, mean_spec)

    def on_roi_change(eclick, erelease):
        """
        Handle rectangle selector change to update ROI coordinates.

        This function updates the ROI coordinates based on user interaction
        with the rectangle selector.
        """
        nonlocal roi_x_start, roi_x_end, roi_y_start, roi_y_end

        roi_x_start, roi_y_start = int(eclick.xdata), int(eclick.ydata)
        roi_x_end, roi_y_end = int(erelease.xdata), int(erelease.ydata)

        if roi_x_start - roi_x_end == 0:
            roi_x_end += 1
        if roi_y_start - roi_y_end == 0:
            roi_y_end += 1

        update_plot()

    def onclick_select(event):
        """
        Handle click events to update ROI coordinates or layer index.

        This function allows users to select a specific ROI or wavelength
        layer by clicking on the plots.
        """
        nonlocal roi_x_start, roi_x_end, roi_y_start, roi_y_end
        if event.inaxes == ax[0]:
            roi_x, roi_y = int(event.xdata), int(event.ydata)
            roi_x_start, roi_x_end = roi_x, roi_x + 1
            roi_y_start, roi_y_end = roi_y, roi_y + 1
            update_plot()
        elif event.inaxes == ax[1]:
            try:
                state['layer_id'] = np.where(dc.wavelengths == find_nex_smaller_wave(dc.wavelengths, int(event.xdata), 10))[0][0]
            except IndexError:
                return
            update_plot()

    # Create main figure and layout with GridSpec
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 2, width_ratios=[4, 4], height_ratios=[4, 1])

    # Main plotting area (image and spectrum)
    ax_image = fig.add_subplot(gs[0, 0])
    ax_spectrum = fig.add_subplot(gs[0, 1])
    ax_spectrum.set_title('Spectrum')
    ax = [ax_image, ax_spectrum]

    # Control panel for buttons and checkbox
    ax_control = fig.add_subplot(gs[1, :])
    ax_control.axis("off")

    # Set up the initial plots
    layer = dc.cube[0]
    imshow = ax[0].imshow(layer)
    spec = dc.cube[:, 0, 0]
    line = ax[1].axvline(x=state['layer_id'], color='lightgrey', linestyle='dashed')

    # ROI mean line
    roi_line, = ax[1].plot(dc.wavelengths, spec, label="ROI Mean")
    ax[1].set_xlabel(f'{dc.notation}')
    ax[1].set_ylabel('Counts')
    ax[1].set_xlim(dc.wavelengths.min(), dc.wavelengths.max())

    # Buttons and checkbox in the control panel
    ax_save = fig.add_axes([0.05, 0.1, 0.15, 0.075])
    btn_save = Button(ax_save, 'Save Plot')
    btn_save.on_clicked(save_plot)

    ax_remove = fig.add_axes([0.25, 0.1, 0.15, 0.075])
    btn_remove = Button(ax_remove, 'Remove Plot')
    btn_remove.on_clicked(remove_last_plot)

    ax_checkbox = fig.add_axes([0.45, 0.1, 0.15, 0.075])
    check = CheckButtons(ax_checkbox, ['Normalize Y (0-1)'], [False])
    check.on_clicked(toggle_normalization)

    # ROI selection
    _ = RectangleSelector(ax[0], on_roi_change, useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    fig.canvas.mpl_connect("button_press_event", onclick_select)
    
    fig.canvas.mpl_connect("key_press_event", on_key)

    update_plot()

    # plt.tight_layout(rect=[0, 0, .95, 1])
    plt.show()
