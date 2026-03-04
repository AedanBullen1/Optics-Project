"""
Module elements.py

Defines the class 'OpticalElement' which serves as a base class for all optical elements.
Defines the class 'SphericalRefraction' which simulates a spherical lens.
Defines the class 'SphericalReflection' which simulates a spherical mirror.

Author: Aedan M. Bullen
Date of creation: 24/04/2025


"""

import numpy as np
from raytracer.physics import refract, reflect

class OpticalElement:
    """
    Base class for all optical elements (derived classes) in the ray tracer model.

    This class defines how all optical elements must be implemented.
    It shouldn't be instantiated itself, but rather be used as a parent class
    for more specific optical components.

    Methods:
        intercept(ray): Finds intersection point for ray passing through an optical element.
        propagate(ray): Computes how ray propagates through element.

    """
    def intercept(self, ray):  # does the ray hit element?
        """
        Computes the intersection point for a ray passing through an optical element.

        Args:
            ray (Ray): Ray whose intersection point we want.

        Raises:
            NotImplementedError: When called from the base class instead of from a derived class.

        """
        raise NotImplementedError('intercept() needs to be implemented in derived classes')

    def propagate_ray(self, ray):  # how does the ray emerge from element?
        """
        Computes how a ray propagates through an optical element.

        Args:
            ray (Ray): Ray that is to be propagated through the element

        Raises:
            NotImplementedError: When called from the base class instead of from a derived class.
        """
        raise NotImplementedError('propagate_ray() needs to be implemented in derived classes')

