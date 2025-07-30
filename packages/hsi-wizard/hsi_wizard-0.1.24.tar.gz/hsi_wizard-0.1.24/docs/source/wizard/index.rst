.. _wizard:

========
Features
========
The core functionality of `hsi-wizard` includes:

- **DataCube Class**: Manage, track and process HSI data using a powerful object model
- **Spectral Visualization**: Plot and explore spectral data using interactive and static visualizations
- **Clustering and Analytics**: Apply clustering methods and analytics for exploratory data analysis
- **File Format Support**: Seamless integration with various file formats, including `.nrrd`, `.pickle`, `.csv`, and `.xlsx`

For a detailed breakdown of each module, refer to the :ref:`Modules <Modules>` section below.

============
Installation
============
You can install `hsi-wizard` through pip or compile it from source:

Via pip
-------
To install the latest release via pip, use:

.. code-block:: console

   pip install hsi-wizard

Compile from Source
-------------------
To install from source:

.. code-block:: console

   python -m pip install -U pip setuptools wheel             # Install/update build tools
   git clone https://github.com/BlueSpacePotato/hsi-wizard   # Clone the repository
   cd hsi-wizard                                             # Navigate into the directory
   python -m venv .env                                       # Create a virtual environment
   source .env/bin/activate                                  # Activate the environment
   pip install -e .                                          # Install in editable mode


====================
DataCube Key Concept
====================

DataCube Representation
-----------------------


The `DataCube.cube` is a 3D array of shape `(v, x, y)`:

   - `v` represents the spectral depth (wavelength)
   - `x` and `y` represent the spatial resolution

Wavelengths and Notation
------------------------


The `DataCube` often contains wavelength information in units such as nanometers (`nm`) or wavenumbers (`cm⁻¹`).

   - this information is stored in the `wavelengths` attribute and can be dynamically updated
   - the `notation` attribute specifies the unit of data
