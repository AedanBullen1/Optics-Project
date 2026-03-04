"""Analysis module."""
import copy
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from raytracer.rays import Ray
from raytracer.elements import SphericalRefraction, OutputPlane, SphericalReflection
from raytracer.rays import RayBundle
from raytracer.lenses import PlanoConvex, ConvexPlano, BiConvex
from raytracer.diffraction_test import diffraction_significance

def task8():
    """
    Task 8.

    In this function you should check your propagate_ray function properly
    finds the correct intercept and correctly refracts a ray. Don't forget
    to check that the correct values are appended to your Ray object.
    """
    surface = SphericalRefraction(z_0=0.0, aperture=1.0, curvature=0.2, n_1=1.0, n_2=1.2)
    for i in np.linspace(0,1,11):  # generate a few
        ray = Ray(pos=[i, 0, -0.8])
        surface.propagate_ray(ray)

        print(f'ray starting at x={i}:')
        for pos in ray.vertices():
            print('initial', pos)
        print(f'emergent direction: {ray.direc()}')
        print( )

 # seems to work fine


def task10():
    """
    Task 10.

    In this function you should create Ray objects with the given initial positions.
    These rays should be propagated through the surface, up to the output plane.
    You should then plot the tracks of these rays.
    This function should return the matplotlib figure of the ray paths.

    Returns:
        Figure: the ray path plot.
    """
    sphere_surface = SphericalRefraction(z_0=100.0, curvature=0.03, aperture=34.0, n_1=1.0, n_2=1.5)
    plane_surface = OutputPlane(z_0=250.0)

    initial_positions = np.array([[0, 4, 0], [0, 1, 0], [0, 0.2, 0],
                                 [0, 0, 0], [0, -.2, 0], [0, -1, 0], [0, -4, 0]], dtype=float)

    rays = [Ray(pos=pos) for pos in initial_positions]

    for ray in rays:
        sphere_surface.propagate_ray(ray)
        plane_surface.propagate_ray(ray)

    figure = plt.figure()
    for ray in rays:
        points = ray.vertices()
        z = [i[2] for i in points]
        y = [i[1] for i in points]
        plt.plot(z, y)

    plt.xlabel('z ($mm$)', fontsize=14)
    plt.ylabel('y ($mm$)', fontsize=14)
    plt.xlim(left=0)
    plt.grid(True)
    plt.show()

    return figure  # figure does show spherical aberration when zoomed in.




def task11():
    """
    Task 11.

    In this function you should propagate the three given paraxial rays through the system
    to the output plane and the tracks of these rays should then be plotted.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for ray paths
    2. the calculated focal point.

    Returns:
        tuple[Figure, float]: the ray path plot and the focal point
    """
    sphere_surface = SphericalRefraction(z_0=100.0, curvature=0.03, aperture=34.0, n_1=1.0, n_2=1.5)
    focal_point = sphere_surface.focal_point()
    plane_surface = OutputPlane(z_0=250.0)
    initial_positions = np.array([[0.1, 0.1, 0.0], [0.0, 0.0, 0.0], [-0.1, -0.1, -0.0]],
                                  dtype=float)

    rays = [Ray(pos=pos) for pos in initial_positions]

    for ray in rays:
        sphere_surface.propagate_ray(ray)
        plane_surface.propagate_ray(ray)

    figure = plt.figure()

    for ray in rays:
        points = ray.vertices()
        z = [i[2] for i in points]
        y = [i[1] for i in points]
        plt.plot(z,y)

    plt.xlabel('z ($mm$)', fontsize=14)
    plt.ylabel('y ($mm$)', fontsize=14)
    plt.xlim(left=0)
    plt.grid(True)
    plt.show()

    return figure, focal_point

 # figure/simulation and calculated value correspond.


