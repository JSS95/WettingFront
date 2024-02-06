"""Image analysis for wetting front experiment.

To analyze with command line, specify the parameters in configuration file(s) and run::

    wettingfront analyze <file1> [<file2> ...]
"""

import argparse
import json
import os
import sys

import yaml

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
    from importlib_resources import files
else:
    from importlib.metadata import entry_points
    from importlib.resources import files

__all__ = [
    "get_sample_path",
    "analyze_files",
]


def get_sample_path(*paths: str) -> str:
    """Get path to sample file.

    Arguments:
        paths: Subpaths under ``wettingfront/samples/`` directory.

    Returns:
        Absolute path to the sample file.

    Examples:
        >>> get_sample_path() # doctest: +SKIP
        'path/wettingfront/samples'
        >>> get_sample_path("myfile") # doctest: +SKIP
        'path/wettingfront/samples/myfile'
    """
    sample_path = files("wettingfront.samples")
    if not paths:
        return str(sample_path._paths[0])  # type: ignore[attr-defined]
    return str(sample_path.joinpath(*paths))


def analyze_files(*paths: str):
    """Perform analysis from configuration files.

    Configuration files can be YAML or JSON. Top-level entries in each file are
    sequentially analyzed. Each entry must have ``type`` field which specifies the
    analyzer registered by :func:`register_analyzer`. Other fields may be required by
    the analyzer.

    For example, the following YAML file contains two entries: ``foo`` and ``bar``. Each
    entry can be analyzed by registering an analyzer with ``Foo`` or ``Bar``.

    .. code-block:: yaml

        foo:
            type: Foo
            ...
        bar:
            type: Bar
            ...

    Arguments:
        paths: Configuration file paths.
    """
    # load analyzers
    ANALYZERS = {}
    for ep in entry_points(group="wettingfront.analyzers"):
        ANALYZERS[ep.name] = ep.load()

    for path in paths:
        _, ext = os.path.splitext(path)
        ext = ext.lstrip(os.path.extsep).lower()
        try:
            with open(path, "r") as f:
                if ext == "yaml" or ext == "yml":
                    data = yaml.load(f, Loader=yaml.FullLoader)
                elif ext == "json":
                    data = json.load(f)
                else:
                    print(f"Skipping {path} ({ext} not supported)")
        except FileNotFoundError:
            print(f"Skipping {path} (path does not exist)")
            continue
        for k, v in data.items():
            try:
                typename = v["type"]
                analyzer = ANALYZERS.get(typename, None)
                if analyzer is None:
                    raise ValueError("Analysis type '%s' is not registered." % typename)
                analyzer(k, v)
            except Exception as err:
                print(f"Skipping {k} ({type(err).__name__}: {err})")
                continue


def unidirect_analyzer(k, v):
    """Image analysis for unidirectional liquid imbibition in porous medium.

    .. note::

        To evoke this analyzer, you need ``img`` optional dependency::

            pip install wettingfront[img]

    In configuration file, the entry must have the following sub-fields:

    - **path** (`str`): Path to the input video file.
    - **output** (`str`): Path to the output video file.

    The following is the example for an YAML entry:

    .. code-block:: yaml

        foo:
            type: Unidirectional
            path: foo.mp4
            output: output/foo.mp4
    """
    import imageio.v3 as iio
    import numpy as np

    path = os.path.expandvars(v["path"])
    output = os.path.expandvars(v["output"])
    dirname, _ = os.path.split(output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    immeta = iio.immeta(path, plugin="pyav")
    fps = immeta["fps"]
    codec = immeta["codec"]
    with iio.imopen(output, "w", plugin="pyav") as out:
        out.init_video_stream(codec, fps=fps)

        for frame in iio.imiter(path, plugin="pyav"):
            gray = np.dot(frame, [0.2989, 0.5870, 0.1140])
            h = np.argmax(np.abs(np.diff(np.mean(gray, axis=1))))
            frame[h, :] = (255, 0, 0)
            out.write_frame(frame)


def main():
    """Entry point function."""
    parser = argparse.ArgumentParser(
        prog="wettingfront",
        description="Image analysis tool to visually detect wetting front.",
    )
    subparsers = parser.add_subparsers(dest="command")

    parser_samples = subparsers.add_parser(
        "samples",
        description="Print path to sample directory.",
        help="print path to sample directory",
    )
    parser_samples.add_argument(
        "plugin",
        type=str,
        nargs="?",
        help="name of the plugin",
    )

    parser_analyze = subparsers.add_parser(
        "analyze",
        description="Parse configuration files and analyze.",
        help="parse configuration files and analyze",
        epilog=(
            "Supported file formats: YAML, JSON.\n"
            "Refer to the package documentation for configuration file structure."
        ),
    )
    parser_analyze.add_argument("file", type=str, nargs="+", help="configuration files")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif args.command == "samples":
        if args.plugin is None:
            print(get_sample_path())
        else:
            for ep in entry_points(group="wettingfront.samples"):
                if ep.name == args.plugin:
                    getter = ep.load()
                    print(getter())
                    break
    elif args.command == "analyze":
        analyze_files(*args.file)
