"""
Module diffraction_test.py

Defines the function 'diffraction_significance' which performs a Rayleigh distribution
test to determine if aberrations are more significant than diffraction. Rayleigh was
chosen due to rotationally a symmetric beam about the optical axis.

H0: Observed spread is diffraction-limited. 
H1: Observed spread exceeds diffraction-limited regime, so aberrations dominate.

Author: Aedan M. Bullen
Date: 23/04/2025

"""
import numpy as np
from scipy.stats import rayleigh

def diffraction_significance(ray_bundle, wavelength,
                              focal_length, rmax, alpha=0.05):
    """
    Determines whether aberrations are statistically significan over diffraction.

    Args:
        ray_bundle (RayBundle): Ray bundle propagated.
        wavelength (float): Wavelength of light.
        focal_length (float): Focal length of element.
        rmax (foat): Maximum radius of ray bundle.
        alpha (float): significance level.

    Returns:
        tuple: (p_value, significant).
        p_value: (float): Probability of seeing RMS <= diffraction scale for H0.
        significant? (bool): True if p_value < alpha.
    """

    diff_theoretical = (wavelength * focal_length) / (2 * rmax)
    rms = ray_bundle.rms()

    sigma = diff_theoretical / np.sqrt(2)  # Rayleigh scale for RMS

    p_value = 1 - rayleigh.cdf(rms, scale=sigma)
    return p_value, (p_value < alpha)