def task12():
    """
    Task 12.

    In this function you should create a RayBunble and propagate it to the output plane
    before plotting the tracks of the rays.
    This function should return the matplotlib figure of the track plot.

    Returns:
        Figure: the track plot.
    """
    plane_surface = OutputPlane(z_0=250.0)
    sphere_surface = SphericalRefraction(z_0=100.0, curvature=0.03, aperture=34.0, n_1=1.0, n_2=1.5)
    rb = RayBundle()
    rb.propagate_bundle([sphere_surface, plane_surface])  # anticipates a list
    figure = rb.track_plot()
    return figure

  # looks as expected - collimated bundle side-on.



def task13():
    """
    Task 13.

    In this function you should again create and propagate a RayBundle to the output plane
    before plotting the spot plot.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the spot plot
    2. the simulation RMS

    Returns:
        tuple[Figure, float]: the spot plot and rms
    """

    rb = RayBundle()
    sphere_surface = SphericalRefraction(z_0=100.0, curvature=0.03, aperture=34.0, n_1=1.0, n_2=1.5)
    focal_point = sphere_surface.focal_point()
    plane_surface = OutputPlane(z_0=focal_point)

    rb.propagate_bundle([sphere_surface, plane_surface])
    figure = rb.spot_plot()
    rms = rb.rms()

    return figure, rms




def task14():
    """
    Task 14.

    In this function you will trace a number of RayBundles through the optical system and
    plot the RMS and diffraction scale dependence on input beam radii.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the diffraction scale plot
    2. the simulation RMS for input beam radius 2.5
    3. the diffraction scale for input beam radius 2.5

    Returns:
        tuple[Figure, float, float]: the plot, the simulation RMS value, the diffraction scale.
    """
    wavelength = 588e-6  # in mm
    radii = np.linspace(0.1, 10.0, 80)
    rms_vals, diffraction_scales = [], []

    sphere_surface = SphericalRefraction(z_0=100.0, curvature=0.03, aperture=34.0, n_1=1.0, n_2=1.5)
    focal_point = sphere_surface.focal_point()
    plane_surface = OutputPlane(z_0=focal_point)
    print(focal_point)

    for i in radii:
        rb = RayBundle(rmax=i)
        rb.propagate_bundle([sphere_surface, plane_surface])

        diameter = 2 * i
        diffraction_scale = (wavelength * focal_point) / (2 * diameter)
        rms_vals.append(rb.rms())
        diffraction_scales.append(diffraction_scale)  # for plotting

    figure, ax = plt.subplots()  # have to use subplots for same axis
    ax.plot(radii, rms_vals, label='RMS spot size')
    ax.plot(radii, diffraction_scales, label='Diffraction scale')
    ax.set(xlabel='Beam radius ($mm$)', ylabel='Magnitude at output/focal plane ($mm$)')
    ax.grid(True)
    ax.legend()
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.show()

    rb_specific = RayBundle(rmax=2.5)
    rb_specific.propagate_bundle([sphere_surface, plane_surface])
    diffraction_specific = (wavelength * focal_point) / (4 * 2.5)

    return figure, rb_specific.rms(), diffraction_specific

  # smaller spot size means more diffraction but less RMS spread -- trade off.


def task15():
    """
    Task 15.

    In this function you will create plano-convex lenses in each orientation and
    propagate a RayBundle through each to their respective focal point. You
    should then plot the spot plot for each orientation.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the spot plot for the plano-convex system
    2. the focal point for the plano-convex lens
    3. the matplotlib figure object for the spot plot for the convex-plano system
    4  the focal point for the convex-plano lens


    Returns:
        tuple[Figure, float, Figure, float]: the spot plots and rms for plano-convex
        and convex-plano.
    """

    # plano-convex
    pc = PlanoConvex(z_0=100, aperture=50.,thickness=5.0, curvature=-0.02,
                      n_inside=1.5168, n_outside=1.00)
    focal_point_pc = pc.focal_point()
    rb_pc = RayBundle(rmax=5)
    plane_surface_pc = OutputPlane(z_0=focal_point_pc)
    rb_pc.propagate_bundle([pc, plane_surface_pc])
    figure_pc = rb_pc.spot_plot()

    # convex-plano
    cp = ConvexPlano(z_0=100, aperture=50.,thickness=5.0, curvature=0.02,
                      n_inside=1.5168, n_outside=1)
    focal_point_cp = cp.focal_point()
    rb_cp = RayBundle(rmax=5)
    plane_surface_cp = OutputPlane(z_0=focal_point_cp)
    rb_cp.propagate_bundle([cp, plane_surface_cp])
    figure_cp = rb_cp.spot_plot()

    print(rb_pc.rms(), rb_cp.rms())

    return figure_pc, focal_point_pc, figure_cp, focal_point_cp



