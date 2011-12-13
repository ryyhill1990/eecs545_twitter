import sys

if len(sys.argv) != 3:
	print "Run with \'python " + sys.argv[0] + " <input filename> <output prefix>\'"
	sys.exit()	
f = open(sys.argv[1], 'r')
graph = []
id_count = 0
edges_count = 0

for line in f:
	id_count = id_count + 1
	adjacency_list = []
	for adjacent_score in line.split():
		score = float(adjacent_score)
		score = score * 1000000
		adjacency_list.append(int(score))
	graph.append(adjacency_list)

edges_count = 0
for adjacency_list in graph:
	edges_count = edges_count + sum (1 for adjacent in adjacency_list if adjacent > 0) 
edges_count = edges_count / 2


g = open(sys.argv[2] + "_metis.graph", 'w')
g.write(str(len(graph)))
g.write('  ')
g.write(str(edges_count))
g.write('  ')
g.write('001')
g.write('\n')
count = 0

for adjacency_list in graph:
	adjacent_id = 0
	for adjacent in adjacency_list:
		adjacent_id = adjacent_id + 1
		if adjacent > 0:
			g.write(str(adjacent_id))
			g.write(' ')
			g.write(str(adjacent))
			g.write(' ')
	g.write('\n')
