# this code uses the given best_fit_line function

def my_interpolate(x_list, y_list):
	# assume that x_list is sorted from lowest to highest
	
	min_x, max_x = x_list[0], x_list[-1]
	u = (min_x + max_x)/2
	
	# left_size determines the number of points 
	# on the left of the corner by checking
	# if each is less than u
	
	left_size = sum(x < u for x in x_list)
	
	max_iter = 3
	for i in range(max_iter):
	
		# left best-fit line
		a_0, a_1 = best_fit_line(x_list[:left_size], y_list[:left_size])
		# right best-fit line
		b_0, b_1 = best_fit_line(x_list[left_size:], y_list[left_size:])
		
		if left_size < 2:
			# too far left, make a corner at x = u
			u = x_list[1]
			v = b_0 + b_1 * u
			a_1 = (y_list[0] - v)/(x_list[0] - u)
			break
		if len(x_list) - left_size < 2:
			# too far right
			u = x_list[-2]
			v = a_0 + a_1 * u
			b_1 = (y_list[-1] - v)/(x_list[-1] - u)
			break
		
		# (this should almost never happen)
		if (a_1 == b_1): raise Exception("Parallel line error")
		
		u = (a_0 - b_0)/(b_1 - a_1)
		v = a_0 + a_1 * u
		
		last_left_size = left_size
		left_size = sum(x < u for x in x_list)
		
		# check if we need to move
		if (last_left_size == left_size): break
	
	return u, v, a_1, b_1
	
def my_function(x, u, v, a, b):
	
	if x < u: return (x - u)*a + v
	else: return (x - u)*b + v