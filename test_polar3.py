#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 16:24:31 2025

@author: ttgjp
"""

from aerox import AeroX

# test reading 3x 3y file with synthetic data for aerofoil polar
# test edge cases with spaces and quotes
# test line and contour plots

print('reading polar3 file..')
polar3 = AeroX('polar3.csv')

print('x longnames:', polar3.x_longnames)
print('y longnames:', polar3.y_longnames)
print('identifiers:', polar3.id[0:4]) # contains some identifier information

# test reading a single row
print('reading single row file..')
row = AeroX('singlerow.csv')
print('x:', row.x, 'y:',row.y)

print('test_polar3 success')
