import LAB2_OpRes as L2
import graph_traffic_matrix as tm
import flow_utilities as flows

intro = 'LAB 02 - Ex. 01 and 02\nWe are going to test and compare the algorithms we have implemented\nTraffic matrix values are in range [0.5; 1.5]'
print(intro)

# Tests use different values for N and delta
ns = [3, 4, 6, 8, 10, 16, 20, 30, 40]
deltas = [1, 2, 3, 5, 7, 9, 15, 19, 25, 29, 35, 39]
# For every pair N - delta, I do a certain number of simulations (experiments)
n_simulations = 4

# TEST
# Open (write mode) the file in which print in output obtained results
res_file = 'res/results.txt'
try:
	with open(res_file, 'w') as fp:
		fp.write(intro + '\n')
		t = 1
		for n in ns:
			for delta in deltas:
				# In this exercise, delta_in and delta_out are always equal: let us call them "delta"
				# Anyway, if delta >= n the result is still a full mesh topology (I can jump the simulation)
				if delta >= n:
					continue
				# Estimated max flows, for every pair N-delta
				est_f_max = {
					'mesh': 0.0,
					'rnd_mesh': 0.0,
					'ring': 0.0,
					'rnd_ring': 0.0
				}
				# Estimated computational times, for every pair N-delta
				est_time = {
					'mesh': 0.0,
					'rnd_mesh': 0.0,
					'ring': 0.0,
					'rnd_ring': 0.0
				}
				# For each pair, I repeat more times the simulation
				for s in range(n_simulations):
					# Creating traffic matrix
					traffic_matrix = tm.random_TM(n, 0.5, 1.5)
					# Experiment number
					exp = 'Exp #%s, Sim #%s - ' % (str(t).zfill(2), str(s).zfill(2))
					# Information strings
					exp_info = '%sN = %d, delta = %d' % (exp, n, delta)
					mesh_title = '%sMesh LTD' % (exp)
					ring_title = '%sRing LTD' % (exp)
					random_mesh_title = '%sRandom vs Mesh' % (exp)
					random_ring_title = '%sRandom vs Ring' % (exp)
					print('\n\n%s' % (exp_info))
					# SOL 1 - Mesh vs Random
					T1 = None
					# While loop trick, in order to avoid traffic matrixes for which the Mesh algorithm fails (very rare!)
					while T1 is None:
						T1 = L2.greedy_LTD_mesh(n, traffic_matrix, delta, delta, mesh_title, userView = False, withLabels = False)
						if T1 is None:
							traffic_matrix = tm.random_TM(n, 0.5, 1.5)
					est_f_max['mesh'] += T1['max_flow']
					est_time['mesh'] += T1['time']
					T1_bis = L2.LTD_random(n, len(T1['topology'].edges()), delta, delta, traffic_matrix, random_mesh_title, userView = False, withLabels = False)
					est_f_max['rnd_mesh'] += T1_bis['max_flow']
					est_time['rnd_mesh'] += T1_bis['time']
					# SOL 2 - Ring vs Random
					T2 = L2.greedy_LTD_ring(n, traffic_matrix, delta, delta, ring_title, userView = False, withLabels = False)
					est_f_max['ring'] += T2['max_flow']
					est_time['ring'] += T2['time']
					T2_bis = L2.LTD_random(n, len(T2['topology'].edges()), delta, delta, traffic_matrix, random_ring_title, userView = False, withLabels = False)
					est_f_max['rnd_ring'] += T2_bis['max_flow']
					est_time['rnd_ring'] += T2_bis['time']
				# Compute estimates (mean value) and print results on the output file
				fp.write('\n=> Test #%s: N = %d, delta = %d\n' % (str(t).zfill(2), n, delta))
				fp.write('Max flow values, with computation times:\n')
				for k in est_f_max.keys():
					est_f_max[k] = round(est_f_max[k] / n_simulations, 2)
					est_time[k] = round(est_time[k] / n_simulations, 2)
					fp.write('%s = %g (%s s)\n' % (k.capitalize(), est_f_max[k], str(est_time[k]) if est_time[k] > 0.0 else '< 0.01'))
				# Next test 
				t += 1
except IOError:
	print('ERR - I/O error for the file "%s"' % (res_file))