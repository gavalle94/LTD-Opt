import LAB2_OpRes as L2
import graph_traffic_matrix as tm
import flow_utilities as flows

intro = 'LAB 02 - Ex. 04\nWe are going to test and compare the traffic routing over a Manhattan topology\nTraffic matrix values are in range [0.5; 1.5]'
print(intro)

# Tests use different values for N: delta, instead, is fixed to 4
ns  = [9, 12, 16, 20, 25, 30, 36, 40]
nrs = [3,  4,  4,  5,  5,  6,  6,  8]
ncs = [3,  3,  4,  4,  5,  5,  6,  5]
delta = 4
# For every N, I o a certain number of simulations
n_simulations = 4

# TEST
# Open (write mode) the output file, in which I print the obtained results 
res_file = 'res/results.txt'
try:
	with open(res_file, 'w') as fp:
		fp.write(intro + '\n')
		t = 1
		for i in range(len(ns)):
			# Number of nodes in the topology
			n = ns[i]
			# Obtain the number of nodes per row/column
			nr = nrs[i]
			nc = ncs[i]
			# Estimated max flow, for every N
			est_f_max = 0.0
			# Estimated computational time, for every N
			est_time = 0.0
			# For every N-nodes topology, I repeat the simulation several times
			for s in range(n_simulations):
				# Creating traffic matrix
				traffic_matrix = tm.random_TM(n, 0.5, 1.5)
				# Experiment number
				exp = 'Exp #%s, Sim #%s - ' % (str(t).zfill(2), str(s).zfill(2))
				# Information strings
				exp_info = '%sN = %d, Nr = %d, Nc = %d' % (exp, n, nr, nc)
				title = '%sManhattan LTD' % (exp)
				print('\n\n%s' % (exp_info))
				# SOLUTION
				T = L2.LTD_manhattan(n, nr, nc, traffic_matrix, title, False, False)
				est_f_max += T['max_flow']
				est_time += T['time']
			# Compute estimates (mean value) and output on file
			fp.write('\n=> Test #%s: N = %d, Nr = %d, Nc = %d\n' % (str(t).zfill(2), n, nr, nc))
			est_f_max = round(est_f_max / n_simulations, 2)
			est_time = round(est_time / n_simulations, 2)
			fp.write('Max flow value: %f\nComputation time: %f\n' % (est_f_max, est_time))
			# Next test 
			t += 1
except IOError:
	print('ERR - I/O error for the file "%s"' % (res_file))