"""Wetting front models."""

from typing import Callable, Tuple

import numpy as np
from scipy.optimize import curve_fit, root  # type: ignore[import-untyped]

__all__ = [
    "fit_washburn",
    "fit_washburn_rideal",
]


def fit_washburn(t, L) -> Tuple[Callable, Tuple[np.float64]]:
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


def fit_washburn_rideal(t, z) -> Tuple[Callable, Tuple[np.float64, np.float64]]:
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
