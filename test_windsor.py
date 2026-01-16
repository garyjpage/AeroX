#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 16:08:57 2025

@author: ttgjp
"""

from aerox import AeroX

base = AeroX('windsor_surfacepressure_group4.csv')

# use standard 2d plotting with internal triangulation
base.plot_2d('y', 'z', 'MeanCp') 

# since x is constant it can cause problems with interpolation so remove
base.delete_x('x')

# add Radial Basis Function interpolation
base.add_interpolator('RBF')

# 2d plotting using interpolator
base.plot_2d('y', 'z', 'MeanCp', interpolate=True) 

# plot vertical line along symmetry y=0
base.plot('z','MeanCp', y=0.0, interpolate=True)

# plot horizontal line along z=0.15 m
base.plot('y','MeanCp', z=0.15, interpolate=True)

# add a comment to document the change
base.add_comment('x column removed as constant value')

# test writing out file with x removed in standard CSV format
base.write('test_windsor.csv', simple_CSV=True)

# test reading back in standard CSV
# need to define the input and output columns when reading
base = AeroX('test_windsor.csv', simple_CSV=True, x_nd=2, y_nd=2)

# manually add units
base.x_units = ['m', 'm']
base.y_units = ['-', '-']


# use standard 2d plotting with internal triangulation
base.plot_2d('y', 'z', 'MeanCp') 

print('test_windsor success')




