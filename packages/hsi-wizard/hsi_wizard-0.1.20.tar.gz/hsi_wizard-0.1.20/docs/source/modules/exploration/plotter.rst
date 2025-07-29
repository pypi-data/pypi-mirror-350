.. _plotter:

Plotter
-------
.. module::  wizard._exploration.plotter
   :platform: Unix
   :synopsis: Plotter function for hyperspectral imaging (HSI) data.

.. function:: plotter(dc)

   This module provides an interactive plotting interface to explore and analyze
   data cubes. Users can visualize slices, define regions of interest (ROIs), and
   inspect the spectral data interactively. It features saving, removing, and normalizing
   plots, and allows ROI-based analysis.

   :param dc: DataCube containing hyperspectral imaging (HSI) data.
   :type dc: DataCube

   This function allows interactive visualization of hyperspectral imaging data, providing features such as:

   - Image layer selection by wavelength.
   - ROI (Region of Interest) selection and mean spectrum calculation.
   - Saving and removing plotted spectra with unique colors.
   - Normalization toggle for spectral data.

   The interactive interface includes:

   - A main image display of the selected wavelength layer.
   - A spectrum plot with the mean spectrum of the selected ROI.
   - Buttons to save and remove plots.
   - A checkbox to enable normalization.

   Example Usage:
   --------------

   The following example script demonstrates how to use the `plotter` function:

   .. literalinclude:: ../../../../examples/01_plot_DataCube/01_example.py
      :language: python
      :linenos:

   .. figure:: ../../../../resources/imgs/plotter_example.png
      :align: center
      :alt: Example of the plotter function in action.

      Example visualization of hyperspectral data using the plotter function.
