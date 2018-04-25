import time
import warnings
import networkx as nx
import matplotlib.pyplot as plt
import input_controls as inc
import flow_utilities as flows


def input_control(n, traffic_matrix, delta_in, delta_out):
	'''
	this function verify that the input parameters for greedy algorithms are valid.
	Functions of the "input_controls" library are used.
	'''
	# Number of nodes
	inc.check_integer(n, "n", minValue = 1)
	# Traffic matrix
	inc.check_array(traffic_matrix, "traffic_matrix", dimensions = 2, of = (int, long, float))
	# Delta_in
	inc.check_integer(delta_in, "delta_in", minValue = 1)
	# Delta_out
	inc.check_integer(delta_out, "delta_out", minValue = 1)

def check_global_delta_constraints(G, delta_in, delta_out):
	'''
	This function verify that the input/output degrees of the graph's nodes respect the delta constraints
	(maximum number of transmitters/receivers per node)
	'''		
	res = True
	# Input/output degrees of the graph's nodes
	in_deg = G.in_degree()
	out_deg = G.out_degree()
	# Verify delta constraints
	for x in G.nodes():
		if in_deg[x] > delta_in or out_deg[x] > delta_out:
			res = False
			break
	# Result
	return res

def str_nodes(G):
	'''
	This function returns, as well formatted string, the list of nodes of the graph "G"
	'''
	nodes = G.nodes()
	return 'Nodes (%d):\n%s' % (len(nodes), ', '.join(map(lambda x: str(x), nodes)))

def str_edges(G):
	'''
	This function returns, as well formatted string, the list of edges of the graph "G"
	'''
	def format_edge(e):
		# Utility function, used to format as a string a single edge
		u = e[0]
		v = e[1]
		f = round(G.edge[u][v]['flow'], 2)
		return '%s -> %s, flow = %s' % (u, v, f)
	# Format every G's edge
	list_edges = map(format_edge, G.edges())
	# Return the list as a single string
	return 'Edges (%d):\n%s' % (len(list_edges), '\n'.join(list_edges))

def str_max_flow(G):
	'''
	This function returns, as a well formatted string, the information associated to the maximum
	flow between graph "G" edges
	'''
	(f_max, e_max) = flows.max_flow(G)
	return 'Max flow: %s units, on the edge %s' % (round(f_max, 2), e_max)

def str_min_flow(G):
	'''
	This function returns, as a well formatted string, the information associated to the minimum
	flow between graph "G" edges
	'''
	(f_min, e_max) = flows.min_flow(G)
	return 'Min flow: %s units, on the edge %s' % (round(f_min, 2), e_max)

def str_info_flow(G):
	'''
	This function returns, as a well formatted string, the extra information about flow values distribution
	of the "G" graph edges we are considering
	'''
	maxF = flows.max_flow(G)[0]
	minF = flows.min_flow(G)[0]
	flow_range = round(maxF - minF, 2)
	flow_perc = round(flow_range*100.0/maxF, 2)
	return 'Flow traffic values are in a range of %s units (%s%% wrt the maximum value)' % (flow_range, flow_perc)

def str_res(G, delta_in, delta_out):
	'''
	The function returns, as a well formatted string, obtained results in a "compact" way
	'''
	if delta_in == delta_out:
		data = 'N = %d, delta = %d' % (len(G.nodes()), delta_in)
	else:
		data = 'N = %d, delta_in = %d, delta_out = %d' % (len(G.nodes()), delta_in, delta_out)
	max_f = 'Estimated max flow = %g' % round(flows.max_flow(G)[0], 2)
	return data + '\n' + max_f + '\n'

def str_time(t):
	'''
	The function returns, as a well formatted string, the computational time required to solve the LTD
	problem (in seconds)
	'''
	return 'Computation time: %g seconds' % (t)

def result(T, traffic_matrix, delta_in, delta_out, initial_time, title, userView, withLabels, approach, depth = 6):
	'''
	This function returns the final data structure (composed by the topology, computational required time and max flow
	values between the edges in the topologies), giving to the user as output the obtained results information
	- "T": evaluated topology from the LTD algorithm
	- "traffic_matrx": traffic matrix, used to evaluate flows of T's edges
	- "delta_in": constraint on the maximum number of receivers per node
	- "delta_out": constraint on the maximum number of transmitters per node
	- "initial_time": computation initial time (in seconds)
	- "title": graph's title
	- "userView": boolean, if True the graph and the log information are visualized on screen (instead that on a text file)
	- "withLabels": boolean, if True the topology photo has the flow printed on aedges (as labels)
	- "approach": approach of the adopted LTD algorithm
	- "depth": maximum depth for the path research, between pairs of nodes
	'''
	# Check the validity of the solution
	if check_global_delta_constraints(T, delta_in, delta_out):
		print('%s approach topology is ready. Routing...' % (approach))
		# Load flows on the topology's edges
		T = flows.complete_water_fill(T, traffic_matrix, depth)
		# information for the user
		print('=> %s solution found!' % (approach))
		# Computation end time and final result
		end_time = time.time()
		computation_time = round(end_time - initial_time, 2)
		res = {
			'topology': T,
			'time': computation_time,
			'max_flow': flows.max_flow(T)[0]
		}
		end(T, delta_in, delta_out, computation_time, title, userView, withLabels)
	else:
		print('ERR - %s solution not found!' % (approach))
		res = None
	# Result
	return res

def end(G, delta_in, delta_out, computation_time, title = '', userView = True, withLabels = True):
	'''
	At the end of the heuristic, I check to have found a valid solution: in that case, obtained results
	are printed at screen or in an output text file
	- "G" is the resulting topology
	- "delta_in" is the constraint on the maximum number of receivers per node
	- "delta_out" is the constraint on the maximum number of transmitters per node
	- "title" is the graph's title and the name of the output files
	- "userView" is a flag, used to decide if final results have to be printed on screen (True) or on a text file (False)
	'''
	# User useful information
	nodes = str_nodes(G)
	edges = str_edges(G)
	time_info = str_time(computation_time)
	max_flow = str_max_flow(G)
	min_flow = str_min_flow(G)
	info_flow = str_info_flow(G)
	log = '\n'.join([nodes, edges, time_info, max_flow, min_flow, info_flow])
	res = str_res(G, delta_in, delta_out)
	# Create the graph and output results
	with warnings.catch_warnings():
		# Disable version warning (for the library "matplotlib")
		warnings.simplefilter("ignore")
		# Graph layout 
		layout = nx.spring_layout(G)
		# Draw nodes and edges
		nx.draw_networkx(G, pos = layout, node_size = 200)
		# Decide if labels have to be drawn
		if withLabels:
			edge_labels = flows.get_flow_labels(G)
			nx.draw_networkx_edge_labels(G, pos = layout, edge_labels = edge_labels, label_pos = 0.65)
		# Disable cartesian axis
		plt.axis('off')
		# Graph's title
		plt.title(title)
		# "userView" flag decides how to output the final results to the user
		if userView:
			# If True, print on screen the log and open the graphical window
			print(log)
			plt.show()
		else:
			# If False, save the log on and the final results on text filesand the photo of the topology as an image
			basename = title.replace('.', '')
			file_log = 'log/%s.txt' % (basename)
			file_img = 'img/%s.png' % (basename)
			try:
				with open(file_log, 'w') as fp:
					fp.write(log)
			except:
				print('ERR - I/O problems with the file "%s"' % (file_log))
			plt.savefig(file_img, format="PNG", bbox_inches='tight')
			# Close the graphical window, to avoid the overlap of the next one (hold)
			plt.close()
