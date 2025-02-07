#!/usr/bin/env python3

# nomogen example program

import sys

sys.path.insert(0, "..")

from math import *

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

###################
# compound interest, epidemics, etc
def compound(r, N):
    # r = % rate pa, y = nr years
    r = r/100
    rm = r/(1-(1+r)**-N) - 1/N
    return rm*100


rmin = 1.0
rmax = 10
Nmin = 1
Nmax = 20
wmin = compound(rmin, Nmin) #*0.9
wmax = compound(rmax, Nmax) #*1.1
#wmin = 0.7
#wmax = 6.5

print( 'wmin is ', wmin, 'wmax is ', wmax )
###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors

NN = 6

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

# the u scale
# dictionary with key:value pairs
left_scale = {
    'u_min': rmin,
    'u_max': rmax,
    'title': r'$bank\thinspace interest \thinspace (\%)$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_scale = {
    'u_min': Nmin,
    'u_max': Nmax,
    'title': r'$N \thinspace Amortizacion (yrs)$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 4,
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$r_m \thinspace average \thinspace interest \thinspace (\%)$',
    'title_x_shift': 1.5,
    'title_y_shift': 0.2,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[5.5, 'x', 12]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 5.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str': r'$r_m = {r \over {1 - (1+r)^{-N}}} - {1 \over N}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(compound, main_params)  # generate nomogram for yrs function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