class Intercept:
    """
    Base class for calculating intercepts between rays and surfaces, as well as initialising
    subclasses and finding normals.

    Not to be directly instantiated.

    Attributes:
            z_0 (float): z-coordinate of front of lens.
            aperture (float): Aperture radius.
            curvature (float): Curvature of convex surface.
            n_1 (float): Refractive index of first medium.
            n_2 (float): Refractive index of second medium.

    Methods:
        z_0(): Returns intercept of surface with the optical axis.
        aperture(): Returns aperture value.
        curvature(): Returns surface curvature.
        n_1(): Returns refractive index of first medium
        n_2(): Returns refractive index of second medium.
        intercept(ray): Calculates the intersection point.
        planar_intercept(): Calculates intersection point for plane.
        spherical_intercept: Calculates the intersection point for spherical surface.
        surface_normal: Calculates the surface normal for use in propagation.


    """

    def __init__(self, z_0, aperture, curvature, n_1, n_2):
        """
        Initialises intercept class.

        Args:
            z_0 (float): The intercept of the surface with the axis.
            aperture (float): The maximum extent of the surface from the optical axis
            curvature (float): The curvature of the surface (a signed quantity with magnitude
                1/(radius of curvature)).
            n_1 (float): Refractive index of first medium.
            n_2 (float): Refractive index of second medium.

        Returns:
            None

        """
        self._z_0 = z_0
        self._aperture = aperture
        self._curvature = curvature
        self._n_1 = n_1
        self._n_2 = n_2  # have to use single underscore due to inheritance

    def z_0(self):  # accessor methods
        """
        Returns intercept of the surface with the axis.

        Returns:
            float: The intercept of the surface with the optical axis.
        """
        return self._z_0

    def aperture(self):
        """
        Returns the aperture of the surface.

        Returns:
            float: The maximum extent of the surface from the optical axis

        """
        return self._aperture

    def curvature(self):
        """
        Returns the curvature of the surface.

        Returns:
            float: The curvature of the surface (a signed quantity with magnitude
                1/(radius of curvature)).

        """
        return self._curvature

    def n_1(self):
        """
        Returns the refractive index of medium 1.

        Returns:
            float: Refractive index of medium 1.

        """
        return self._n_1

    def n_2(self):
        """
        Returns the refractive index of medium 2.

        Returns:
            float: Refractive index of medium 2.

        """
        return self._n_2

    def intercept(self, ray):
        """
        Finds the intersection point for a ray with a surface.

        Args:
            ray (Ray): Ray whose intersection point is to be found.

        Returns:
            numpy.ndarray or None: Point of intersection or None if no point is found.

        """

        if self._curvature is None or self._curvature == 0.0:
            return self.planar_intercept(ray)

        return self.spherical_intercept(ray)


    def planar_intercept(self, ray):
        """
        Finds the intersection point for a ray with a plane.

        Args:
            ray (Ray): Ray whose intersection point is to be found.

        Returns:
            numpy.ndarray or None: Point of intersection or None if no point is found.

        """

        point_interception = None
        r0 = ray.pos()
        direc = ray.direc()

        if direc[2] != 0:
            param = (self._z_0 - r0[2]) / direc[2]
            if param >= 0:
                point = r0 + param * direc
                if (
                    self._aperture is None or
                    np.dot(point[:2], point[:2]) <= self._aperture * self._aperture
                    # in case ray not within
                ):
                    point_interception = point
        return point_interception


    def spherical_intercept(self, ray):
        """
        Finds the intersection point for a ray with a spherical surface.

        Args:
            ray (Ray): Ray whose intersection point is to be found.

        Returns:
            numpy.ndarray or None: Point of intersection or None if no point is found.

        """
        point_interception = None
        r0 = ray.pos()
        direc = ray.direc()


        centre = np.array([0.0, 0.0, self._z_0 + 1.0 / self._curvature])
        r_point = r0 - centre

        dotprod_r_direc = np.dot(r_point, direc)
        dotprod_r_r = np.dot(r_point, r_point)

        discrim = dotprod_r_direc * dotprod_r_direc - (dotprod_r_r - (1.0 / self._curvature) ** 2)

        if discrim >= 0:
            sqrt_discrim = np.sqrt(discrim)

            l_positive = -dotprod_r_direc + sqrt_discrim
            l_negative = -dotprod_r_direc - sqrt_discrim

            if self._curvature > 0:
                chosen_l = min((l for l in (l_positive, l_negative) if l > 0), default=None)
            else:
                chosen_l = max((l for l in (l_positive, l_negative) if l > 0), default=None)
            # default to deal with no +ve roots

            if chosen_l is not None:
                point = r0 + chosen_l * direc
                if (
                    self._aperture is None or
                    np.dot(point[:2], point[:2]) <= self._aperture * self._aperture
                ):
                    point_interception = point

        return point_interception

    def surface_normal(self, point):
        """
        Calculates the surface normal unit vector for use in propagate_ray methods.

        Args:
            point (numpy.ndarray): Intersection point on the surface for the ray.

        Returns:
            numpy.ndarray: Normalised surface normal vector.

        """
        if self._curvature == 0.0:
            return np.array([0.0, 0.0, -1.0])

        centre = np.array([0.0, 0.0, self._z_0 + 1 / self._curvature])

        if self._curvature > 0:
            normal = point - centre
        else:
            normal = centre - point

        return normal / np.linalg.norm(normal)


class SphericalRefraction(Intercept, OpticalElement):
    """
    A spherical refracting surface centred on the optical axis (z-axis).

    Attributes:
        z_0 (float): The intercept of the surface with the axis.
        aperture (float): The maximum extent of the surface from the optical axis
        curvature (float): The curvature of the surface (a signed quantity with magnitude
            1/(radius of curvature)).
        n_1 (float): Refractive index of first medium.
        n_2 (float): Refractive index of second medium.

    Methods:
        __repr__(): Returns human-readable represenation of object.
        propagate_ray(ray): Propagates ray through spherical surface.
        focal_point(): Locates the focal point of the spherical surface.


    """

    def __repr__(self):
        """
        Returns a human-readable string version of the spherical refraction instance.

        Returns:
            str: String of the following properties of the optical element: z-axis position,
            aperture, curvature, refractive index of medium 1, refractive index of medium 2.

        """
        return(f'SphericalRefraction(z_0={self._z_0}, aperture={self._aperture},'
               f'curvature={self._curvature},'
               f'n_1={self._n_1}, n_2={self._n_2})')

    def propagate_ray(self, ray):
        """
        Propagates a ray through the spherical surface.

        Using a calculated intercept point, this method finds the surface normal at that
        point and applies Snell's law to determine the emergent ray direction in medium two.
        No valid intersection will not append any points to the ray's path.

        Args:
            ray (Ray): Ray object that is to be propagated. Position and direction via 'ray.pos()'
            and 'ray.direc()'. 'ray.append(position, direction)' also used to add point to ray path.

        Returns:
            None: Ray not modified if no intersection.
            ray.append(): Emerging direction added to ray using this appending method.


        """

        intercept = self.intercept(ray)
        if intercept is None:
            return # don't append

        direc = ray.direc()

        normal = self.surface_normal(intercept)

        emergent_direction = refract(direc, normal, self._n_1, self._n_2)
        if emergent_direction is None:
            return


        ray.append(intercept, emergent_direction)

    def focal_point(self):
        """
        Returns focal point of spherical surface as a z-axis coordinate in the paraxial
        approximation.

        Returns:
            float: The z-coordinate position of the focal point, also accounting for
            the infinite case of a planar surface.
        """

        if self._curvature == 0:
            return np.inf  # is this right ?

        radius = 1 / self._curvature
        focal = (self._n_2 * radius) / (self._n_2 - self._n_1)
        focal_z = self._z_0 + focal
        return focal_z


