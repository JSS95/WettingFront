Getting started
===============

.. currentmodule:: wettingfront

Installation
------------

WettingFront can be installed by :mod:`pip` from
github repository.

.. code-block:: bash

   pip install git+https://github.com/JSS95/wettingfront.git

This installs the package with its latest commit. If you want a specific
version, append ``@[tag name]`` such as:

.. code-block:: bash

   pip install git+https://github.com/JSS95/wettingfront.git@v1.0.0

For more detailed instructions, refer to :ref:`install`.

Basic usage
-----------

WettingFront provides command-line API to invoke analysis using configuration
files.

.. code-block:: bash

   wettingfront analyze config1.yml config2.json ...

It can be run as a package as well:

.. code-block:: bash

   python -m wettingfront analyze config1.yml config2.json ...

Check :ref:`config-reference` to learn about the configuration file structure.

.. note::
   To check the other commands, run:

   .. code-block:: bash

      wettingfront -h

   Or you can refer to :ref:`command-reference` page.

Next steps
----------

For more detailed information, please refer to the following pages:

* :ref:`tutorial` pages provides quick examples.
* Read :ref:`module-reference` for the Python runtime API.
* :ref:`explanation` page includes detailed information for developers.
