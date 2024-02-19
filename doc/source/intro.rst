Getting started
===============

.. currentmodule:: wettingfront

Installation
------------

WettingFront can be downloaded from `PyPI <https://pypi.org/project/wettingfront/>`_
by using :mod:`pip`::

   pip install wettingfront

You can also install with optional dependencies as::

   pip install wettingfront[img]

Available optional dependencies for WettingFront are:

* ``img``: access to image analysis features.
* ``test``: run tests.
* ``doc``: build documentations.
* ``dev``: every dependency (for development).

Usage
-----

Analysis starts with writing a :ref:`configuration file <config-reference>`,
either as YAML or JSON.

.. code-block:: yaml

   data1:
      type: Unidirectional
      model: Washburn
      path: your-video.mp4
      output-vid: result.mp4
      output-data: result.csv
   data2:
      type: MyType
      my-parameters: ...
   data3:
      ...

The ``type`` field is important.
It defines how the analysis is done and what parameters are required.
You can define and register your own type by writing a :ref:`plugin <plugin>`.

After specifying the parameters in configuration file, pass it to
:ref:`'wettingfront analyze' <command-reference>` command to perform analysis::

   wettingfront analyze config.yml

Refer to :ref:`tutorial` page for a runnable example.
