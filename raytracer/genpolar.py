"""
Module genpolar.py

Defines the function 'rtrings' which generates concentric rings of points
used to generate raybundles.

Author: Aedan M. Bullen
Date of creation: 16/05/2025

"""

import numpy as np


def rtrings(rmax, nrings, multi):
    """
    Generates points arranged in concentric rings. First is always at origin.

    Args:
        rmax (float): Radius of outer ring.
        nrings (int): Number of rings.
        multi (int): Multiplier so that nth ring has n * multi number of
            points.

    Returns:
        list of tuple: List of points in polar coordinates as (radius, angle in
            radians).

    """
    points = [(0.0, 0.0)]
    for i in range(1, nrings + 1):
        radius = rmax * i / nrings
        n_pts = i * multi
        for j in range(n_pts):
            theta = (2 * np.pi / n_pts) * j
            points.append((radius, theta))
    return points
