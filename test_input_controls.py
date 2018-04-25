import input_controls as inc
import networkx as nx

s = 'prova'

print('controllo interi:')
inc.check_integer(8, s)
inc.check_integer(8, s, minValue = 2)
inc.check_integer(8, s, minValue = 8)
inc.check_integer(8, s, maxValue = 10)
inc.check_integer(8, s, maxValue = 8)
inc.check_integer(8, s, minValue = 5, maxValue = 18)
inc.check_integer(8, s, minValue = 8, maxValue = 8)
try:
	inc.check_integer('o', s)
except:
	print('ok1')
try:
	inc.check_integer(8, s, minValue = 'k')
except:
	print('ok2')
try:
	inc.check_integer(8, s, maxValue = 'o')
except:
	print('ok3')
try:
	inc.check_integer(8, s, maxValue = 5)
except:
	print('ok4')
	pass
try:
	inc.check_integer(8, s, minValue = 15)
except:
	print('ok5')
print('END')



print('controllo grafo orientato')
G1 = nx.DiGraph()
G2 = nx.Graph()

inc.check_DiGraph(G1, s)
try:
	inc.check_DiGraph('ciao', s)
except:
	print('ok1')
try:
	inc.check_DiGraph(G2, s)
except:
	print('ok2')
print('END')



print('controllo nodi grafo')
G1.add_node(5)
G1.add_node('nodo')

inc.check_node_exists(5, G1)
inc.check_node_exists('nodo', G1)
try:
	inc.check_node_exists('ciao', G1)
except:
	print('ok1')
print('END')


print('controllo array')
l = list(range(4))
t = tuple(range(4))
ss = set(l)
m2 = [l, l]
m3 = [m2, m2]

inc.check_array(l, s)
inc.check_array(t, s)
inc.check_array(ss, s)
inc.check_array(m2, s)
inc.check_array(m3, s)
inc.check_array(m2, s, dimensions = 2)
inc.check_array(m3, s, dimensions = 3)
inc.check_array(m2, s, dimensions = 2, of = int)
inc.check_array(m3, s, dimensions = 3, of = (int, long))
try:
	inc.check_array(m2, s, 3)
except:
	print('ok1')
try:
	inc.check_array(l, s, 2)
except:
	print('ok2')
try:
	inc.check_array(m2, s, dimensions = 2, of = str)
except:
	print('ok3')
try:
	inc.check_array(m2, s, dimensions = 2, of = 'ciao')
except:
	print('ok4')
print('END')


print('controllo input utente')

inc.input_int('intero tra 1 e 5', 1, 5)
inc.input_int('intero tra -1 e 5', -1, 5)
inc.input_int('intero tra 1 e 1', 1, 1)
inc.input_float('float tra 1 e 6', 1, 6)
inc.input_float('float tra -5 e 5', -5, 5)
try: 
	inc.input_int('msg', 5, 1)
except:
	print('ok1')
try:
	inc.input_float('msg', 5, 1)
except:
	print('ok2')
print('END')