import math
import numpy

def my_interpolate(x_list, y_list):

	n = len(x_list)
	
	""" 
	these lists will be such that:
	
	a_list[i] is a_i
	b_list[i] is b_i
	r_list[i] is r_2i
	th_list[i] is theta_2i
	phi_list[i] is phi_2i
	
	if the arc is a line, then r_list[i] will be math.nan,
	a_list[i], b_list[i] will be the coordinates of the start
	th_list[i], phi_list[i] will be the coordinates of the vector
	"""
	
	a_list, b_list, r_list, th_list, phi_list = [], [], [], [], []
	
	for i in range(n)[:-2:2]: 
		# i increments by 2
		mag2_0 = x_list[i]**2 + y_list[i]**2
		mag2_1 = x_list[i+1]**2 + y_list[i+1]**2
		mag2_2 = x_list[i+2]**2 + y_list[i+2]**2
		Dmag2_0 = mag2_1 - mag2_0
		Dmag2_1 = mag2_2 - mag2_1
		
		Dvect = [Dmag2_0, Dmag2_1]
		
		A = [[x_list[i+1] - x_list[i], y_list[i+1] - y_list[i]], 
		[x_list[i+2] - x_list[i+1], y_list[i+2] - y_list[i+1]]]
		
		if numpy.linalg.det(A) == 0:
			r_list.push(math.nan)
			a_list.push(x_list[i])
			b_list.push(y_list[i])
			th_list.push(x_list[i+2] - x_list[i])
			phi_list.push(y_list[i+2] - x_list[i])
			# ignore the rest, go to the next i
			continue
		
		A_inv = numpy.linalg.inv(A)
		
		[a, b] = 1/2 * A_inv @ Dvect
		
		a_list.push(a)
		b_list.push(b)
		
		r = math.sqrt((x_list[i] - a)**2 + (y_list[i] - b)**2)
		r_list.push(r)
		
		# atan2, as described above, is supported natively
		theta = math.atan2(y_list[i] - b, x_list[i] - a)
		th_list.push(theta)
		
		alpha = math.atan2(y_list[i+1] - b, x_list[i+1] - a) - theta
		beta = math.atan2(y_list[i+2] - b, x_list[i+2] - a) - alpha - theta
		
		sign_alpha = 1 if alpha >= 0 else -1 
		if alpha * beta >= 0:
			if alpha + beta > sign_alpha * 2 * math.pi:
				alpha -= 2 * math.pi
				beta -= 2 * math.pi
		else:
			if alpha * sign_alpha > - beta * sign_alpha:
				alpha -= sign_alpha * 2 * math.pi
			else:
				beta += sign_alpha * 2 * math.pi
				
		phi_list.push(alpha + beta)
	
	if n%2 == 0:
		# segment for the leftover point
		r_list.push(math.nan)
		a_list.push(x_list[-2])
		b_list.push(y_list[-2])
		th_list.push(x_list[-1] - x_list[-2])
		phi_list.push(y_list[-1] - y_list[-2])
	
	return a_list, b_list, r_list, th_list, phi_list
	
def my_function(t, a_list, b_list, r_list, th_list, phi_list):
	i = math.floor(t)
	t -= i
	if (r_list[i] == math.nan):
		x = a_list[i] + t * th_list[i]
		y = b_list[i] + t * phi_list[i]
	else:
		x = a_list[i] + r_list[i] * math.cos(th_list[i] + t * phi_list[i])
		y = b_list[i] + r_list[i] * math.sin(th_list[i] + t * phi_list[i])
	return x, y