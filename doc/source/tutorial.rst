.. _tutorial:

Tutorial
========

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

Running the following command will analyze ``entry1``::

    wettingfront analyze example.yml -e entry1

Result (``example1.mp4``):

.. raw:: html

    <video controls width="320" height="256">
        <source src="_static/example1.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>

The output csv file contains the wetting height and its result of fitting to
`Washburn's equation <https://en.wikipedia.org/wiki/Washburn%27s_equation>`_.

.. plot::
    :include-source:
    :context: reset

    import pandas, matplotlib.pyplot as plt
    df = pandas.read_csv("output/example1.csv")
    plt.plot(df["time (s)"], df["height (pixels)"], label="data")
    plt.plot(df["time (s)"], df["fitted height (pixels)"], "--", label="model")
    plt.xlabel("time (s)")
    plt.ylabel("height (pixels)")
    plt.legend()

However, since the video acquisition did not start simultaneously with the
imbibition, the fitting do not seem to agree well.
To compensate this offset, ``entry2`` adopts a modified equation.

Running the following command will analyze ``entry2``::

    wettingfront analyze example.yml -e entry2

.. note::

    You can analyze every entry by not specifying any entry at all.

The result is now better.

.. plot::
    :include-source:
    :context: close-figs

    df = pandas.read_csv("output/example2.csv")
    plt.plot(df["time (s)"], df["height (pixels)"], label="data")
    plt.plot(df["time (s)"], df["fitted height (pixels)"], "--", label="model")
    plt.xlabel("time (s)")
    plt.ylabel("height (pixels)")
    plt.legend()
