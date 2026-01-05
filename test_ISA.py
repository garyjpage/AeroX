#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 17:22:00 2025

@author: ttgjp
"""

from aerox import AeroX

# test reading constants with x_nd = 0
# AeroX has some edge cases 


ISA = AeroX('isa.csv')
print('print testing get constant on ISA SL conditions..') 
rho0 = ISA.get_constant('rho0')
P0 = ISA.get_constant('P0')
T0 = ISA.get_constant('T0')
print(rho0, ISA.y_units[0] )
print(P0,   ISA.y_units[1] )
print(T0,   ISA.y_units[2] )

