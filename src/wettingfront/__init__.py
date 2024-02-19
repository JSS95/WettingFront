"""Package to analyze wetting front data.

To analyze with command line, specify the parameters in configuration file(s) and run::

    wettingfront analyze <file1> [<file2> ...]
"""

import argparse
import csv
import json
import logging
import os
import sys
from typing import Callable, Tuple

import numpy as np
import yaml
from scipy.optimize import curve_fit, root  # type: ignore[import-untyped]

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
    from importlib_resources import files
else:
    from importlib.metadata import entry_points
    from importlib.resources import files

__all__ = [
    "get_sample_path",
    "analyze_files",
    "fit_washburn",
    "fit_washburn_rideal",
]


def get_sample_path(*paths: str) -> str:
    """Get path to sample file.

    Arguments:
        paths: Subpaths under ``wettingfront/samples/`` directory.

    Returns:
        Absolute path to the sample file.

    Examples:
        >>> from wettingfront import get_sample_path
        >>> get_sample_path() # doctest: +SKIP
        'path/wettingfront/samples'
        >>> get_sample_path("myfile") # doctest: +SKIP
        'path/wettingfront/samples/myfile'
    """
    return str(files("wettingfront").joinpath("samples", *paths))


def analyze_files(*paths: str) -> bool:
    """Perform analysis from configuration files.

    Supported formats:
        * YAML
        * JSON

    Each file can have multiple entries. Each entry must have ``type`` field which
    specifies the analyzer. Analyzers are searched from entry point group
    ``"wettingfront.analyzers"``, and must have the following signature:

    * :obj:`str`: entry name
    * :obj:`dict`: entry fields

    For example, the following YAML file contains ``foo`` entry which is analyzed by
    ``Foo`` analyzer. The analyzer is loaded by searching an entry point whose name is
    ``Foo``.

    .. code-block:: yaml

        foo:
            type: Foo
            ...

    Arguments:
        paths: Configuration file paths.

    Returns:
        Whether the analysis is finished without error.
    """
    # load analyzers
    ANALYZERS = {}
    for ep in entry_points(group="wettingfront.analyzers"):
        ANALYZERS[ep.name] = ep.load()

    ok = True
    for path in paths:
        path = os.path.expandvars(path)
        _, ext = os.path.splitext(path)
        ext = ext.lstrip(os.path.extsep).lower()
        try:
            with open(path, "r") as f:
                if ext == "yaml" or ext == "yml":
                    data = yaml.load(f, Loader=yaml.FullLoader)
                elif ext == "json":
                    data = json.load(f)
                else:
                    logging.error(f"Skipping file: '{path}' (format not supported)")
                    ok = False
                    continue
        except FileNotFoundError:
            logging.error(f"Skipping file: '{path}' (does not exist)")
            ok = False
            continue
        for k, v in data.items():
            try:
                typename = v["type"]
                analyzer = ANALYZERS.get(typename, None)
                if analyzer is not None:
                    analyzer(k, v)
                else:
                    logging.error(
                        f"Skipping entry: '{path}::{k}' (unknown type: '{typename}')"
                    )
            except Exception:
                logging.exception(f"Skipping entry: '{path}::{k}' (exception raised)")
                ok = False
                continue
    return ok


def fit_washburn(t, L) -> Tuple[Callable, Tuple[np.float64, np.float64, np.float64]]:
    r"""Fit data to Washburn's equation [#f1]_.

    The data are fitted to:

    .. math::

        L = k \sqrt{t}

    where :math:`k` is penetrativity of the liquid.

    Arguments:
        t (array_like, shape (M,)): Time.
        L (array_like, shape (M,)): Penetration length.

    Returns:
        func
            Washburn equation function f(t, k).
        (k,)
            Argument for *func*.

    .. [#f1] Washburn, E. W. (1921). The dynamics of capillary flow.
             Physical review, 17(3), 273.
    """

    def func(t, k):
        return k * np.sqrt(t)

    ret, _ = curve_fit(func, t, L)
    return func, ret


