import LAB2_OpRes as L2
import graph_traffic_matrix as tm
import flow_utilities as flows

intro = 'LAB 02 - Ex. 05\nWe are going to test and compare the traffic routing over a Manhattan topology\nTraffic matrix values are in range [0.5; 1.5]'
print(intro)

# tests will use different N values: delta, instead, is fixed to 4
ns  = [9, 12, 16, 20, 25, 30, 36, 40]
nrs = [3,  4,  4,  5,  5,  6,  6,  8]
ncs = [3,  3,  4,  4,  5,  5,  6,  5]
delta = 4
# For every N value I do several simulations
n_simulations = 4

# PLEASE NOTE
# We will call "A" the first non-optimized solution (same as ex04), "B" the optimized one

# TEST
# Open output file in read mode
res_file = 'res/results.txt'
try:
	with open(res_file, 'w') as fp:
		fp.write(intro + '\n')
		t = 1
		for i in range(len(ns)):
			# Number of nodes in the topology
			n = ns[i]
			# Retrieve number of nodes per row/column
			nr = nrs[i]
			nc = ncs[i]
			# Estimated max flow, for every N
			est_f_max_A = 0.0
			est_f_max_B = 0.0
			# Estimated computational time, for each N
			est_time_A = 0.0
			est_time_B = 0.0
			# FOr every N-nodes topology, repeat th simulation several times
			for s in range(n_simulations):
				# Compute traffic matrix (same for A and B)
				traffic_matrix = tm.random_TM(n, 0.5, 1.5)
				# Experiment number
				exp = 'Exp #%s, Sim #%s - ' % (str(t).zfill(2), str(s).zfill(2))
				# Information strings
				exp_info = '%sN = %d, Nr = %d, Nc = %d' % (exp, n, nr, nc)
				title = '%sManhattan LTD' % (exp)
				print('\n\n%s' % (exp_info))
				# SOLUTION
				# Non-optimized
				T_A = L2.LTD_manhattan(n, nr, nc, traffic_matrix, title, False, False)
				est_f_max_A += T_A['max_flow']
				est_time_A += T_A['time']
				# Optimized
				title = '%sManhattan LTD Smart' % (exp)
				T_B = L2.LTD_manhattan_smart(n, nr, nc, traffic_matrix, title, False, False)
				est_f_max_B += T_B['max_flow']
				est_time_B += T_B['time']
			# Compute estimates (mean values) and output on file
			fp.write('\n=> Test #%s: N = %d, Nr = %d, Nc = %d\n' % (str(t).zfill(2), n, nr, nc))
			est_f_max_A = round(est_f_max_A / n_simulations, 2)
			est_time_A = round(est_time_A / n_simulations, 2)
			est_f_max_B = round(est_f_max_B / n_simulations, 2)
			est_time_B = round(est_time_B / n_simulations, 2)
			fp.write('A) Max flow value: %f\nComputation time: %f\n' % (est_f_max_A, est_time_A))
			fp.write('B) Max flow value: %f\nComputation time: %f\n' % (est_f_max_B, est_time_B))
			# Next test 
			t += 1
except IOError:
	print('ERR - I/O error for the file "%s"' % (res_file))