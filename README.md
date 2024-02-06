# WettingFront - Wetting front image analysis

[![Build Status](https://github.com/JSS95/wettingfront/actions/workflows/ci.yml/badge.svg)](https://github.com/JSS95/wettingfront/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/wettingfront/badge/?version=latest)](https://wettingfront.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/JSS95/wettingfront)](https://github.com/JSS95/wettingfront/blob/master/LICENSE)

WettingFront provides an extensible framework to detect and analyze the wetting front by image analysis.

## Usage

Store the analysis parameters in configuration files and pass to the command:

```
$ wettingfront analyze config1.yml conf2.yml ...
```

Refer to the documentation to learn more about the configuration file.

## Installation

```
$ pip install git+https://github.com/JSS95/wettingfront.git
```

## Documentation

Wettingfront is documented with [Sphinx](https://pypi.org/project/Sphinx/).
Documentation can be found on Read the Docs:

> https://wettingfront.readthedocs.io

If you want to build the document yourself, get the source code and install with `[doc]` option.
Then go to `doc` directory and build the document.

```
$ pip install .[doc]
$ cd doc
$ make html
```

Document will be generated in `build/html` directory. Open `index.html` to see the central page.
