#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 17:16:51 2025

@author: ttgjp
"""

from aerox import AeroX
import numpy as np

# generate a new AeroX file based on sin(omega*t)

motion = AeroX()

# circular motion
omega = 0.5 # rad/s
radius = 4.0 # m
time = np.arange(0, 50, 0.2)
x = radius*np.cos(omega*time)
y = radius*np.sin(omega*time)

# insert data will automatically increment x_nd and y_nd
motion.insert_x('time', 'time', 's', time)
motion.insert_y('xpos', 'x position', 'm', x)
motion.insert_y('ypos', 'y position', 'm', y)

# plot to check 
motion.plot('time', 'xpos')

# build up the comments
motion.add_comment('AeroX analytical test file')
motion.add_comment('circular motion as a function of time')

# finally write
motion.write('test_motion.csv')

# test generating an empty data and filling manually
# will be faster than using insert_x and insert_y but only matters for huge arrays
motion2 = AeroX(x_nd=1, y_nd=2, nrows=250)

# manually insert data into x and y
for i in range(250):
    time = 0.2*i
    x = radius*np.cos(omega*time)
    y = radius*np.sin(omega*time)
    motion2.x[i,0] = time
    motion2.y[i,0] = x
    motion2.y[i,1] = y

# to be useful will also need to manually enter names, long names, units
# and set min, max, mean    
motion2.x_names=['time']
motion2.x_longnames=['time']
motion2.x_units=['s']

motion2.y_names=['xpos', 'ypos']
motion2.y_longnames=['x position', 'y position']
motion2.y_units=['m', 'm']

motion2._set_minmaxmean_x()
motion2._set_minmaxmean_y()

# plot to check 
motion2.plot('time', 'xpos')




print('test_generate success')