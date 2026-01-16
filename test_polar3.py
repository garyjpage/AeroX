#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 16:24:31 2025

@author: ttgjp
"""

from aerox import AeroX
import numpy as np

# test reading 3x 3y file with synthetic data for aerofoil polar
# test edge cases with spaces and quotes
# test filter remove including not a number

print('reading polar3 file..')
polar3 = AeroX('polar3.csv')

print('x longnames:', polar3.x_longnames)
print('y longnames:', polar3.y_longnames)
print('identifiers:', polar3.id[0:4]) # contains some identifier information

# test removing some rows
print('min max x:', polar3.x_min, polar3.x_max)
print('min max y:', polar3.y_min, polar3.y_max)

print('removing alpha = 10 data')
polar3.filter_remove(alpha=10.0)

print('removing CM is NaN data')
polar3.filter_remove(CM=np.nan)

print('removing alpha is NaN data')
polar3.filter_remove(alpha=np.nan)

print('min max x:', polar3.x_min, polar3.x_max)
print('min max y:', polar3.y_min, polar3.y_max)


# test reading a single row
print('reading single row file..')
row = AeroX('singlerow.csv')
print('x:', row.x, 'y:',row.y)

print('test_polar3 success')
