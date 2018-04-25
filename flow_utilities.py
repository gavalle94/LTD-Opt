import networkx as nx


def max_flow(G):
	'''
	This function returns the max flow value on the G's edges. It returns also the corresponding edges
	'''
	# Instantiate useful variables
	edges = G.edges()
	f_max = None
	e_max = None
	# Loop on edges
	for e in edges:
		# Nodes of the current edge
		u = e[0]
		v = e[1]
		# Flow of the current edge
		f = G.edge[u][v]['flow']
		# Control max flow
		if f > f_max:
			# Maximum value update
			f_max = f
			e_max = (u, v)
	# Result
	return (f_max, e_max)

def min_flow(G):
	'''
	This function returns the min flow value on the G's edges. It returns also the corresponding edges
	'''
	# Instantiate useful variables
	edges = G.edges()
	f_min = None
	e_max = None
	# Loop on edges
	for e in edges:
		# Nodes of the current edge
		u = e[0]
		v = e[1]
		# Flow of the current edge
		f = G.edge[u][v]['flow']
		# Min flow control
		if f < f_min or f_min is None:
			# Min value update
			f_min = f
			e_max = (u, v)
	# Result
	return (f_min, e_max)

def complete_water_fill(G, traffic_matrix, depth = 6):
	'''
	Load flow values for the G's edges, according to the water filling principle and values indicated
	into the traffic matrix
	'''
	nodes = G.nodes()
	# Attach flows to edges
	for u in nodes:
		for v in nodes:
			# Flow to assign is traffic u->v: it must be a positive number
			f = traffic_matrix[u][v]
			if f > 0:
				# If nodes u and v are already connected by an edge, I can directly assign to it the flow
				if G.edge[u].has_key(v):
					G.edge[u][v]['flow'] += f
				else:
					# Paths between u and v
					# To avoid memory problems, the search depth is limited
					max_depth = len(G.nodes()) - 1
					found = False
					while not found:
						paths = list(nx.all_simple_paths(G, u, v, cutoff = depth))
						found = len(paths) > 0
						# If no path is found, I try to go deeper
						if not found:
							if depth < max_depth:
								depth = min(depth + 3, max_depth)
							else:
								# There are not paths between the nodes u and v: exit from the loop
								break
					if not found:
						# Error: "u" and "v" are not connected each other
						G = None
					else:
						# Distribute f over edges of every found path
						G = water_fill(G, paths, f)
	return G

def water_fill(T, paths, f):
	'''
	This function loads edges of the specified "paths" belonging to the graph "T", according to the
	flow value "f"; the first path to be loaded is the one whose max flow value (between its edges' flow
	values) is the lowest one.
	=>  Water filling: emulates the increasing water level, while it covers (for example) steps of a 
	ladder. Steps' height differences are progressively hidden
	'''
	# Utility functions
	def path_max_flow(G, path):
		'''
		This function returns the max flow value between edges of the specified path
		'''
		# "path" is a list of nodes, which form the path in the specified order
		f_max = None
		for i in range(len(path) - 1):
			# Nodes and flow of the edge
			u = path[i]
			v = path[i+1]
			f = G.edge[u][v]['flow']
			# Verify maximum value
			if f > f_max:
				f_max = f
		# Result
		return f_max

	def paths_max_flow(G, paths):
		'''
		This function computes, for every specified path, the maximum flow values between its edges.
		These values are then returned as a list of dictionaries (path, max_flow), ordered by
		ascending path associated flow value
		'''
		# Init result variable
		f_paths = []
		# Loop over paths
		for p in paths:
			# Evaluate max flow value for the current path
			f = path_max_flow(G, p)
			# Save the result
			el = {
				'path': p,
				'max_flow': f
			}
			f_paths.append(el)
		# Order by ascending flow value
		f_paths.sort(key = (lambda x: x['max_flow']))
		# Result
		return f_paths

	# The flow to assign must be positive: otherwise, exit
	if f > 0:
		# First of all, evaluate the maximum flow values between path's edges (ordering by ascending flow value)
		paths_with_flow = paths_max_flow(T, paths)
		# "remaining_quota" is the flow portion we still have to assign
		remaining_quota = f
		# "paths_batch" is the number of paths we are loading, in the same moment
		paths_batch = 1
		# Now, redistribute the entire flow
		while remaining_quota > 0:
			# paths' flows are disposed as a ladder: every time I redistribute "f",
			# first "paths_batch" steps of the ladder have the same height.
			if paths_batch < len(paths):
				# "step" is the height gap between the first non-leveled step of the ladder and the previous ones 
				step = paths_with_flow[paths_batch]['max_flow'] - paths_with_flow[paths_batch-1]['max_flow']
				# In order to fill this gap, these two steps must have different height
				if step > 0:
					# Now, I have to verify if the remaining quota cover entirely this gap
					if step * paths_batch <= remaining_quota:
						# Load flows, without any problems: the gap will be entirely covered
						quota = step
						remaining_quota -= step * paths_batch
						# Loop over the batch of paths, on which I load their edges' flows
						for i in range(paths_batch):
							# Current path
							p = paths_with_flow[i]['path']
							# Loop over path's edges, attaching the flow
							for j in range(len(p) - 1):
								u = p[j]
								v = p[j+1]
								T.edge[u][v]['flow'] += quota							
					else:
						# Load flows, for the last time
						# In fact, I know that I will not be able to fill the height gap
						quota = float(remaining_quota) / paths_batch
						# Loop over the batch of paths, on which I load their edges' flows
						for i in range(paths_batch):
							# Current path
							p = paths_with_flow[i]['path']
							# Loop over path'sedges, attaching them a flow
							for j in range(len(p) - 1):
								u = p[j]
								v = p[j+1]
								T.edge[u][v]['flow'] += quota
				# New path in my batch
				paths_batch += 1
			else:
				# If I have not covered every gap, but I still have flow to redistribute, 
				# this will be assigned proportionally to every path 
				quota = remaining_quota / paths_batch
				# Loop over paths, on which I increment flow values
				for x in paths_with_flow:
					# Current path
					p = x['path']
					# Loop over path's edges, attaching them flow values
					for j in range(len(p) - 1):
						u = p[j]
						v = p[j+1]
						T.edge[u][v]['flow'] += quota
	return T

def get_flow_labels(G):
	'''
	Returns as a dictionary pairs "edge - flow", rounding its value at 2 decimal digits.
	Format is compatible with the one requested by NetworkX, in order to visualize and print
	the resulting topology.
	'''
	# First of all, retrieve edges' flow values
	edge_labels = nx.get_edge_attributes(G, 'flow')
	# Now, round them at 2 decimal digits
	# key = tuple of the edge's nodes, value = rouded flow value
	items = map(lambda x: (x[0], round(x[1], 2)), edge_labels.items())
	# Rebuild the dictionary, with the new flow values
	edge_labels = {}
	for i in items:
		edge_labels[i[0]] = i[1]
	# Result
	return edge_labels
