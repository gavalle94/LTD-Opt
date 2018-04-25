# System libraries
import time
# Third party libraries
import networkx as nx
# Our libraries
import input_controls as inc
import graph_topologies as gt
import graph_traffic_matrix as tm
import ltd_utilities as ltd


def LTD_random(n, n_edges, delta_in, delta_out, traffic_matrix, title = 'Random LTD - Comparisons', userView = True, withLabels = True):
	'''
	This function solves the LTD problem generating a random topology, according to the input specified criteria:
	- "n" is the number of nodes
	- "n_edges" is the number of edges
	- "delta_in" is the maximum number of receivers per node
	- "delta_out" is the maximum number of transmitters per node
	- "traffic_matrix" is the traffic matrix, used to decide edges' flow values
	- title: graph's title and output files names (.txt e .png)
	- userView: boolean, used to require the visualization of the topology and the log of the results on screen
	- withLabels: boolean, used to require the visualization of the flow labels in the obtained topology photo
	'''
	# INPUT CONTROL
	# n, delta_in, delta_out and traffic_matrix
	ltd.input_control(n, traffic_matrix, delta_in, delta_out)
	# n_edges: extreme case are the ring or the full mesh topologies
	inc.check_integer(n_edges, 'n_edges', minValue = n, maxValue = n * (n - 1))

	# ALGORITHM
	# Computation starting time
	initial_time = time.time()
	# Create the topology (oriented random graph)
	T = gt.random_topology(n, n_edges, delta_in, delta_out)
	# Result
	return ltd.result(T, traffic_matrix, delta_in, delta_out, initial_time, title, userView, withLabels, 'Random')


def greedy_LTD_mesh(n, traffic_matrix, delta_in, delta_out, title = 'Sol. 1 - Mesh LTD', userView = True, withLabels = True):
	'''
	This function generates a network topolgy in order to solve, using a greedy approach, an LTD problem.
	Input parameters are:
	- n: number of nodes
	- traffic_matrix: traffic matrix (mean traffic value exchanged by node pairs)
	- delta_in: constraint on the maximum number of receivers per node
	- delta_out: constraint on the maximum number of trnasmitters per node
	- title: graph's title and output files names (.txt e .png)
	- userView: boolean, used to require the visualization of the topology and the log of the results on screen
	- withLabels: boolean, used to require the visualization of the flow labels in the obtained topology photo
	'''
	# INPUT CONTROL
	ltd.input_control(n, traffic_matrix, delta_in, delta_out)

	# UTILITY FUNCTIONS
	def edges_to_check(n, traffic_matrix):
		'''
		Lists the edges of the graph "G", ordered by their flow value (ascending order)
		'''
		G = gt.loaded_mesh_topology(n, traffic_matrix)
		edges_to_check = []
		for e in G.edges():
			# Associate the flow to the edge
			u = e[0]
			v = e[1]
			f = G.edge[u][v]['flow']
			edges_to_check.append({
				'edge': e,
				'flow': f
			})
		edges_to_check.sort(key = lambda x: x['flow'])
		return edges_to_check

	# ALGORITHM
	# Computation starting time
	initial_time = time.time()
	# Print on the screen the traffic matrix content
	tm.print_TM(traffic_matrix)
	# If one of the deltas is equal to 1, I know for sure that the resulting topology has to be a ring
	if delta_in == 1 or delta_out == 1:
		T = gt.ring_topology(n)
	else:
		# Instantiate the initial full mesh topology, from which I'm going to remove edges
		T = gt.mesh_topology(n)
		# This array contains the graph's edges, sorted according their flow (ascending order)
		edges_to_check = edges_to_check(n, traffic_matrix)

		# OPTIMIZE THE TOPOLOGY
		# Noe, I have to remove edges until the delta contraints are satisfied 
		# BUT: I could find edges impossible to remove...
		print('\nPlease wait...')
		while (not ltd.check_global_delta_constraints(T, delta_in, delta_out)) and len(edges_to_check) > 0:
			# The edge I try to remove first is the one with minimum flow value
			edge_to_remove = edges_to_check.pop(0)['edge']
			# Nodes of the selected edge
			u = edge_to_remove[0]
			v = edge_to_remove[1]
			# Analyzing the delta constraint on "u" and "v", I could find that it is not necessary to remove this edge
			u_out_degree = T.out_degree()[u]
			v_in_degree = T.in_degree()[v]
			# Check if I really need to remove the edge
			if u_out_degree > delta_out or v_in_degree > delta_in:
				# Verify that, once the edge is removed, the resulting graph will not be disconnected
				if gt.has_alternative_paths(T, edge_to_remove):
					# I can remove the selected edge
					T.remove_edge(u, v)
	# Result
	return ltd.result(T, traffic_matrix, delta_in, delta_out, initial_time, title, userView, withLabels, 'Mesh')


