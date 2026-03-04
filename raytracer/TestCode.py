"""
Module testcode.py

This module was used to test code early on in the raytracer worksheet.
"""

from raytracer.rays import Ray
import raytracer.elements as ele

#  Task 2
ray1 = Ray()
print('Initial test')
print('Initial', ray1)
print('Position', ray1.pos())
print('Direction', ray1.direc())
print('vertices', ray1.vertices()) #all works well

init_pos = [0, 1, 2]
init_direc = [0, 1, 2]
ray2 = Ray(pos=init_pos, direc=init_direc)
print('Testing pos, direc and vertices')
print('Initial', ray2)
print('Position', ray2.pos())
print('Direction', ray2.direc())
print('vertices', ray2.vertices())

ray2.append([1, 2, 5], [0, 5, 2])
ray2.append([5, 2, 3], [1, 6, 3])
print('Testing append')
print('Position', ray2.pos())
print('Direction', ray2.direc())
print('vertices', ray2.vertices())

print('Testing exceptions')
init_pos1 = [0, 2, 4, 1]
init_direc2 = [0, 1, 1, 1]
ray3 = Ray(pos=init_pos1, direc=init_direc2) #Error message - good

#  Task 4
sr = ele.SphericalRefraction(z_0=10, aperture=5, curvature=0.2, n_1=1., n_2=1.5)
print(sr)