def task16():
    """
    Task 16.

    In this function you will be again plotting the radial dependence
    of the RMS and diffraction values
    for each orientation of your lens.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the diffraction scale plot
    2. the RMS for input beam radius 3.5 for the plano-convex system
    3. the RMS for input beam radius 3.5 for the convex-plano system
    4  the diffraction scale for input beam radius 3.5

    Returns:
        tuple[Figure, float, float, float]: the plot, RMS for plano-convex, RMS for
          convex-plano, diffraction scale.
    """
    wavelength = 588e-6  # in mm
    radii = np.linspace(0.1, 10.0, 80)

    pc = PlanoConvex(z_0=100, aperture=50.,thickness=5.0, curvature=-0.02,
                      n_inside=1.5168, n_outside=1.00)
    plane_surface_pc = OutputPlane(pc.focal_point())

    cp = ConvexPlano(z_0=100, aperture=50.,thickness=5.0, curvature=0.02,
                      n_inside=1.5168, n_outside=1.00)
    plane_surface_cp = OutputPlane(cp.focal_point())

    # wants thin lens focal
    focal_thin_pc = (1 / abs(pc.curvature())) / ((pc.n_inside() / pc.n_outside()) - 1)


    rms_pc_vals, rms_cp_vals, diffraction_scales = [], [], []

    for i in radii:
        rb_cp = RayBundle(rmax=i)
        rb_pc = RayBundle(rmax=i)
        rb_cp.propagate_bundle([cp, plane_surface_cp])
        rb_pc.propagate_bundle([pc, plane_surface_pc])
        rms_cp_vals.append(rb_cp.rms())
        rms_pc_vals.append(rb_pc.rms())

        diffraction_scale = (wavelength * focal_thin_pc) / (2 * i)
        diffraction_scales.append(diffraction_scale)

    figure, ax = plt.subplots()
    ax.plot(radii, rms_pc_vals, label='RMS spot size for plano-convex')
    ax.plot(radii, rms_cp_vals, label='RMS spot size for convex-plano')
    ax.plot(radii, diffraction_scales, label='Diffraction scale')
    ax.set(xlabel='Beam radius ($mm$)',
            ylabel='Magnitude at output/focal plane ($mm$)')
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)
    ax.grid(True)
    ax.legend()
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    plt.show()

    # now for specific 3.5 radius

    rb_pc_specific = RayBundle(rmax=3.5)
    rb_cp_specific = RayBundle(rmax=3.5)
    rb_pc_specific.propagate_bundle([pc, plane_surface_pc])
    rb_cp_specific.propagate_bundle([cp, plane_surface_cp])

    # statistical test extension

    p_value_pc, significant_pc = diffraction_significance(rb_pc_specific, wavelength=wavelength,
                                                           focal_length=focal_thin_pc, rmax=3.5)
    print('p-value pc', p_value_pc, 'significant?', significant_pc)

    p_value_cp, significant_cp = diffraction_significance(rb_cp_specific, wavelength=wavelength,
                                                           focal_length=focal_thin_pc, rmax=3.5)
    print('p-value cp', p_value_cp, 'significant?', significant_cp)

    return (figure, rb_pc_specific.rms(), rb_cp_specific.rms(),
            (wavelength * focal_thin_pc) / (2 * 3.5))




