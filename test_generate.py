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
motion.write('motion.csv')

print('test_generate success')