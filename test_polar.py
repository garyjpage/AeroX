#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 17:22:00 2025

@author: ttgjp
"""

from aerox import AeroX
import numpy as np

# test reading 2x 2y file with synthetic data for aerofoil polar
# test using interpolation
# test line and contour plots

print('reading file..')
polar = AeroX('polar.csv')

print('adding RBF interpolator..')
polar.add_interpolator('RBF')
print('testing interpolation on multiple points..')
x = np.array([[0.0,1E6], [4.0,1E6], [0.0,2E6], [4.0,2E6], [4.5,1E6], [4.0,1.5E6] ])
y = polar.interpolate(x)
print('input x:', x)
print('output y:', y)

CD = polar.interpolate_y('CD', alpha=0.0, Re=1.0E6)
print('interpolate alpha=0.0, Re=1E6, CD=:', CD)
CL = polar.interpolate_y('CL', alpha=0.0, Re=1.0E6)
print('test interpolate alpha=0.0, Re=1E6, CL=:', CL)

CD = polar.interpolate_y('CD', alpha=4.0, Re=1.0E6)
print('interpolate alpha=4.0, Re=1E6, CD=:', CD)
CL = polar.interpolate_y('CL', alpha=4.0, Re=1.0E6)
print('interpolate alpha=4.0, Re=1E6, CL=:', CL)

CD = polar.interpolate_y('CD', alpha=4.5, Re=1.0E6)
print('interpolate alpha=4.5, Re=1E6, CD=:', CD)
CL = polar.interpolate_y('CL', alpha=4.5, Re=1.0E6)
print('interpolate alpha=4.5, Re=1E6, CL=:', CL)

CD = polar.interpolate_y('CD', alpha=4.0, Re=1.5E6)
print('interpolate alpha=4.0, Re=1.5E6, CD=:', CD)
CL = polar.interpolate_y('CL', alpha=4.0, Re=1.5E6)
print('interpolate alpha=4.0, Re=1.5E6, CL=:', CL)

CD = polar.interpolate_y('CD')
print('interpolate mean defaults, CD=:', CD)
CL = polar.interpolate_y('CL')
print('interpolate mean defaults, CL=:', CL)

print('testing line plots..')
polar.plot('alpha','CD', Re=1.0E6, interpolate=True )

print('testing contour plots..')
polar.plot_2d('alpha', 'Re', 'CD', interpolate=True)
polar.plot_2d('alpha', 'Re', 'CD')

# check writing
polar.write('test_polar.csv')

print('test_polar success')
