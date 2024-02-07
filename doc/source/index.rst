.. WettingFront documentation master file, created by
   sphinx-quickstart on Tue Feb  6 12:26:23 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to WettingFront's documentation!
========================================

.. plot::
   :context: reset

   from wettingfront import get_sample_path
   import pandas, matplotlib.pyplot as plt, imageio.v3 as iio
   df = pandas.read_csv("output/example.csv")
   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
   for sp in ax1.spines:
       ax1.spines[sp].set_visible(False)
   ax1.xaxis.set_visible(False)
   ax1.yaxis.set_visible(False)
   ax1.imshow(iio.imread(get_sample_path("example.jpg")))
   ax2.plot(df["time (s)"], df["height (pixels)"], label="data")
   ax2.plot(df["time (s)"], df["fitted height (pixels)"], "--", label="model")
   ax2.set_xlabel("time (s)")
   ax2.set_ylabel("height (pixels)")
   ax2.legend()
   fig.tight_layout()

WettingFront is a Python package to visualize and analyze the wetting front.

The advantages of WettingFront are:

* Provides simple image analysis scheme.
* Good extensibility.
* Written in pure Python.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   tutorial
   reference/index
   explanation/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
