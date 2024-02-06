.. _config-reference:

Configuration file reference
============================

.. currentmodule:: wettingfront

A configuration file consists of multiple entries representing individual
sets of analysis.

For example, the following YAML file defines two entries whose names are
``data1`` and ``data2``:

.. code-block:: YAML

    data1:
        type: ...
        ...

    data2:
        type: ...
        ...

``type`` is a mandatory field which specifies the analyzer registered by
:func:`~.register_analyzer`. Depending on the analyzer, entries may need to have
additional fields.

This document includes the docstrings for each analyzer which specifies the
required fields.

Basic
-----

.. autofunction:: wettingfront.basic_analyzer
