.. _install:

Installation
============

This document provides detailed explanation about installation.

Downloading the source (Optional)
---------------------------------

.. _download-source:

You can download full source code of WettingFront project from
its repository.

.. code-block:: bash

   $ git clone git@github.com:https://epicgit.snu.ac.kr/Jisu/wettingfront.git

Installing
----------

The package can be installed by

.. code-block:: bash

   $ pip install [-e] <url/path>[[...]]

.. rubric:: Install options

.. _install-options:

There are two noticeable install options for developers.

* Install with editable option (``-e``)
* Install with optional dependencies (``[...]``)

The editable option allows changes made to the source code to be immediately
reflected in the installed package. For more information, refer to
`pip documentation <https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs>`_.

Optional dependencies can be specified by adding them into brackets right after
the package url/path. When specified, additional module are installed to help
accessing extra features of the package.

Available optional dependencies for WettingFront are:

* ``img``: access to image analysis features.
* ``test``: run tests.
* ``doc``: build documentations.
* ``dev``: every additional dependency (useful for development).

With commas without trailing whitespaces, i.e. ``[A,B]``, you can pass multiple
specifications.

Installing from repository
^^^^^^^^^^^^^^^^^^^^^^^^^^

By passing the vcs url, ``pip`` command automatically clones the source code
and installs the package.

.. code-block:: bash

   $ pip install git+https://github.com/JSS95/wettingfront.git

If you want to pass install options, you need to specify the package name by
``#egg=``. For example, the following code installs the package with
``dev`` dependencies.

.. code-block:: bash

   $ pip install git+https://github.com/JSS95/wettingfront.git#egg=wettingfront[dev]

.. note::

   If you pass ``-e`` option, source code of the project will be downloaded in
   your current location.

Installing from source
^^^^^^^^^^^^^^^^^^^^^^

.. _install-from-source:

If you have already downloaded the source, you can install it by passing its
path to ``pip install``. For example, in the path where ``pyproject.toml`` is
located, the following command installs the package in editable mode, with
full dependencies for developers.

.. code-block:: bash

   $ pip install -e .[dev]
