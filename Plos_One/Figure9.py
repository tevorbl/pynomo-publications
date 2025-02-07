#!/usr/bin/env python3

# Boltzmann_Nomogen.py
# nomogen example program

#######  bug: printing scales => math domain error ########


import sys
#import numpy as np

sys.path.insert(0, "../nomogen")
sys.path.insert(0, "..")

import math

from nomogen import Nomogen
from pynomo.nomographer import Nomographer


########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand scales
########################################

#####################################################
# Boltzmann equation:
# return Delta
# T = temperature
# P = probability
def Delta(P, T):
    #return -(T*np.log10(P))/0.43
    return -T*math.log(P)

    #return -(T*np.log10(P))/0.43
    return -T*math.log(P)

def Temp(Delta, P):
    return - Delta / math.log(P)

# Pis the middle scale,
# Delta and T are respectively the left and right axes
def P(delta,T):
#    print( 'delta is ', delta, ', T is ', T, ', delta/T is', delta/T )
    return math.exp(-delta/T)

Deltamin = 1 #0.1
Deltamax = 100

Tmin = 1 #0.1
Tmax = 1000 #1000

#Pmin = P(Deltamin, Tmin)
#Pmax = P(Deltamax, Tmax)

Pmin = 0.1
Pmax = 0.99


###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 19

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': Deltamin,
    'u_max': Deltamax,
    'title': r'$\delta$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_scale = {
    'u_min': Tmin,
    'u_max': Tmax,
    'title': r'$T$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_scale = {
    'u_min': Pmin,
    'u_max': Pmax,
    'title': r'$P$',
    'scale_type': 'linear smart',
    'tick_levels': 4,
    'tick_text_levels': 2,
    'tick_side': 'left',
}


block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[40, 'x', 200]],
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 6.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'title_str': r'$Boltzmann \thinspace Equation$',
    'extra_texts': [
        {'x': 4,
         'y': 3,
         'text': r'$P=e^{-{{\delta}\over{T}}}$',
         'width': 5,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],

    # nomogen can attempt a shape that minimises parallax errors
    # instead of forcing the ends of the axes to the corners of the unit square
    # uncomment the following line to attempt this
    #'muShape': 3,
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(P, main_params)  # generate nomogram for function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
