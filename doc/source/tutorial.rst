.. _tutorial:

Tutorial
========

.. currentmodule:: wettingfront

.. note::

    To run this tutorial, you need ``img`` optional dependency::

        pip install wettingfront[img]

    Additionally, environment variable ``$WETTINGFRONT_SAMPLES`` must be set:

    .. tabs::

        .. code-tab:: bash

            export WETTINGFRONT_SAMPLES=$(wettingfront samples)

        .. code-tab:: bat cmd

            FOR /F %G IN ('wettingfront samples') DO SET WETTINGFRONT_SAMPLES=%G

        .. code-tab:: powershell

            $env:WETTINGFRONT_SAMPLES=$(wettingfront samples)

    Check if the variable is properly set.
    The output of ``wettingfront samples`` command should be same as the result of:

    .. tabs::

        .. code-tab:: bash

            echo $WETTINGFRONT_SAMPLES

        .. code-tab:: bat cmd

            echo %WETTINGFRONT_SAMPLES%

        .. code-tab:: powershell

            echo $env:WETTINGFRONT_SAMPLES

Download :download:`example.yml` file in your local directory.
The contents of this configuration file are:

.. literalinclude:: example.yml
    :language: yaml

Running the following command will start the analysis::

    wettingfront analyze config.yml

Result:

.. raw:: html

    <video controls width="320" height="256">
        <source src="_static/example.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>

Configuration file format
-------------------------

Configuration file can be in other formats as well.
The following :download:`example.json` file is equivalent to
:download:`example.yml`:

.. literalinclude:: example.json
    :language: json

.. note::

    Refer to the :ref:`config-reference` page for more information about the
    configuration file and the supported analysis types.

