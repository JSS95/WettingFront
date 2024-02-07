# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import shutil
import subprocess

import yaml

from wettingfront import get_sample_path

os.environ["WETTINGFRONT_SAMPLES"] = get_sample_path()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "WettingFront"
copyright = "2024, Jisoo Song"
author = "Jisoo Song"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "sphinx_tabs.tabs",
    "matplotlib.sphinxext.plot_directive",
]

templates_path = ["_templates"]
exclude_patterns = []  # type: ignore

autodoc_typehints = "description"

autoapi_dirs = ["../../src"]
autoapi_template_dir = "_templates/autoapi"
autoapi_root = "reference"


def autoapi_skip(app, what, name, obj, skip, options):
    if what == "module" and name in [
        "wettingfront.__main__",
    ]:
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", autoapi_skip)


intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
    "pip": ("https://pip.pypa.io/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "mypy": ("https://mypy.readthedocs.io/en/stable/", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = "WettingFront"
html_static_path = ["_static"]

plot_html_show_formats = False
plot_html_show_source_link = False

# -- Custom scripts ----------------------------------------------------------

# Tutorial files

with open("example.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

subprocess.call(
    [
        "wettingfront",
        "analyze",
        "example.yml",
    ],
)

os.makedirs(html_static_path[0], exist_ok=True)
shutil.copy("output/example.mp4", "_static/example.mp4")

# Reference file

f = open("help-wettingfront.txt", "w")
subprocess.call(["wettingfront", "-h"], stdout=f)
f.close()

f = open("help-wettingfront-samples.txt", "w")
subprocess.call(["wettingfront", "samples", "-h"], stdout=f)
f.close()

f = open("help-wettingfront-analyze.txt", "w")
subprocess.call(["wettingfront", "analyze", "-h"], stdout=f)
f.close()
