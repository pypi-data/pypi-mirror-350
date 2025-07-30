.. _loader:

loader
======

This package provides a collection of modules for handling various file formats and converting their contents into a unified `DataCube` format.

The `wizard.read()` function serves as the main entry point for users. It abstracts the file handling process and automatically determines the appropriate handler based on the file type. For example:

.. code-block:: python

    from wizard import read

    # Reading an FSM file
    datacube = read('test.fsm')

    # Reading a CSV file
    datacube = read('data.csv')



Each file format has a corresponding module with specialized functions for reading and writing data.

.. contents:: Modules Overview
   :local:
   :depth: 1

csv
---

.. module:: wizard._utils._loader.csv
   :platform: Unix
   :synopsis: Provides reader and writer functions for CSV files.

This module includes functions for reading and writing `.csv` files.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.csv._read_csv
.. autofunction:: wizard._utils._loader.csv._write_csv


folder
------

.. module:: wizard._utils._loader.folder
   :platform: Unix
   :synopsis: Provides functions to read image files from a folder.

This module includes functions for reading images from files and converting them into a `DataCube`.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.folder._read_folder


fsm
---

.. module:: wizard._utils._loader.fsm
   :platform: Unix
   :synopsis: Provides reader functions for FSM files.

This module includes functions for reading `.fsm` files, typically from Perkin Elmer instruments.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.fsm._read_fsm


nrrd
----

.. module:: wizard._utils._loader.nrrd
   :platform: Unix
   :synopsis: Provides functions to read and write NRRD files.

This module includes functions for reading and writing `.nrrd` files, which are commonly used
to store multi-dimensional data, particularly in the field of medical imaging.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.nrrd._read_nrrd
.. autofunction:: wizard._utils._loader.nrrd._write_nrrd


pickle
------

.. module:: wizard._utils._loader.pickle
   :platform: Unix
   :synopsis: Provides functions to read and write pickle files.

This module includes functions for reading pickle files that store serialized Python objects,
specifically NumPy arrays.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.pickle._read_pickle
.. autofunction:: wizard._utils._loader.pickle._write_pickle


tdms
----

.. module:: wizard._utils._loader.tdms
   :platform: Unix
   :synopsis: Provides functions to read .tdms files.

This module includes functions for reading `.tdms` files, specifically designed to extract spectral data
and organize it into a DataCube format.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.tdms._read_tdms


xlsx
----

.. module:: wizard._utils._loader.xlsx
   :platform: Unix
   :synopsis: Provides functions to read and write .xlsx files.

This module includes functions for reading from and writing to `.xlsx` files, facilitating the
import and export of spectral data organized in a DataCube format.

Functions
~~~~~~~~~

.. autofunction:: wizard._utils._loader.xlsx._read_xlsx
.. autofunction:: wizard._utils._loader.xlsx._write_xlsx

Credits
-------

The FSM module in this package was inspired by the `specio` repository by paris-saclay-cds. The original repository can be found at https://github.com/paris-saclay-cds/specio.