def task17():
    """
    Task 17.

    In this function you will be first plotting the spot plot for your
    PlanoConvex lens with the curved side first (at the focal point). You will
    then be optimising the curvatures of a BiConvex lens in order to minimise
    the RMS spot size at the same focal point. This function should return
    the following items as a tuple in the following order:
    1. The comparison spot plot for both PlanoConvex (curved side first) and
      BiConvex lenses at PlanoConvex focal point.
    2. The RMS spot size for the PlanoConvex lens at focal point
    3. the RMS spot size for the BiConvex lens at PlanoConvex focal point

    Returns:
        tuple[Figure, float, float]: The combined spot plot, RMS for the PC lens,
          RMS for the BiConvex lens
    """


    cpl = ConvexPlano(z_0=100., curvature=0.02, n_inside=1.5168,
                       n_outside=1.0, thickness=5., aperture=50.)
    plane_surface_cpl = OutputPlane(cpl.focal_point())

    rb = RayBundle(rmax=5)

    rb_cpl_propagated = copy.deepcopy(rb)  # as in pre-project work

    rb_cpl_propagated.propagate_bundle([cpl, plane_surface_cpl])
    rms_cpl = rb_cpl_propagated.rms()

    def objective_function(curvatures):
        curvature_1, curvature_2 = curvatures


        biconvex = BiConvex(z_0=100.0, curvature1=curvature_1,
                             curvature2=curvature_2, n_inside=1.5168,
                               n_outside=1.0, thickness=5, aperture=50.0)

        rb_being_optimised = copy.deepcopy(rb)

        rb_being_optimised.propagate_bundle([biconvex, plane_surface_cpl])

        return rb_being_optimised.rms()


    optimisation_result = minimize(objective_function, [0.02, -0.02])  # will be between these

    rms_biconvex = optimisation_result.fun
    opt_curvature_1, opt_curvature_2 = optimisation_result.x

    optimal_biconvex = BiConvex(z_0=100., curvature1=opt_curvature_1,
                                 curvature2=opt_curvature_2, n_inside=1.5168,
                                   n_outside=1.0, thickness=5., aperture=50.)
    rb_biconvex = copy.deepcopy(rb)
    rb_biconvex.propagate_bundle([optimal_biconvex, plane_surface_cpl])



    figure, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))
    ax1 = rb_cpl_propagated.spot_plot(ax=ax1)

    ax2 = rb_biconvex.spot_plot(ax=ax2)

    plt.tight_layout()
    plt.show()
    print(rms_cpl, rms_biconvex)

    return figure, rms_cpl, rms_biconvex






def task18():
    """
    Task 18.

    In this function you will be testing your reflection modelling. Create
    a new SphericalReflecting surface and trace a RayBundle through it
    to the OutputPlane.This function should return the following items as a
      tuple in the following order:
    1. The track plot showing reflecting ray bundle off SphericalReflection surface.
    2. The focal point of the SphericalReflection surface.

    Returns:
        tuple[Figure, float]: The track plot and the focal point.

    """

    reflect_surface = SphericalReflection(z_0=100., aperture=6., curvature=-0.02)
    plane_surface = OutputPlane(z_0=50)

    rb = RayBundle(rmax=5)
    rb.propagate_bundle([reflect_surface, plane_surface])

    figure = rb.track_plot()

    focal_point = reflect_surface.focal_point()
    print(focal_point)

    return figure, focal_point



if __name__ == "__main__":

    # Run task 8 function
    task8()

    # Run task 10 function
    FIG10 = task10()

    # Run task 11 function
    FIG11, FOCAL_POINT = task11()

    # Run task 12 function
    FIG12 = task12()

    # Run task 13 function
    FIG13, TASK13_RMS = task13()

    # Run task 14 function
    FIG14, TASK14_RMS, TASK14_DIFF_SCALE = task14()

    # Run task 15 function
    FIG15_PC, FOCAL_POINT_PC, FIG15_CP, FOCAL_POINT_CP = task15()

    # Run task 16 function
    FIG16, PC_RMS, CP_RMS, TASK16_DIFF_SCALE = task16()

    # Run task 17 function
    FIG17, CP_RMS, BICONVEX_RMS = task17()


    # Run task 18 function
    FIG18, FOCAL_POINT = task18()

    plt.show()
