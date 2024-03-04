import numpy

def best_fit_parabola(x_list, y_list):
    """ 
    Returns the coefficients a_0, a_1, a_2
    for the best-fitting parabola y = a_0 + a_1 x + a_2 x^2
    to the given coordinates in x_list and y_list.
    Only works if both lists are the same length.
    """
    
    if (len(x_list) != len(y_list)):
        raise Exception("Coordinate lists have unequal size")
        
    if (len(x_list) < 3):
        # Returns a best-fit line if two or fewer points
        return (*best_fit_line(x_list, y_list)), 0
        
    n = len(x_list)
    s_x = sum(x_list)
    s_xx = sum(x**2 for x in x_list)
    s_xxx = sum(x**3 for x in x_list)
    s_xxxx = sum(x**4 for x in x_list)
    s_y = sum(y_list)
    s_xy = sum(x*y for x,y in zip(x_list, y_list))
    s_xxy = sum(x*x*y for x,y in zip(x_list, y_list))
    
    # this uses numpy for matrix inverses and multiplication
    XTX = [
        [n, s_x, s_xx], 
        [s_x, s_xx, s_xxx], 
        [s_xx, s_xxx, s_xxxx]
        ]
    XTy = [s_y, s_xy, s_xxy]
    
    XTX_inv = numpy.linalg.inv(XTX)
    [a_0, a_1, a_2] = XTX_inv @ XTy
    
    return a_0, a_1, a_2

def para_func(a_0, a_1, a_2):
    return lambda x: a_0 + a_1*x + a_2*x**2

"""
To get the line as a function of x, 
use x_list, y_list in this line:

this_parabola = para_func(*best_fit_parabola(x_list, y_list))

then:

this_func(x)
"""