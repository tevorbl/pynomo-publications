#!/usr/bin/python3
"""
nomogen test program
--------------------

generate a nomogram for the equation below

"""

# nomogen example program

import sys
import math

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer


# pylint: disable=invalid-name


########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand scales
########################################

###############################################
#
#
rhos = 2.8
def fTu(du, cw):
    """ equation to find Tu """
#    du = 105.6640 - 417.332/((2.65 - rhos) + 100*rhos/cw) + 27.94*math.log(Tu*1.102293/rhos )

    t1 = du -  105.6640 + 417.332/((2.65 - rhos) + 100*rhos/cw)
    t2 = math.exp(t1 / 27.94)
    Tu = t2 * rhos / 1.102293
    assert( math.isclose(du, 105.6640 - 417.332/((2.65 - rhos) + 100*rhos/cw) + 27.94*math.log(Tu*1.102293/rhos )) )
    return Tu


Tumin = 10 # t/h
Tumax = 1000
cwmin = 30 # %
cwmax = 80
dumin = 10  #  mm
dumax = 220 #

###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 3

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

middle_scale = {
    'u_min': Tumin,
    'u_max': Tumax,
    'title': r'$T_u \thinspace t \slash h$',
    'scale_type': 'log smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': cwmin,
    'u_max': cwmax,
    'title': r'$C_w \thinspace \%$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

left_scale = {
    'u_min': dumin,
    'u_max': dumax,
    'title': r'$d_u \thinspace mm$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max']) / 2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max']) / 2]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 5.5,
    'title_y': 1.0,
    'title_box_width': 10.0,
 #   'title_str': r'$d_u = 105.6640 \thinspace - \thinspace { 417.332 \over {(2.65-\rho_s) + { 100 \rho_s} \over C_w } } \thinspace + \thinspace 27.94 \thinspace ln({ { 1.102293 \thinspace T_u } \over \rho_s } ) $',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(fTu, main_params)  # generate nomogram for pendulum() function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
