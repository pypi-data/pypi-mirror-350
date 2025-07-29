.. _datacube_ops:

DataCube Operations
===================

.. module:: wizard._core.datacube_ops
    :platform: Unix
    :synopsis: DataCube Operations.

Module Overview
---------------

This module contains functions for processing datacubes. The methods are dynamically added to the DataCube class in its __init__ method. Therefore, they can be used as standalone functions or as methods of the DataCube class.

Functions
---------

.. autofunction:: remove_spikes
.. autofunction:: remove_background
.. autofunction:: resize
.. autofunction:: baseline_als
.. autofunction:: merge_cubes
.. autofunction:: inverse
.. autofunction:: register_layers
.. autofunction:: remove_vingetting
