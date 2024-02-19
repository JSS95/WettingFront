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
   df1 = pandas.read_csv("output/example1.csv")
   df2 = pandas.read_csv("output/example2.csv")
   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
   for sp in ax1.spines:
       ax1.spines[sp].set_visible(False)
   ax1.xaxis.set_visible(False)
   ax1.yaxis.set_visible(False)
   ax1.imshow(iio.imread(get_sample_path("example.jpg")))
   ax2.plot(df1["time (s)"], df1["height (pixels)"], label="data")
   ax2.plot(df1["time (s)"], df1["fitted height (pixels)"], "--", label="model 1")
   ax2.plot(df2["time (s)"], df2["fitted height (pixels)"], "-.", label="model 2")
   ax2.set_xlabel("time (s)")
   ax2.set_ylabel("height (pixels)")
   ax2.legend()
   fig.tight_layout()

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   tutorial
   plugin
   reference/index
   development

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
