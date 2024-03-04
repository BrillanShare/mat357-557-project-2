import math
import numpy

def best_fit_sinusoid(x_list, y_list, wl):
    """ 
    Returns the coefficients a_0, a_s, a_c
    for the best-fitting sinsoid 
    y = a_0 + a_s * sin(2*pi*x/wl) + a_c * cos(2*pi*x/wl)
    with wl as the wavelength
    to the given coordinates in x_list and y_list.
    Only works if both lists are the same length.
    """
    
    if (len(x_list) != len(y_list)):
        raise Exception("Coordinate lists have unequal size")
    if (wl == 0):
        raise Exception("Zero wavelength not permitted")
        
    if (len(x_list) == 2):
        # you can fill this in if needed
        raise Exception("Sets of two points not supported")
        
    if (len(x_list) == 1):
        # horizontal line
        return y_list[0], 0, 0
        
    n = len(x_list)
    s_s = sum(math.sin(2*math.pi*x/wl) for x in x_list)
    s_c = sum(math.cos(2*math.pi*x/wl) for x in x_list)
    s_ss = sum(math.sin(2*math.pi*x/wl)**2 for x in x_list)
    s_sc = sum(math.sin(2*math.pi*x/wl)* \
               math.cos(2*math.pi*x/wl) for x in x_list)
    s_cc = sum(math.cos(2*math.pi*x/wl)**2 for x in x_list)
    
    s_y = sum(y_list)
    s_sy = sum(math.sin(2*math.pi*x/wl)*y for x,y in zip(x_list, y_list))
    s_cy = sum(math.cos(2*math.pi*x/wl)*y for x,y in zip(x_list, y_list))
    
    # this uses numpy for matrix inverses and multiplication
    XTX = [
        [n, s_s, s_c], 
        [s_s, s_ss, s_sc], 
        [s_c, s_sc, s_cc]
        ]
    XTy = [s_y, s_sy, s_cy]
    
    if numpy.linalg.det(XTX) == 0:
        raise Exception("Singular matrix error")
    
    XTX_inv = numpy.linalg.inv(XTX)
    [a_0, a_s, a_c] = XTX_inv @ XTy
    
    return a_0, a_s, a_c, wl

def sin_func(a_0, a_s, a_c, wl):
    return lambda x: a_0 + \
        a_s * math.sin(2*math.pi*x/wl) + \
        a_c * math.cos(2*math.pi*x/wl)

"""
To get the line as a function of x, 
use x_list, y_list in this line:

sin_func = para_func(*best_fit_sinusoid(x_list, y_list))

then:

this_func(x)
"""