def greedy_LTD_ring(n, traffic_matrix, delta_in, delta_out, title = 'Sol. 2 - Ring LTD', userView = True, withLabels = True):
	'''
	This function computes a network topology in order to solve, using a greedy approach, an LTD problem.
	With respect to the function "greedy_LTD_mesh", here the starting topology is a ring: the idea is to add edges
	to it until the delta constraints are satisfied.

	Input parameters are:
	- n: number of nodes
	- traffic_matrix: traffic matrix (mean traffic value exchanged by node pairs)
	- delta_in: constraint on the maximum number of receivers per node
	- delta_out: constraint on the maximum number of trnasmitters per node
	- title: graph's title and output files names (.txt e .png)
	- userView: boolean, used to require the visualization of the topology and the log of the results on screen
	- withLabels: boolean, used to require the visualization of the flow labels in the obtained topology photo
	'''
	# INPUT CONTROL
	ltd.input_control(n, traffic_matrix, delta_in, delta_out)

	# UTILITY FUNCTIONS
	def edges_to_check(G, traffic_matrix):
		'''
		This function lists the possible edges I can add to the topology, sorted by decreasing flow value
		'''
		res = []
		nodes = G.nodes()
		edges = G.edges()
		# Loop on the traffic matrix values
		for u in nodes:
			for v in nodes:
				# No zero-flow edges (self-loops included)
				f = traffic_matrix[u][v]
				if f > 0:
					# The edge must not already exist i the topology
					e = (u, v)
					if e not in edges:
						# I've foun a candidate edge
						res.append({
							'edge': e,
							'flow': f
						})
		# Sort by decreasing fow value
		res.sort(key = lambda x: x['flow'], reverse = True)
		# Result
		return res

	def check_can_add_edges(G, delta_in, delta_out):
		'''
		This function verify that exist at least 2 nodes, different each other, having at least
		a free receiver and a free transmitter
		'''		
		# Input/output degree of the graph's nodes
		in_deg = G.in_degree()
		out_deg = G.out_degree()
		# Graph's nodes
		nodes = G.nodes()
		# Check the delta_in constraint
		res_ok = False
		for x in nodes:
			if in_deg[x] < delta_in:
				# I've found a node with a free receiver
				# Check now the delta_out constraint
				for y in nodes:
					if y != x and out_deg[y] < delta_out:
						# I've found another node with a free transmitter
						res_ok = True
						break
				if res_ok:
					break
		# Result
		return res_ok

	# ALGORITHM
	# Computation starting time
	initial_time = time.time()
	# Print on screen the content of the traffic matrix
	tm.print_TM(traffic_matrix)
	# The starting topology is a ring
	T = gt.ring_topology(n)
	# If one of the delta constraints is equal to 1, I know for sure that the resulting topology will be the starting one
	if delta_in > 1 and delta_out > 1:
		# Graph's edges, serted by decreasing flow values
		edges_to_check = edges_to_check(T, traffic_matrix)

		# OPTIMIZE THE TOPOLOGY
		# Now, I have to add edges until the delta constraints allow me to do that 
		# BUT: I could find edges impossible to add...
		print('\nPlease wait...')
		while check_can_add_edges(T, delta_in, delta_out) and len(edges_to_check) > 0:
			# The edge I'm going to try to add is the one with the least associated flow value
			edge_to_add = edges_to_check.pop(0)['edge']
			# Nodes of the selected edge
			u = edge_to_add[0]
			v = edge_to_add[1]
			# Check if the selected edge can be added to the topology
			u_out_degree = T.out_degree()[u]
			v_in_degree = T.in_degree()[v]
			if u_out_degree < delta_out and v_in_degree < delta_in:
				# Add the selected edge
				T.add_edge(u, v, flow = 0.0)
	# Result
	return ltd.result(T, traffic_matrix, delta_in, delta_out, initial_time, title, userView, withLabels, 'Ring')


