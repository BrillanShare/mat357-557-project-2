import numpy

def best_fit_line(x_list, y_list):
    """ 
    Returns the coefficients a_0, a_1
    for the best-fitting line y = a_0 + a_1 x
    to the given coordinates in x_list and y_list.
    Only works if both lists are the same length.
	"""
	
    if (len(x_list) != len(y_list)):
        raise Exception("Coordinate lists have unequal size")
        
    if (len(x_list) < 2):
        # Returns a horizontal line if given one point
        return x_list[0], 0
        
    n = len(x_list)
    s_x = sum(x_list)
    s_xx = sum(x**2 for x in x_list)
    s_y = sum(y_list)
    s_xy = sum(x*y for x,y in zip(x_list, y_list))
    
    # this uses numpy for matrix inverses and multiplication
    XTX = [[n, s_x], [s_x, s_xx]]
    XTy = [s_y, s_xy]
    
    XTX_inv = numpy.linalg.inv(XTX)
    [a_0, a_1] = XTX_inv @ XTy
    
    return a_0, a_1

def line_func(a_0, a_1):
    return lambda x: a_0 + a_1*x

"""
To get the line as a function of x, 
use x_list, y_list in this line:

this_func = line_func(*best_fit_line(x_list, y_list))

then:

this_func(x)
"""