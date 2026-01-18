#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 17:28:50 2026

@author: ttgjp
"""

from aerox import AeroX

data = AeroX('units.csv')

# show units and min, max before
print('before...')
print('x_names:', data.x_names)
print('x_units:', data.x_units)
print('x min:', data.x_min)
print('x max:', data.x_max)
print()
print('y_names:', data.y_names)
print('y_units:', data.y_units)
print('y min:', data.y_min)
print('y max:', data.y_max)

# do some random conversions
data.convert_units('alpha', 'radians')
data.convert_units('t', 'minutes')
data.convert_units('x', 'inches')

data.convert_units('mass', 'lbs')
data.convert_units('p', 'psi')
data.convert_units('rho', 'slug/(ft**3)')
data.convert_units('v', 'fps')

# show units and min, max after
print()
print('...after')
print('x_names:', data.x_names)
print('x_units:', data.x_units)
print('x min:', data.x_min)
print('x max:', data.x_max)
print()
print('y_names:', data.y_names)
print('y_units:', data.y_units)
print('y min:', data.y_min)
print('y max:', data.y_max)

# write out new file
data.write('out_units.csv')