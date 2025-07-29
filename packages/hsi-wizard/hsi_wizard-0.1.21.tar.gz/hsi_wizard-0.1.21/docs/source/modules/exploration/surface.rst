.. _surface:

Surface Plotter
---------------

.. module:: wizard._exploration.surface
   :platform: Unix
   :synopsis: Plotter function for hyperspectral imaging (HSI) data.

.. function:: plot_surface(dc)

   This module provides functionalities for manipulating and visualizing hyperspectral imaging (HSI) data cubes. It includes utilities for slicing, cutting, and plotting 3D surfaces interactively using sliders.

   :param dc: DataCube containing hyperspectral imaging (HSI) data.
   :type dc: DataCube

   This function allows interactive visualization of hyperspectral imaging data, enabling users to explore data slices and apply threshold-based cuts interactively.

   Example Usage:
   --------------

   The following example script demonstrates how to use the `plot_surface` function:

   .. literalinclude:: ../../../../examples/06_plot_surface/06_example.py
      :language: python
      :linenos:

   .. figure:: ../../../../resources/imgs/surface_example.png
      :align: center
      :alt: Example of the surface plotter function in action.

      Example visualization of hyperspectral data using the surface plotting function.

