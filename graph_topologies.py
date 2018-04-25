import random
import networkx as nx
import input_controls as inc


def ring_topology(n_nodes):
	'''
	This function generates an oriented ring topology, whose edges' flow values are null
	'''
	G = nx.DiGraph()
	G.add_cycle(list(range(n_nodes)), flow = 0)
	return G

def loaded_ring_topology(n_nodes, traffic_matrix):
	'''
	This function generates an oriented ring topology, whose edges' flow values are computed
	according to the traffic matrix content
	'''
	# Creting the ring
	G = ring_topology(n_nodes)
	# Load flows on the edges, according to the "water filling" principle
	G = flows.complete_water_fill(G, traffic_matrix)
	# Result 
	return G

def mesh_topology(n_nodes):
	'''
	This function generates a full mesh oriented topology, wihout self-loops. Edges' flow values
	are null
	'''
	# Creating an empty oriented graph
	G = nx.DiGraph()
	# Nodes of the topology
	nodes = range(n_nodes)
	# Instantiate the full mesh topology
	for u in nodes:
		for v in nodes:
			# No self-loops
			if u != v:
				# Creating edge u->v
				G.add_edge(u, v, flow = 0)
	# Result
	return G

def loaded_mesh_topology(n_nodes, traffic_matrix):
	'''
	This function create a n oriented full-mesh topology, without self.loops, assigning to edges a flow
	value according to the traffic matrix content
	'''
	# Creating empty oriented graph
	G = nx.DiGraph()
	# Nodes of the topology
	nodes = range(n_nodes)
	# Instantiate the full mesh topology
	for u in nodes:
		for v in nodes:
			# No self-loops
			if u != v:
				# Creating edge u->v, whose flow is equal to "traffic_matrix[u][v]"
				G.add_edge(u, v, flow = traffic_matrix[u][v])
	# Result
	return G

def random_topology(n_nodes, n_edges, delta_in, delta_out):
	'''
	This function creates and returns an oriented graph, whose topology id randomly defined.
	- "n_nodes" is the required number of nodes to create
	- "n_edges" is the required number of edges to create
	- "delta_in" is the constraint on the maximum number of receivers per node
	- "delta_out" is the constraint on the maximum number of transmitters per node
	'''
	# INPUT CONTROL
	# I cannot obtain a feasible topology if:
	if n_edges > n_nodes * max(delta_in, delta_out):
		print 'Delta constraint not satisfied...'
		return None
	if n_edges > n_nodes * (n_nodes-1):
		print 'More edges than a full-mesh...'
		return None
	if n_edges < n_nodes:
		print 'Less edges than a ring...'
		return None

	# Create oriented empty graph
	G = nx.DiGraph()
	# Nodes of the topology
	nodes = range(n_nodes)
	G.add_nodes_from(nodes)
	# Starting ring topology (the order of the nodes disposal is random)
	random.shuffle(nodes)
	G.add_cycle(nodes, flow = 0.0)
	# Creating possible edges
	possible_edges = []
	for u in nodes:
		for v in nodes:
			# No self-loops
			if u != v:
				e = (u, v)
				possible_edges.append(e)
	random.shuffle(possible_edges)
	# Add edges to the graph, until the "n_edges" constraint is satisfied
	for e in possible_edges:
		# If I have reached the required number of edges in the topology, I stop
		if len(G.edges()) == n_edges:
			break
		# Current edge nodes
		u, v = e
		# Check if these nodes can be directly connected
		u_out_deg = G.out_degree()[u]
		v_in_deg = G.in_degree()[v]
		if u_out_deg < delta_out and v_in_deg < delta_in:
			# Add the edge to the topology: if it already exists, I simply have no alterations
			G.add_edge(u, v, flow = 0.0)
	# If the obtained topology is not feasible yet, I have to force the entering of extra edges
	found = True
	while len(G.edges()) < n_edges and found:
		# La flag torna ad essere vera se riesco ad inserire un nuovo arco nella topologia
		found = False
		# Focus on nodes for which the delta constraint is not satisfied yet
		# Let us call "candidate node - u" a node for which I still can add exiting edges
		candidate_us = map(lambda x: x[0], filter(lambda x: x[1] < delta_out, G.out_degree().items()))
		# Let us call "candidate node - v" a node for which I still can add entering edges
		candidate_vs = map(lambda x: x[0], filter(lambda x: x[1] < delta_in, G.in_degree().items()))
		# It may be that some of the candidate "u"s are, at the same moment, candidate "v"s
		candidate_both = filter(lambda x: x in candidate_vs, candidate_us)
		# CASE 1: if a common candidate "z" exists, then I remove an edge "s-d" in order to create a path "s-z-d"
		if len(candidate_both) > 0:
			random.shuffle(candidate_both)
			# Looking for a candidate "z" for which exists, in the topology, an edge "s-d" (with "s" and "d" different from "z")
			for z in candidate_both:
				for e in G.edges():
					s, d = e
					if s != z and d != z:
						# I can remove the edge and create the path
						found = True
						G.remove_edge(s, d)
						G.add_edge(s, z, flow = 0.0)
						G.add_edge(z, d, flow = 0.0)
						# Exit the for loop on "e"
						break
				if found:
					# Exit the for loop on "z"
					break
		if not found:
			# CASE 2: case 1 is not feasible, or it hasn't worked. The idea now is to look for two candidates "u" and "v",
			# connected by the edge "u-v", and look for an edge "s-d" in the topology where "s" and "d" are different from
			# "u" e "v". If its removal does not disconnect the graph, we remove the edge "s-d" in order to create, instead, 
			# edges "u-d" and "s-v"
			def u_ok(x):
				for v in candidate_vs:
					if G.edge[x].has_key(v):
						return True
				return False
			us_connected_to_v = filter(u_ok, candidate_us)
			random.shuffle(us_connected_to_v)
			for u in us_connected_to_v:
				vs_connected_to_u = filter(lambda x: G.edge[u].has_key(x), candidate_vs)
				random.shuffle(vs_connected_to_u)
				for v in vs_connected_to_u:
					# Once defined "u" and "v", we look for an edge "s-d"
					for e in G.edges():
						s, d = e
						# Control flag over edge's nodes
						s_ok = s != u and s != v and (not G.edge[s].has_key(v))
						d_ok = d != u and d != v and (not G.edge[u].has_key(d))
						if s_ok and d_ok:
							# Control if I can remove the edge
							if has_alternative_paths(G, e):
								found = True
								G.remove_edge(s, d)
								G.add_edge(s, v, flow = 0.0)
								G.add_edge(u, d, flow = 0.0)
						if found:
							# Exit from the for loop on "e"
							break
					if found:
						# Exit from the for loop on "v"
						break
				if found:
					# Exit from the for loop on "u"
					break
		if not found:
			# CASE 3: third and last possible case (extremely rare). Previous alterations in the topology have created
			# candidate "u"s and "v"s which can be directly connected by an edge u->v
			random.shuffle(candidate_us)
			random.shuffle(candidate_vs)
			# Look for a pair of nodes I can connect
			for u in candidate_us:
				for v in candidate_vs:
					if not G.edge[u].has_key(v):
						G.add_edge(u, v, flow = 0.0)
						found = True
					if found:
						# Exit from the for loop on "v"
						break
				if found:
					# Exit from the for loop on "u"
					break
	# Final check
	if len(G.edges()) != n_edges:
		G = None
	# Result
	return G