def fit_washburn_rideal(
    t, z
) -> Tuple[Callable, Tuple[np.float64, np.float64, np.float64]]:
    r"""Fit data to Washburn-Rideal equation [#f2]_.

    The data are fitted to:

    .. math::

        t = \frac{\alpha}{2\beta}z^2 - \frac{1}{\alpha}\ln{\frac{\alpha}{\sqrt{\beta}}z}

    where :math:`\alpha` and :math:`\beta` denotes the ratios of viscous drag,
    surface tension and inertial force [#f3]_.

    Arguments:
        t (array_like, shape (M,)): Time.
        z (array_like, shape (M,)): Penetration length.

    Returns:
        func
            Washburn-Rideal equation function f(t, alpha, beta).
        (alpha, beta)
            Arguments for *func*.

    .. [#f2] Rideal, E. K. (1922). CVIII. On the flow of liquids under capillary
             pressure. The London, Edinburgh, and Dublin Philosophical Magazine and
             Journal of Science, 44(264), 1152-1159.

    .. [#f3] Levine, S., & Neale, G. H. (1975). Theory of the rate of wetting of a
             porous medium. Journal of the Chemical Society, Faraday Transactions 2:
             Molecular and Chemical Physics, 71, 12-21.
    """

    def washburn(t, a, b):
        return np.sqrt(2 * b / a * t)

    def washburn_rideal(z, a, b):
        return np.piecewise(
            z,
            [z > 0, z == 0],
            [lambda z: a / 2 / b * z**2 - 1 / a * np.log(a / np.sqrt(b) * z), 0],
        )

    ret, _ = curve_fit(washburn_rideal, z, t)

    def func(t):
        t = np.array(t)
        return root(lambda z: washburn_rideal(z, *ret) - t, washburn(t, *ret)).x

    return func, ret


def unidirect_analyzer(k, v):
    """Image analysis for unidirectional liquid imbibition in porous medium.

    .. note::

        To evoke this analyzer, you need ``img`` optional dependency::

            pip install wettingfront[img]

    Unidirectional analyzer detects the horizontal wetting front in the image by
    pixel intensities and fits the data using :func:`fit_washburn`.

    The analyzer defines the following fields in configuration entry:

    - **path** (`str`): Path to the input video file.
    - **output-vid** (`str`, optional): Path to the output video file.
    - **output-data** (`str`, optional): Path to the output csv file.

    The output csv file contains three colums; time, wetting height, and fitted
    wetting height. The time unit is seconds and the distance unit is pixels.

    The following is the example for an entry in YAML configuration file:

    .. code-block:: yaml

        foo:
            type: Unidirectional
            path: foo.mp4
            output-vid: output/foo.mp4
            output-data: output/foo.csv
    """
    import imageio.v3 as iio

    # Prepare output
    path = os.path.expandvars(v["path"])
    out_vid = v.get("output-vid")
    out_data = v.get("output-data")
    if out_vid:
        out_vid = os.path.expandvars(v["output-vid"])
        dirname, _ = os.path.split(out_vid)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
    if out_data:
        out_data = os.path.expandvars(v["output-data"])
        dirname, _ = os.path.split(out_data)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

    def yield_result(path):
        for frame in iio.imiter(path, plugin="pyav"):
            gray = np.dot(frame, [0.2989, 0.5870, 0.1140])
            h = np.argmax(np.abs(np.diff(np.mean(gray, axis=1))))
            frame[h, :] = (255, 0, 0)
            yield frame, int(frame.shape[0] - h)

    # Get data (and write video)
    immeta = iio.immeta(path, plugin="pyav")
    fps = immeta["fps"]
    heights = []
    gen = yield_result(path)
    if out_vid:
        codec = immeta["codec"]
        with iio.imopen(out_vid, "w", plugin="pyav") as out:
            out.init_video_stream(codec, fps=fps)
            for frame, h in gen:
                out.write_frame(frame)
                heights.append(h)
    elif out_data:
        for frame, h in gen:
            heights.append(h)

    # write data
    if out_data:
        times = np.arange(len(heights)) / fps
        func, (k,) = fit_washburn(times, heights)
        washburn = func(times, k)

        with open(out_data, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time (s)", "height (pixels)", "fitted height (pixels)"])
            for t, h, w in zip(times, heights, washburn):
                writer.writerow([t, h, w])


def main():
    """Entry point function."""
    parser = argparse.ArgumentParser(
        prog="wettingfront",
        description="Wetting front analysis.",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="set logging level",
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

    loglevel = args.log_level.upper()
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)8s] --- %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=loglevel,
    )

    logging.debug(f"Input command: {' '.join(sys.argv)}")

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
            else:
                logging.error(f"Unknown plugin: '{args.plugin}'")
                sys.exit(1)
    elif args.command == "analyze":
        ok = analyze_files(*args.file)
        if not ok:
            sys.exit(1)
