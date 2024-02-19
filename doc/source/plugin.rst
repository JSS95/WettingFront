.. _plugin:

Writing plugins
===============

.. currentmodule:: wettingfront

By writing a plugin, you can define your own analysis routines and specify them
in your configuration file.

.. note::

    If you are not familiar with plugins and entrypoints, you may want to read
    `Python packaging guide <https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/>`_
    and `Setuptools documentation <https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`_
    first.

Analyzer
--------

Let us suppose that we want to implement an analysis type ``Foo`` for the
following configuration file entry:

.. code-block:: yaml

    foo:
        type: Foo
        ...

For this, we can write a simple plugin named ``wettingfront-foo``.
The package structure will be::

    wettingfront-foo
    ├── pyproject.toml
    └── foo.py

In ``foo.py`` we define:

.. code-block:: python

    def foo_analyzer(k: str, v: dict):
        ... # do whatever you want

The signature of analyzer is specified in :func:`analyze_files`.
Then, in ``pyproject.toml`` we define a table to register
:func:`foo_analyzer` to ``Foo``:

.. code-block:: toml

    [project.entry-points."wettingfront.analyzers"]
    Foo = "foo:foo_analyzer"

Now, by installing the ``wettingfront-foo`` package, the analysis type ``Foo``
will be recognized.

Models
------

During the analysis, you are likely to interpret the data using models
describing rate of penetration, such as :func:`~.models.fit_washburn`.
Instead of using default models, you can define your own by writing plugin.

With the package structure described above, in ``foo.py`` we define:

.. code-block:: python

    def my_model(t, x):
        ... # define your model

and register an entry point in ``pyproject.toml``:

.. code-block:: toml

    [project.entry-points."wettingfront.models"]
    MyModel = "foo:my_model"

Note that the model must strictly adhere to the prescribed function signature.

Arguments
^^^^^^^^^

1. array_like (shape ``(M,)``)
    Timestamp.
2. array_like (shape ``(M,)``)
    Penetration length.

Returns
^^^^^^^

1. Prediction function (callable)
    Takes 1-D timestamp and returns predicted penetration length.
2. Fitted parameters (tuple)

Samples
-------

As shown in :ref:`tutorial`, WettingFront supports :ref:`'wettingfront samples'
<command-reference>` command to print the path to the directory where sample
files are stored. If your plugin has its own sample directory, you can
register it to the same API.

To distribute the sample files as package data, the ``wettingfront-foo``
needs to be a little more complicated::

    wettingfront-foo
    ├── pyproject.toml
    ├── MANIFEST.in
    └── src
        └── foo
            ├── samples
            └── __init__.py

Make sure that the sample directory is included in ``MANIFEST.in``.
Then, in ``__init__.py`` we define:

.. code-block:: python

    from importlib.resources import files

    def sample_path():
        return str(files("wettingfront-foo").joinpath("samples"))

And in ``pyproject.toml`` we define a table:

.. code-block:: toml

    [project.entry-points."wettingfront.samples"]
    foo = "foo:sample_path"

Then, invoking ``wettingfront samples foo`` will print the path to
the samples directory.
Note that :func:`sample_path` can have different signature as long as it
returns the correct path when called with empty argument.