def manhattan_topology(r, c = None, derived = None):
	'''
	The function returns a manhattan topology rxc
	- "r": number of rows
	- "c": number of nodes per row (default: "r")
	- "derived": Manhattan topology from which compute the result (swap nodes)
	=> In total, nodes in the topology are "n_nodes" = r*c
	'''
	# INPUT CONTROL
	if c is None:
		c = r
	# R
	inc.check_integer(r, 'r', minValue = 2)
	# C
	inc.check_integer(c, 'c', minValue = 2)
	# derived
	if derived is not None:
		inc.check_DiGraph(derived, 'derived')

	# Create the graph
	G = nx.DiGraph()
	# Create nodes
	n_nodes = r * c
	nodes = list(range(n_nodes))
	G.add_nodes_from(nodes)
	# Create edges (oriented)
	# If derived is not specified, nodes' disposal is the standard one
	if derived is None:
		for u in nodes:
			# Up: first row control
			if u < c:
				v = u + n_nodes - c 	# connect to last row
			else:
				v = u - c
			G.add_edge(u, v, flow = 0.0)
			# Right: control last column
			if (u+1) % c == 0:
				v = u - c + 1			# connect to first column (left most)
			else:
				v = u + 1
			G.add_edge(u, v, flow = 0.0)
			# Down: last row control
			if u >= n_nodes - c:
				v = u - n_nodes + c 	# cponnect to first row
			else:
				v = u + c
			G.add_edge(u, v, flow = 0.0)
			# Left: control first column
			if u % c == 0:
				v = u + c - 1			# connect to last column (right most)
			else:
				v = u - 1
			G.add_edge(u, v, flow = 0.0)
	# Otherwise, create edges according to nodes' names specified in the reference topology
	else:
		# Loop over nodes (positions)
		for n in nodes:
			# Retrieve n's name
			n_name = derived.node[n]['name']
			# Loop over nodes (positions) connected to n
			for x in derived.edge[n].keys():
				# Retrieve current node name
				x_name = derived.node[x]['name']
				# Create correct edge in the new topology (swapped node)
				G.add_edge(n_name, x_name, flow = 0.0)
	# Result
	return G


if __name__ == '__main__':
	x = True
	i = 0
	while x is not None:
		x = random_topology(4, 8, 2, 2)
		if x is not None:
			i = (i+1) % 100
			print 'ok%d' % (i)

def has_alternative_paths(G, e):
	'''
	This function verify that, on the graph G, if I remove the edge "e" between nodes "u" and "v"
	they are still connected by at least one path
	'''
	# Edge nodes and flow
	u = e[0]
	v = e[1]
	f = G.edge[u][v]['flow']
	# Temporary remove the edge from the topology
	G.remove_edge(u, v)
	# Verify the existance of alternative paths between "u" and "v"
	res = nx.has_path(G, u, v)
	# Reinsert the removed edge
	G.add_edge(u, v, flow = f)
	# Result
	return res