#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 15:45:02 2026

@author: ttgjp
"""

from aerox import AeroX

# create empty object
tec = AeroX()

# import simple CSV with single header line, 2 input columns and 3 output columns
# and data separated by a single space
tec.import_simpleCSV('tecplot.dat', 2, 3, delimiter_char=' ')

# remove any non valid lines of data
tec.filter_keep(isValid=1)

# the isValid data is now superfluous so remove
tec.delete('isValid')

# the coordinate data is all in mm, manual convert to m
#xm = tec.get('x')/1000.0
#ym = tec.get('y')/1000.0

#tec.replace('x', xm)
#tec.replace('y', ym)

# add long names and units to inputs, original file is in mm
tec.x_longnames = ['x coordinate', 'y coordinate']
tec.x_units = ['mm', 'mm']

# add long names and units to outputs
tec.y_longnames = ['x velocity component', 'y velocity component']
tec.y_units = ['m/s', 'm/s']

# convert x and y to meters
tec.convert_units('x', 'm')
tec.convert_units('y', 'm')

# add a linear interpolator (too many points for RBF)
tec.add_interpolator('linear')

# use this to do a contour plot
tec.plot_2d('x', 'y', 'Vx', interpolate=True)

# use this to plot a line
tec.plot('x', 'Vx', interpolate=True, y=-0.1)

# add some comments
tec.add_comment('created from tecplot.dat file and invalid data removed')
tec.add_comment('invalid data removed and coordinates converted to metres')

# finally write out in AeroX standard
tec.write('out_tecplot.csv')

print('test_simpleCSV success')