class OutputPlane(Intercept, OpticalElement):
    """
    Output plane at certain z-position. This is the last point in a ray.

    Records position where ray intersects a planar surface (infinite surface). It does not
    modify the ray direction.

    Attributes:
        z_0 (float): z-coordinate of output plane.

    """

    def __init__(self, z_0):
        """
        Initialises OutputPlane.

        Args:
            z_0 (float): z-coordinate of output plane.

        Returns:
            None


        """
        super().__init__(z_0, aperture=None, curvature=None, n_1=None, n_2=None)

    def propagate_ray(self, ray):
        """
        Propagates ray to output plane, then appends intercept between ray and plane without
        changing the ray's direction.

        Args:
            ray (Ray): Ray that is to be propagated.

        Returns:
            ray (Ray): Ray that has been propagated.
            None: if no intercept.


        """
        direc = ray.direc()

        intercept = self.intercept(ray)

        if intercept is not None:
            ray.append(intercept, direc)
            return ray

        return None

class SphericalReflection(Intercept, OpticalElement):
    """
    A spherical reflecting surface centred on the optical axis (z-axis).

    Attributes:
        z_0 (float): The intercept of the surface with the axis.
        aperture (float): The maximum extent of the surface from the optical axis
        curvature (float): The curvature of the surface (a signed quantity with magnitude
            1/(radius of curvature)).

    Methods:
        __repr__(): Returns human-readable represenation of object.
        propagate_ray(ray): Propagates ray through spherical surface.
        focal_point(): Locates the focal point of the spherical surface.


    """

    def __init__(self, z_0, aperture, curvature):
        """
        Initialises reflecting surface.

        Args:
            z_0(): Intercept of surface with the optical axis.
            aperture(): Aperture value.
            curvature(): Surface curvature.

        Returns:
            None

        """

        super().__init__(z_0, aperture, curvature, n_1=1.0, n_2=1.0)


    def __repr__(self):
        """
        Returns a human-readable string version of the spherical reflection instance.

        Returns:
            str: String of the following properties of the optical element: z-axis position,
            aperture, curvature, refractive index of medium 1, refractive index of medium 2.

        """
        return(f'SphericalReflection(z_0={self._z_0}, aperture={self._aperture},'
               f'curvature={self._curvature})')



    def propagate_ray(self, ray):
        """
        Propagates ray through reflecting surface, then appends intercept between ray and surface
        without changing the ray's direction.

        Args:
            ray (Ray): Ray that is to be propagated.

        Returns:
            None


        """

        intercept = self.intercept(ray)
        if intercept is None:
            return

        direc = ray.direc()

        normal = self.surface_normal(intercept)

        emergent_direction = reflect(direc, normal)

        if emergent_direction is None:
            return

        ray.append(intercept, emergent_direction)


    def focal_point(self):
        """
        Returns focal point of the mirror.

        Returns:
            float: The focal point value.

        """

        if self._curvature == 0:
            return np.inf


        radius = 1 / self._curvature
        return self._z_0 + radius / 2
