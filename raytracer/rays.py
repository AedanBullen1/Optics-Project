"""
Module rays.py

Defines the class 'Ray' which represents 3D rays with position and (normalised) direction
vectors.

Creates rays, appends Cartesian points to those rays, and returns data about rays.
Also creates track and spot plots, which help to visualise ray paths.

Author: Aedan M. Bullen
Date: 23/04/2025


"""

import numpy as np
import matplotlib.pyplot as plt
from raytracer.genpolar import rtrings
from raytracer.elements import OpticalElement


class Ray:
    """Represents a 3D ray with position and direction vectors.

    The ray is defined by a series of 3D points stored as a Numpy array (the positions),
    and a normalised direction vector. By default, a new ray starts at the origin and is
    directed along the positive z-axis.

    Attributes:
        __points (list of np.ndarray): List of points that define the ray's path.
        __direc (np.ndarray): Normalised vector that specifies the ray's direction.

    Methods:
        pos(): Returns the current position of the ray.
        direc(): Returns the current direction vector (normalised).
        append(pos, direc): Updates the ray by adding a new point and direction to it.
        vertices(): Returns a copy of the whole list of all the points comprising the ray.


    """
    def __init__(self, pos=None, direc=None):
        """
        Initialises a ray instance.

        Args:
            pos (np.ndarray or list): Initial vector position.
                Defaults to [0.0, 0.0, 0.0]

            direc (np.ndarray or list): Initial vector direction.
            Defaults to [0.0, 0.0, 1.0]

        Raises:
            ValueError: If position or direction don't have three Cartesian components.
            ValueError: If the direction vector is the zero vector.

        """
        if pos is None:
            pos = [0.0, 0.0, 0.0] #default
        if direc is None:
            direc = [0.0, 0.0, 1.0] #default

        pos = np.array(pos, dtype=float)
        direc = np.array(direc, dtype=float)

        self.__direc = np.array(direc, dtype=float)

        if len(pos) != 3: #Exceptions
            raise ValueError('position array must have three Cartesian components')
        if len(direc) != 3:
            raise ValueError('direction array must have three Cartesian components')

        norm = np.linalg.norm(direc) #more efficient
        if norm == 0:
            raise ValueError('direction vector cannot be the zero vector')

        self.__points = [pos]
        self.__direc = direc / norm

    def __repr__(self): #human readable
        """
        Returns a human-readable string version of the ray instance.

        Returns:
            str: String representing the latest position and direction vectors.

        """
        return f"Ray(pos={self.__points[-1]}, direc={self.__direc})"

    def pos(self): #access methods
        """
        Returns the last point of the position vector array

        Returns:
            np.ndarray: The latest position vector.
        """
        return self.__points[-1] #last point in array

    def direc(self):
        """
        Returns the latest direction vector (normalised) for the ray.

        Returns:
            np.ndarray: The latest normalised direction vector.

        """
        return self.__direc

    def append(self, pos, direc):
        """
        Appends another position and direction to the ray.

        Args:
            pos(list or np.ndarray): New position vector
            direc (list or np.ndarray): New direction vector.

        Raises:
            ValueError: If position or direction don't have three Cartesian components.
            ValueError: If the direction vector is the zero vector.

        Returns:
            None

        """
        pos = np.array(pos, dtype=float)
        direc = np.array(direc, dtype=float)

        if len(pos) != 3:
            raise ValueError('position array must have three Cartesian components')
        if len(direc) != 3:
            raise ValueError('direction array must have three Cartesian components')

        norm = np.linalg.norm(direc)
        if norm == 0:
            raise ValueError('direction vector cannot be the zero vector')

        self.__points.append(pos)
        self.__direc = direc / norm

    def vertices(self):
        """
        Returns all points that comprise a ray.

        Returns:
            list of np.ndarray: Copy of the list of position vectors.
        """
        return self.__points.copy()

class RayBundle:
    """
    Represents a ray bundle in concentric rings around the optical axis.

    The class generates rays in polar coordinates. They point along the z-axis, and may be
    propagated through optical elements.

    Attributes:
        __rays (list of Ray): List of Ray objects that make up the bundle.

    Methods:
        propagate_bundle(elements): Propagates rays through list of optical elements.
        track_plot(): Plots trajectories of ray bundles as a z-y plot.
        rms(): Returns root-mean-square spread of a ray bundle.
        spot_plot(): Returns a plot of ray bundle looking down the z-axis.


    """

    def __init__(self, rmax=5., nrings=5, multi=6):
        """
        Initialises RayBundle with certain ray bundle structure.

        Number of rays and rings specified.

        Args:
            rmax (float, optional): Maximum ring radius. Default is 5.0 mm.
            nrings (int, optional): Number of rings. Default is 5.
            multi (int, optional): Multiplier making number of rays per ring increase linearly as
            the number of rings increases.

        """
        self.__rays = []

        for r, theta in rtrings(rmax, nrings, multi):
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            pos = [x, y, 0.0]
            direc = [0.0, 0.0, 1.0]

            self.__rays.append(Ray(pos, direc))

    def propagate_bundle(self, elements):
        """
        Propagates rays in bundle through a list of optical elements.

        Args:
            elements (list of OpticalElement): List of optical elements in order to be
              propagated through.

        Raises:
            TypeError: If an element is not an instance of OpticalElement.

        Returns:
            None
        """

        for element in elements:
            if not isinstance(element, OpticalElement):
                raise TypeError('Needs to be instance of OpticalElement')
            # is element instance of OpticalElement or inheriting class?
            for ray in self.__rays:
                element.propagate_ray(ray)

    def n_rays(self):
        """
        Returns the number of rays in a bundle.

        Returns:
            int: Number of rays in a bundle.
        
        """

        return len(self.__rays)

    def track_plot(self):
        """
        Plots the trajectory of each ray on z-y plot.

        Returns:
            matplotlib.figure.Figure: figure object which is the plot.

        """
        figure = plt.figure()

        for ray in self.__rays:
            points = ray.vertices()
            z = [i[2] for i in points]
            y = [i[1] for i in points]
            plt.plot(z, y)

        plt.xlabel('z ($mm$)', fontsize=14)
        plt.ylabel('y ($mm$)', fontsize=14)
        plt.xlim(left=0)
        plt.grid(True)
        plt.show()

        return figure

    def rms(self):
        """
        Returns the rms (root-mean-square) spread of rays in a bundle about the optical axis.

        Returns:
            float: Value of the rms spread.

        """

        x_positions = []
        y_positions = []

        for ray in self.__rays:
            pos = ray.pos()
            x_positions.append(pos[0])
            y_positions.append(pos[1])

        x_positions = np.array(x_positions)
        y_positions = np.array(y_positions)

        rms = np.sqrt(np.mean(x_positions * x_positions + y_positions * y_positions))
        return rms

    def spot_plot(self, ax=None):

        """
        Creates plot of ray bundle looking down the z-axis (x-y plane).

        Args:
            ax (matplotlib.axes, optional): Axis to plot on

        Returns:
            matplotlib.figure.Figure: Plot of the ray bundle in x-y plane.
        """
        x_positions = []
        y_positions = []

        for ray in self.__rays:
            pos = ray.pos()
            x_positions.append(pos[0])
            y_positions.append(pos[1])

        if ax is None:
            figure, ax = plt.subplots()
            plot_show = True
        else:
            figure = ax.figure
            plot_show = False

        ax.plot(x_positions, y_positions, '.')
        ax.set_xlabel('x ($mm$)', fontsize=14)
        ax.set_ylabel('y ($mm$)', fontsize=14)
        ax.grid(True)

        if plot_show:
            plt.show()

        return figure