def LTD_manhattan_smart(n, nr, nc, traffic_matrix, title = 'Manhattan LTD', userView = True, withLabels = True):
	'''
	This function creates a Manattan topology and, according to the input traffic matrix, solves an LTD problem.
	
	Input parameters are:
	- n: number of nodes in the topology, placed as a "rectangle"
	- nr: number of nodes per row
	- nc: number of nodes per column
	- traffic_matrix: traffic matrix (mean traffic value exchanged by node pairs)
	- title: graph's title and output files names (.txt e .png)
	- userView: boolean, used to require the visualization of the topology and the log of the results on screen
	- withLabels: boolean, used to require the visualization of the flow labels in the obtained topology photo
	'''
	# UTILITY FUNCTIONS
	def max_pair(T):
		'''
		Retrieve indexes of the highest traffic value into the traffic matrix
		'''
		# Init variables
		maxV = -1
		s_res = None
		d_res = None
		# T is a matrix n x n
		n = len(T)
		# loop over the matrix, to find the maximum value
		for s in range(n):
			for d in range(n):
				if T[s][d] > maxV:
					# Update max values
					maxV = T[s][d]
					s_res = s
					d_res = d
		# Result
		return (s_res, d_res)

	def copy_TM(T):
		'''
		Retrieve a copy for the given traffic matrix (avoid pointer references)
		'''
		res = []
		for row in T:
			res.append([])
			for c in row:
				res[-1].append(c)
		return res

	def empty_place(G, n):
		'''
		Verify that the position "n" of the "G" is empty
		'''
		return G.node[n]['name'] == None

	def place_node(G, pos, name):
		'''
		Place the node "name" into the position "pos" of the topology "G"
		'''
		G.node[pos]['name'] = name

	def node_position(G, n):
		'''
		Retrieve the position in the topology "G" of a node whose name is "n", already positioned
		'''
		res = None
		# Loop over positions
		for p in G.nodes():
			if G.node[p]['name'] == n:
				# I've found the position for the node named "n"
				res = p
				break
		# Result
		return res

	def place_2_nodes(G, s, d):
		'''
		Try to place in "G" nodes "s" and "d": there must be two adjacent places
		'''
		# Loop over positions
		for u in G.nodes():
			# If not positioned, control adjacent nodes
			if empty_place(G, u):
				if place_1_node(G, u, d):
					# I've found a free position and I've placed the second node
					place_node(G, pos = u, name = s)
					return True	
		# No adjacent places for "s" and "d"
		return False

	def place_1_node(G, p, x):
		'''
		Try to place in "G" node "x" near to "p"
		'''
		# Loop over "p" adjacent places
		for v in G.edge[p].keys():
			if empty_place(G, v):
				# I've found two free adjacent places
				place_node(G, pos = v, name = x)
				return True
		# I haven't found an available place for "x"
		return False

	# Start computation time, in seconds
	initial_time = time.time()
	# Print the content of the traffic matrix
	tm.print_TM(traffic_matrix)
	# Create a copy of the traffic matrix (to avoid reference pointers)
	tm_temp = copy_TM(traffic_matrix)
	# First of all, retrieve the starting topology
	T_temp = gt.manhattan_topology(nr, nc)
	# Then, name nodes using an "empty" name
	nodes = T_temp.nodes()
	for n in nodes:
		T_temp.node[n]['name'] = None

	# STEP 0
	# End of computation flag
	end = False
	# Placed nodes
	S = set()
	# Not placed yet nodes
	L = set(nodes)
	while not end:
		# STEP 1
		# Retrieve the pair of nodes who exchange most traffic 
		s, d = max_pair(tm_temp)
		tm_temp[s][d] = -1
		# STEP 2
		s_placed = s in S
		d_placed = d in S
		# Both nodes of the pair are not placed
		if not s_placed and not d_placed:
			# STEP 3
			# Try to place these nodes
			if place_2_nodes(T_temp, s, d):
				# Mark as placed
				S.add(s)
				S.add(d)
				L.remove(s)
				L.remove(d)
		# Only one of the nodes is placed
		elif (s_placed and not d_placed) or (not s_placed and d_placed): 
			# STEP 4
			# Let us call "p" the placed node, "x" the other one
			if s_placed:
				p = s
				x = d
			else:
				p = d
				x = s
			# Try to place node "x"
			if place_1_node(T_temp, node_position(T_temp, p), x):
				# Mark as placed
				S.add(x)
				L.remove(x)
		# STEP 5
		# Both nodes were already placed, or their placement attempt failed
		# Control if I have other nodes to place
		end = len(L) == 0
	# Now, create a second Manhattan topology in which nodes are swapped
	T = gt.manhattan_topology(nr, nc, derived = T_temp)
	# Decide how deep is the existing path research between a pair of nodes
	depth = nr-1 if nr == nc else nr/2 + nc/2
	# Route traffic according to the "water filling" principle
	return ltd.result(T, traffic_matrix, 4, 4, initial_time, title, userView, withLabels, 'Manhattan', depth)


