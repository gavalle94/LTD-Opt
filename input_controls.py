from networkx import DiGraph


def check_integer(value, name, minValue = None, maxValue = None):
	'''
	This function verify if the variable "value" is an integer number, in the specified interval
	'''
	# Verify that the variable and the extreme values for the range (if declared) are integer numbers
	if not isinstance(value, (int, long)):
		raise TypeError('the parameter "%s" is invalid: it must be an integer' % (name))
	if minValue is not None and not isinstance(minValue, (int, long)):
		raise TypeError('the parameter "minValue" is invalid: it must be an integer')
	if maxValue is not None and not isinstance(maxValue, (int, long)):
		raise TypeError('the parameter "maxValue" is invalid: it must be an integer')
	# Verify in-range condition
	if minValue is not None and value < minValue:
		raise ValueError('the parameter "%s" must be an integer greater than or equal to %d' % (name, minValue))
	if maxValue is not None and value > maxValue:
		raise ValueError('the parameter "%s" must be an integer lower than or equal to %d' % (name, maxValue))

def check_number(value, name, minValue = None, maxValue = None):
	'''
	This function verify if the variable "value" is an real number, in the specified interval
	'''
	# Verify that the variable and the extreme values for the range (if declared) are float numbers
	if not isinstance(value, (int, long, float)):
		raise TypeError('the parameter "%s" is invalid: it must be a number' % (name))
	if minValue is not None and not isinstance(minValue, (int, long, float)):
		raise TypeError('the parameter "minValue" is invalid: it must be a number')
	if maxValue is not None and not isinstance(maxValue, (int, long, float)):
		raise TypeError('the parameter "maxValue" is invalid: it must be a number')
	# Verify in-range condition
	if minValue is not None and value < minValue:
		raise ValueError('the parameter "%s" must be a number greater than or equal to %d' % (name, minValue))
	if maxValue is not None and value > maxValue:
		raise ValueError('the parameter "%s" must be a number lower than or equal to %d' % (name, maxValue))

def check_DiGraph(value, name):
	'''
	This function verify if the variable "value" is an oriented graph
	'''
	if not isinstance(value, DiGraph):
		raise TypeError('the parameter "%s" is invalid: it must be an oriented graph' % (name))

def check_node_exists(node, G):
	'''
	This function verify if the graph "G" contains the node "node"
	'''
	if node not in G.nodes():
		raise ValueError('the specified node (%s) does not exist' % (node))

def check_array(value, name, dimensions = 1, of = None):
	'''
	This function verify if the variable "value" is an multidimensional array.
	I can also verify the data type of the array'cells (using the parameter "of")
	'''
	# INPUT CONTROL
	check_integer(dimensions, 'dimensions', minValue = 1)
	
	def recursive_check(value, actual_dimension, of):
		'''
		Recursive function, used to check the validity of the array
		'''
		# End condition
		if actual_dimension == 1:
			# If needed, I check the data type
			typeok = True
			if of is not None:
				try:
					for x in value:
						if not isinstance(x, of):
							typeok = False
							break
				except TypeError:
					typeok = False
			# Result
			return (typeok and isinstance(value, (list, tuple, set)))

		# Recursion
		for x in value:
			if not recursive_check(x, actual_dimension-1, of):
				return False
		return True

	# Check the variable
	if not recursive_check(value, dimensions, of):
		raise TypeError('the parameter "%s" is invalid: it must be a %d-dimensional array' % (name, dimensions))

def input_int(msg, minValue = None, maxValue = None):
	'''
	This function allow the user to retrieve an integer number as input from the keyboard.
	If specified, I can decide a range of valid values
	'''
	# INPUT CONTROL
	# minValue
	if minValue is not None:
		check_integer(minValue, 'minValue')
	# maxValue
	if maxValue is not None:
		check_integer(maxValue, 'maxValue', minValue = minValue)

	# ALGORITHM
	while True:
		try:
			# User input: if it is not an integer number, int() raise an exception
			n = int(input(msg + ': '))
			# Using assert, I can verify the in-range condition (if necessary)
			if minValue is not None:
				assert n >= minValue
			if maxValue is not None:
				assert n <= maxValue
			# If I arrive here, the input is valid: I exit the while loop
			break
		except:
			# The input is not an integer number: create an error message
			msg_err = '\nPlease, insert an integer'
			if minValue != None and maxValue != None:
				msg_err += ' between %d and %d' % (minValue, maxValue)
			elif minValue != None:
				msg_err += ' greater than or equal to %d' % (minValue)
			elif maxValue != None:
				msg_err += ' lower than or equal to %d' % (maxValue)
			# Print on the screen the error message
			print(msg_err)
	# Result
	return n

def input_float(msg, minValue = None, maxValue = None):
	'''
	This function allow the user to retrieve a real number as input from the keyboard.
	If specified, I can decide a range of valid values
	'''
	# INPUT CONTROL
	# minValue
	if minValue is not None:
		check_integer(minValue, 'minValue')
	# maxValue
	if maxValue is not None:
		check_integer(maxValue, 'maxValue', minValue = minValue)

	# ALGORITHM
	while True:
		try:
			# User input: if it is not a real number, float() raise an exception
			n = float(input(msg + ': '))
			# Using assert, I can verify the in-range condition (if necessary)
			if minValue is not None:
				assert n >= minValue
			if maxValue is not None:
				assert n <= maxValue
			# If I arrive here, the input is valid: I exit the while loop
			break
		except:
			# The input is not a real number: create an error message
			msg_err = '\nPlease, insert a number'
			if minValue != None and maxValue != None:
				msg_err += ' between %d and %d' % (minValue, maxValue)
			elif minValue != None:
				msg_err += ' greater than or equal to %d' % (minValue)
			elif maxValue != None:
				msg_err += ' lower than or equal to %d' % (maxValue)
			# Print on the screen the error message
			print(msg_err)
	# Result
	return n