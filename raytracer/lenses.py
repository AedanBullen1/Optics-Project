"""
Module lenses.py

Defines the class 'LensBase', a base class for all lenses.
Defines the class 'PlanoConvex' which models a plano-convex lens.
Defines the class 'ConvexPlano' which models a Convex-Plano lens.
Defines the class 'BiConvex' which models a biconvex lens.

Author: Aedan M. Bullen
Date of creation: 02/06/2025

"""
from raytracer.elements import OpticalElement, SphericalRefraction

class LensBase(OpticalElement):
    """
    Base class for lenses made. (Not to be instantiated.)

    Represents common properties of each lens.

    Args:
        z_0 (float): z-coordinate of front of lens.
        aperture (float): Aperture size of the lens.
        thickness(float): Thickness of lens.
        n_inside (float): Refractive  index of lens material.
        n_outside (float): Refractive index of outside medium.

    Methods:
        z_0(): Returns z-coordinate of lens front.
        aperture(): Returns aperture size.
        thickness(): Returns thickness.
        n_inside(): Returns refractive index of lens material.
        n_outside(): Returns refractive index outside lens.
    """

    def __init__(self, z_0, aperture, thickness, n_inside, n_outside):
        """
        Initialises LensBase.

        Args:
            z_0 (float): z-coordinate of front of lens.
            aperture (float): Aperture size of the lens.
            thickness(float): Thickness of lens.
            n_inside (float): Refractive  index of lens material.
            n_outside (float): Refractive index of outside medium.
        """
        self.__z_0 = z_0
        self.__aperture = aperture
        self.__thickness = thickness
        self.__n_inside = n_inside
        self.__n_outside = n_outside

    def z_0(self):
        """
        Returns front position of lens.

        Returns:
            float: z-coordinate front position of lens.

        """
        return self.__z_0

    def aperture(self):
        """
        Returns aperture size.

        Returns:
            float: Aperture value.

        """
        return self.__aperture

    def thickness(self):
        """
        Returns thickness of lens.

        Returns:
            float: Lens thickness.

        """
        return self.__thickness

    def n_inside(self):
        """
        Returns refractive index of lens material.

        Returns:
            float: Lens refractive index.

        """
        return self.__n_inside

    def n_outside(self):
        """
        Returns refractive index of medium outside of lens.

        Returns:
            float: Refractive index of outside medium.

        """
        return self.__n_outside

    def intercept(self, ray):
        """
        Default intercept method (always returns None).

        Subclasses will override if they return an intersection point.

        Args: ray (Ray): Ray whose intersection is to be found.

        Returns:
            None
        """
        return None

    def propagate_ray(self, ray):
        """
        Default propagation method (does nothing).

        Subclasses will override this to propagate a ray.

        Args: ray (Ray): Ray whose intersection is to be found.

        Returns:

        """
        return


