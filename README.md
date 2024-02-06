# WettingFront

Python package for wetting front image analysis.

## Usage

Analysis can be done by passing configuration files.

```
$ wettingfront analyze config1.yml conf2.yml ...
```

Refer to the documentation to learn more about the configuration file.

## Installation

```
$ pip install git+https://github.com/JSS95/wettingfront.git
```

## Documentation

To build the document yourself, you must download the full source code of the project and install the package with `doc` dependency.

```
$ git clone https://github.com/JSS95/wettingfront.git
$ cd wettingfront
$ pip install .[doc]
```

Then run the following command to build the document.

```
$ cd doc
$ make html
```

Documents will be generated in `doc/build/html` directory.
`index.html` file will lead you to main page.
