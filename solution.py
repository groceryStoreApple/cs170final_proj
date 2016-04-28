import networkx as nx
import matplotlib.pyplot as plt
import tarjan as tj

def construct_graph(instance_name):
	f = open(instance_name)
	G = nx.DiGraph()
	content = [line.rstrip('\n') for line in f]
	num_of_lines = len(content)
	num_of_vertex = int(content[0])
	for i in range(num_of_vertex):
		G.add_node(i,child = False)
	children = content[1].split(' ')
	for child in children:
		c = int(child)
		G.node[c]['child'] = True

	for i in range(2,num_of_lines):
		line = content[i].split(' ')
		for j in range(len(line)):
			if int(line[j]):
				G.add_edge(i-2,j)
	f.close()
	return G

def construct_graph_for_tarjan(graph):
	result = {}
	num_of_vertex = 0
	for v in nx.nodes(graph):
		result[v] = nx.all_neighbors(graph,v)
		num_of_vertex += 1
	print "there are " +str(num_of_vertex) + "vertices"
	return result

def tarjan_algo(graph):
	print tj.tarjan(graph)

def find_all_scc():
	for i in range(1,492):
		filename = "phase1-processed/"+str(i)+".in"
		g = construct_graph(filename)
		dict = construct_graph_for_tarjan(g)
		tarjan_algo(dict)

def find_all_cycle(graph):
	# graph_gen = nx.simple_cycles(graph)
	# while (1):
	# 	cycle = graph_gen.next()
	# 	if len(cycle) <6:
	# 		print cycle
	vertices = graph.nodes()
	cycles = []
	for vertex in vertices:
		cycle = find_cycle(graph,vertex,vertex,5)
		print cycle
		cycles += cycle
	print len(cycles)

def find_cycle(graph, start, end, depth, path=[]):
	if depth == 0:
		return None
	path = path + [start]
	paths = []
	for v in nx.all_neighbors(graph,start):
		if v == end:
			paths.append(path)
		elif v not in path:
			newpaths = find_cycle(graph,v,end,depth-1,path)
			if newpaths:
				paths += newpaths
	return paths




def find_unique_cycle(cycles):
	unique_cycles = []
	unique = [True] * len(cycles)
	for i in range(0, len(cycles)):
		if not unique[i]:
			continue
		for j in range(0, len(cycles)):
			if i == j:
				continue
			if list(set(cycles[i]) & set(cycles[j])):
				unique[i] = False
				unique[j] = False
		if unique[i]:
			unique_cycles.append(cycles[i])
	remain_cycles = [c for i, c in enumerate(cycles) if not unique[i]]
	print unique_cycles
	print remain_cycles
	return unique_cycles, remain_cycles



def main():
	# g = construct_graph()
	# find_all_cycle(g)

	cycles = [[5, 2], [2, 5], [2, 6], [8, 4]]
	find_unique_cycle(cycles)


if __name__ == "__main__":
	main()