class PlanoConvex(LensBase):
    """
    Plano-convex lens model made of a planar surface followed by a spherical surface.

    Inherits from LensBase, propagating rays through the surfaces using SphericalRefraction.

    Attributes:
        curvature (float): Curvature of convex surface
        plane (SphericalRefraction): Planar lens surface.
        convex (SphericalRefraction): Curved lens surface.

    Methods:
        propagate_ray(ray): Propagates ray through lens.
        curvature(): Returns curvature of convex surface.
        __repr__(): Returns human-readable string representation of lens.
        focal_point(): Finds focal point of plano-convex lens.
    """

    def __init__(self, z_0, aperture, thickness, curvature, n_inside, n_outside):
        """
        Initialises plano-convex lens.

        Args:
            z_0 (float): z-coordinate of front of lens.
            aperture (float): Aperture radius.
            thickness (float): Distance between spherical and planar lens surfaces.
            curvature (float): Curvature of convex surface.
            n_inside (float): Refractive index inside material.
            n_outside (float): Refractive index outside material.

        Raises:
            ValueError: If curvature is zero, so not plano-convex.
        """


        super().__init__(z_0, aperture, thickness, n_inside, n_outside)

        self.__curvature = curvature

        if curvature == 0.0:
            raise ValueError('Plano-convex lens must have right side with non-zero curvature.')

        self.__plane = SphericalRefraction(self.z_0(), self.aperture(),
                                            0.0, self.n_outside(), self.n_inside())
        self.__convex = SphericalRefraction(self.z_0() + self.thickness(),
                                             self.aperture(), curvature,
                                               self.n_inside(), self.n_outside())

    def propagate_ray(self, ray):
        """
        Propagates ray through lens.

        Args:
            ray (Ray): Ray object that is to be propagated through the lens.

        """
        if self.__plane.intercept(ray) is None:
            return

        self.__plane.propagate_ray(ray)

        if self.__convex.intercept(ray) is None:
            return

        self.__convex.propagate_ray(ray)

    def curvature(self):
        """
        Returns curvature of convex surface.

        Returns:
            float: Curvature value.

        """
        return self.__curvature

    def __repr__(self):
        """
        Returns a human-readable string version of the plano-convex lens.

        Returns:
            str: String including input values for plano-convex lens.

        """
        return(f'PlanoConvex(z_0={self.z_0()}, aperture={self.aperture()},'
               f'thickness={self.thickness()}, curvature1={self.__curvature},'
               f' n_inside={self.n_inside()}, n_outside={self.n_outside()})')

    def focal_point(self):
        """
        Returns focal point of plano-convex lens (paraxial approximation).

        Returns:
            float: z-coordinate of focal point.
        """

        n = self.n_inside() / self.n_outside()
        curvature = self.__curvature
        radius = abs(1 / curvature)

        focal = radius / (n - 1)  # thin lens formula

        # thick correction
        return self.z_0() + self.thickness() + focal





class ConvexPlano(LensBase):
    """
    Convex-plano lens model made of a spherical surface followed by a planar surface.

    Inherits from LensBase, propagating rays through the surfaces using SphericalRefraction.

    Attributes:
        curvature (float): Curvature of convex surface
        plane (SphericalRefraction): Planar lens surface.
        convex (SphericalRefraction): Curved lens surface.

    Methods:
        propagate_ray(ray): Propagates ray through lens.
        curvature(): Returns curvature of convex surface.
        __repr__(): Returns human-readable string representation of lens.
        focal_point(): Finds focal point of convex-plano lens.
    """

    def __init__(self, z_0, aperture, thickness, curvature, n_inside, n_outside):
        """
        Initialises plano-convex lens.

        Args:
            z_0 (float): z-coordinate of front of lens.
            aperture (float): Aperture radius.
            thickness (float): Distance between spherical and planar lens surfaces.
            curvature (float): Curvature of convex surface.
            n_inside (float): Refractive index inside material.
            n_outside (float): Refractive index outside material.

        Raises:
            ValueError: If curvature is zero, so not convex-plano.
        """

        super().__init__(z_0, aperture, thickness, n_inside, n_outside)

        self.__curvature = curvature

        if curvature == 0.0:
            raise ValueError('Plano-convex lens must have right side with non-zero curvature.')

        self.__convex = SphericalRefraction(self.z_0(), self.aperture(),
                                             curvature, n_1=self.n_outside(),
                                               n_2=self.n_inside())
        self.__plane = SphericalRefraction(self.z_0() + self.thickness(),
                                            self.aperture(), 0.0, self.n_inside(),
                                              self.n_outside())



    def propagate_ray(self, ray):
        """
        Propagates ray through lens.

        Args:
            ray (Ray): Ray object that is to be propagated through the lens.

        """
        if self.__convex.intercept(ray) is None:
            return

        self.__convex.propagate_ray(ray)

        if self.__plane.intercept(ray) is None:
            return

        self.__plane.propagate_ray(ray)


    def curvature(self):
        """
        Returns curvature of convex lens.

        Returns:
            float: Curvature value.

        """
        return self.__curvature


    def __repr__(self):
        """
        Returns a human-readable string version of the convex-plano lens.

        Returns:
            str: String including input values for convex-plano lens.

        """
        return(f'ConvexPlano(z_0={self.z_0()}, aperture={self.aperture()},'
               f'thickness={self.thickness()}, curvature1={self.__curvature},'
               f' n_inside={self.n_inside()}, n_outside={self.n_outside()})')

    def focal_point(self):
        """
        Returns focal point of convex-plano lens (paraxial approximation).

        Returns:
            float: z-coordinate of focal point.

        """
        curvature = self.__curvature
        n = self.n_inside() / self.n_outside()
        radius = abs((1 / curvature))

        focal = radius / (n - 1)  # thin lens formula

        displacement = (n - 1) * self.thickness() / n  # thick correction
        return self.z_0() + focal + displacement



