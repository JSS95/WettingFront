Writing plugins
===============

.. currentmodule:: wettingfront

WettingFront provides extensible API through plugins by entrypoints.
By writing plugins, you can register your own analyzers instead of
those listed in :ref:`config-reference`.

If you are not familiar with plugins and entrypoints, you may want to read
`Python packaging guide <https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/>`_
and `Setuptools documentation <https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`_
first.

For example, let us consider that we want to implement an analysis type
``Foo``, i.e., for the following configuration file entry:

.. code-block:: yaml

    foo:
        type: Foo
        ...

We can write a simple plugin for this. The package structure will be::

    wettingfront-foo
    ├── pyproject.toml
    └── src
        └── wettingfront_foo
            ├── __init__.py
            └── samples

with ``__init__.py`` as:

.. code-block:: python

    def get_sample_path():
        ... # return path to sample directory

    def foo_analyzer(k, v):
        ... # do whatever you want

and ``pyproject.toml`` having a table:

.. code-block:: toml

    [project.entry-points."wettingfront.samples"]
    foo = "wettingfront_foo:get_sample_path"

    [project.entry-points."wettingfront.analyzers"]
    Foo = "wettingfront_foo:foo_analyzer"
