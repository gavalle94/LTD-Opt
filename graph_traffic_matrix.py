import random
import input_controls as inc


def random_TM(n, valueMin, valueMax):
	'''
	This function creates and returns a traffic matrix nxn, whose diagonal is zero (no self-loops).
	Traffic values are computed as instance of random variables, whose pdf is uniform between values
	"valueMin" and "valueMax" (both included)
	'''
	# INPUT CONTROL
	# valueMin
	inc.check_number(valueMin, 'valueMin', minValue = 0)
	# valueMax
	inc.check_number(valueMax, 'valueMax', minValue = valueMin)
	# N
	inc.check_integer(n, 'n', minValue = 2)

	# Creating the matrix
	tmp = range(n)
	res = []
	for i in tmp:
		# i-th row of the matrix
		res.append([])
		for j in tmp:
			# j-th cell of the i-th row
			if i == j:
				v = 0.0
			else:
				v = round(random.random()*(valueMax - valueMin) + valueMin, 2)
			res[i].append(v)
	# Result
	return res

def random_TM_2(n, low_min, low_max, high_min, high_max, p):
	'''
	This function creates and returns a traffic matrix nxn, whose diagonal is zero (no self-loops).
	Traffic values are computed as instance of random variables, whose pdf is uniform: its extrame values
	vary according to a boolean value "high_traffic", which is true with associated probability "p".
	Input required parameters are:
	- "n": number of nodes
	- "low_min" and "low_max": pdf extreme values, when "high_traffic" = False
	- "high_min" and "high_max": pdf extreme values, when "high_traffic" = True
	'''
	# INPUT CONTROL
	# low_min
	inc.check_number(low_min, 'low_min', minValue = 0)
	# low_max
	inc.check_number(low_max, 'low_max', minValue = low_min)
	# high_min
	inc.check_number(high_min, 'high_min', minValue = 0)
	# high_max
	inc.check_number(high_max, 'high_max', minValue = high_min)
	# N
	inc.check_integer(n, 'n', minValue = 2)
	# P
	inc.check_number(p, 'p', minValue = 0, maxValue = 1)

	# ALGORITHM
	T = []
	for s in range(n):
		T.append([])
		for d in range(n):
			# The diagonal is 0
			if s == d:
				x = 0.0
			else:
				# Check to be in the "high traffic" condition
				high_traffic = random.random() <= p
				# Compute pdf extreme values "a" and "b"
				if high_traffic:
					a = high_min
					b = high_max
				else:
					a = low_min
					b = low_max
				# Compute the random variable instance  n = U(a, b)
				x = round(random.random() * (b - a) + a, 2)
			# Value for Tsd
			T[s].append(x)
	# Result
	return T

def print_TM(tm):
	'''
	This function pronts on screen the content of the specified traffic matrix
	'''
	print('\nTraffic Matrix:')
	for r in tm:
		s = ''
		for c in r:
			s += '%s\t' % (c)
		print(s)