class BiConvex(LensBase):
    """
    Biconvex model with two spherical convex surfaces.

    Inherits from LensBase, propagating rays through the surfaces using SphericalRefraction.

    Attributes:
        curvature1 (float): Curvature of first surface.
        curvature2 (float): Curvature of second surface.
        convex1 (SphericalRefraction): First convex surface.
        convex2 (Spherical Refraction): Second convex surface.

    Methods:
        propagate_ray(ray): Propagates ray through lens.
        curvature1(): Returns curvature of first convex surface.
        curvature2(): Returns curvature of second convex surface.
        __repr__(): Returns human-readable string representation of lens.
        focal_point(): Finds focal point of biconvex lens.
    """

    def __init__(self, z_0, aperture, thickness, curvature1, curvature2, n_inside, n_outside):
        """
        Initialises biconvex lens.

        Args:
            z_0 (float): z-coordinate of front of lens.
            aperture (float): Aperture radius.
            thickness (float): Distance between spherical surfaces.
            curvature1 (float): Curvature of first surface
            curvature2 (float): Curvature of second surface.
            n_inside (float): Refractive index inside material.
            n_outside (float): Refractive index outside material.

        """

        super().__init__(z_0, aperture, thickness, n_inside, n_outside)


        self.__curvature1 = curvature1
        self.__curvature2 = curvature2

        self.__convex1 = SphericalRefraction(self.z_0(), self.aperture(),
                                             self.__curvature1, self.n_outside(),
                                               self.n_inside())
        self.__convex2 = SphericalRefraction(self.z_0() + self.thickness(),
                                              self.aperture(), self.__curvature2,
                                                self.n_inside(), self.n_outside())


    def propagate_ray(self, ray):
        """
        Propagates ray through lens.

        Args:
            ray (Ray): Ray object that is to be propagated through the lens.

        """
        self.__convex1.propagate_ray(ray)
        self.__convex2.propagate_ray(ray)


    def curvature1(self):
        """
        Returns curvature of first lens surface.

        Returns:
            float: First curvature value.

        """
        return self.__curvature1

    def curvature2(self):
        """
        Returns curvature of second lens surface.

        Returns:
            float: Second curvature value.

        """
        return self.__curvature2


    def __repr__(self):
        """
        Returns a human-readable string version of the biconvex lens.

        Returns:
            str: String including input values for biconvex lens.

        """
        return(f'BiConvex(z_0={self.z_0()}, aperture={self.aperture()},'
               f'thickness={self.thickness()}, curvature1={self.__curvature1},'
               f'curvature2={self.__curvature2}, n_inside={self.n_inside()},'
               f'n_outside={self.n_outside()})')


    def focal_point(self):
        """
        Returns focal point of biconvex lens.

        Returns:
            float: z-coordinate of focal point.
        """

        n = self.n_inside() / self.n_outside()
        displacement = ((n - 1) * self.__curvature1 *
                        self.__curvature2 * self.thickness() / n)
        # correction for thick lens

        top = n - 1

        focal = 1 / (top * (displacement + self.__curvature1 - self.__curvature2))

        return self.z_0() + focal
