"""
Module physics.py

Defines function 'refract' which describes the underlying ray physics for lens systems.

Author: Aedan M. Bullen
Date of creation: 24/04/2025

"""
import numpy as np

def refract(direc, normal, n_1, n_2):
    """
    Computes direction of refracted ray emerging from a surface using Snell's law.

    Finds refracted direction vector for a ray passing between media of different refractive
    indices. The indicent direction and surface normal are (if needed, converted to) normalised
    3D NumPy arrays. The normal is assumed to point from the surface to the side where the ray
    is coming from. Total internal reflecition (TIR) will return 'None'.

    Args:
        direc (array or similar): Normalised incident direction of ray.
        normal (array or similar): Normalised surface normal.
        n_1 (float): Refractive index of medium one.
        n_2 (float): Refractive index of medium two.

    Returns:
        np.ndarray or None: Normalised vector that represents the refracted direction vector
        or 'None' if TIR happens.

    Raises:
        Exception: When normal not defined in correct direction

    """
    direc = np.array(direc, dtype=float)
    normal = np.array(normal, dtype=float)

    normal = normal / np.linalg.norm(normal)
    direc = direc / np.linalg.norm(direc)

    costheta_1 = -np.dot(direc, normal)

    ratio = n_1 / n_2

    sintheta_2_squared = ratio * ratio * (1 - costheta_1 * costheta_1)
    sintheta_1 = np.sqrt(1 - costheta_1 * costheta_1)

    if sintheta_1 > 1 / ratio:
        #print('Total internal reflection')
        return None  # TIR


    costheta_2 = np.sqrt(1 - sintheta_2_squared)
    refracted_direc = ratio * direc + (ratio * costheta_1 - costheta_2) * normal

    return refracted_direc / np.linalg.norm(refracted_direc)

def reflect(direc, normal):
    """
    Computes direction of reflected ray emerging from a surface.

    The normal is assumed to point from the surface to the side where the ray is coming from.

    Args:
        direc (array or similar): Normalised incident direction of ray.
        normal (array or similar): Normalised surface normal.

    Returns:
        np.ndarray or None: Normalised vector that represents the refracted direction vector

    """

    direc = np.array(direc, dtype=float)
    normal = np.array(normal, dtype=float)

    normal = normal / np.linalg.norm(normal)
    direc = direc / np.linalg.norm(direc)

    if np.dot(direc, normal) > 0:
        normal = -normal

    costheta_1 = np.dot(direc, normal)
    reflection = direc - 2 * costheta_1 * normal

    reflected_direc = reflection / np.linalg.norm(reflection)
    return reflected_direc