def LTD_manhattan(n, nr, nc, traffic_matrix, title = 'Manhattan LTD', userView = True, withLabels = True):
	'''
	This function creates a Manattan topology and, according to the input traffic matrix, solves an LTD problem.
	
	Input parameters are:
	- n: number of nodes in the topology, placed as a "rectangle"
	- nr: number of nodes per row
	- nc: number of nodes per column
	- traffic_matrix: traffic matrix (mean traffic value exchanged by node pairs)
	- title: graph's title and output files names (.txt e .png)
	- userView: boolean, used to require the visualization of the topology and the log of the results on screen
	- withLabels: boolean, used to require the visualization of the flow labels in the obtained topology photo
	'''
	# Computation starting time, in seconds
	initial_time = time.time()
	# Print on screen the content of the traffic matrix
	tm.print_TM(traffic_matrix)
	# First of all, compute the topology
	T = gt.manhattan_topology(nr, nc)
	# Evaluate the maximum search depth for the paths between pairs of nodes
	depth = nr-1 if nr == nc else nr/2 + nc/2
	# Now, route the traffic according to the "water filling" principle
	return ltd.result(T, traffic_matrix, 4, 4, initial_time, title, userView, withLabels, 'Manhattan', depth)


def greedy_LTD_start():
	'''
	Shortcut: called by the user, in order to retrieve several solutions and compare them each other
	Parameters used to create the graphs are take as input from the user
	'''
	# Number of nodes
	n = inc.input_int('Number of nodes', minValue = 1)
	# Extreme values for the traffic matrix
	TM_min = inc.input_int('Traffic matrix lower bound', minValue = 1)
	TM_max = inc.input_int('Traffic matrix upper bound', minValue = TM_min)
	# Delta values
	delta_in = inc.input_int('Delta_in (max #rx per node)', minValue = 1)
	delta_out = inc.input_int('Delta_out (max #tx per node)', minValue = 1)
	# Traffic matrix
	traffic_matrix = tm.random_TM(n, TM_min, TM_max)
	# Results:
	T1 = greedy_LTD_mesh(n, traffic_matrix, delta_in, delta_out)
	T1_bis = LTD_random(n, len(T1.edges()), delta_in, delta_out, traffic_matrix)
	T2 = greedy_LTD_ring(n, traffic_matrix, delta_in, delta_out)
	T2_bis = LTD_random(n, len(T2.edges()), delta_in, delta_out, traffic_matrix)


# Executable code (main)
if __name__ == '__main__':
	T = greedy_LTD_start()
