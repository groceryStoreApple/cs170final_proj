import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tarjan as tj


def construct_graph(instance_name):
	f = open(instance_name)
	G = nx.DiGraph()
	content = [line.rstrip('\n') for line in f]
	num_of_lines = len(content)
	num_of_vertex = num_of_lines - 2
	for i in range(num_of_vertex):
		G.add_node(i,child = False)
	children = content[1].split(' ')
	for child in children:
		if not (child == '' or child == ' ' or child == '\n' or not child):
			try:
				c = int(child)
			except:
				continue
			G.node[c]['child'] = True
	for i in range(2,num_of_lines):
		line = content[i].split(' ')
		for j in range(len(line)):
			try:
				num = int(line[j])
			except:
				continue
			if num:
				G.add_edge(i-2,j)
	f.close()
	return G

def construct_graph_for_tarjan(graph):
	result = {}
	num_of_vertex = 0
	for v in nx.nodes(graph):
		result[v] = nx.all_neighbors(graph,v)
		num_of_vertex += 1
	# print "there are " +str(num_of_vertex) + "vertices"
	return result

def solve_all():
	for i in range(1,492):
		filename = "phase1-processed/"+str(i)+".in"
		print filename
		g = construct_graph(filename)
		instance_solver(g)

def instance_solver(graph):
	solution_set = []
	graph,solution_set,largest_scc_size = scc_screening(graph,solution_set)
	# children_cycles = find_all_children_cycle(graph)

	while largest_scc_size>5:
		graph_copy = graph.copy()
		most_constricted_vertex = find_most_constricted(graph_copy)
		cycle = find_one_cycle_length_five(graph,most_constricted_vertex,most_constricted_vertex,5)
		
		while not cycle:
			graph_copy.remove_node(most_constricted_vertex)
			most_constricted_vertex = find_most_constricted(graph_copy)
			cycle = find_one_cycle_length_five(graph,most_constricted_vertex,most_constricted_vertex,5)
		
		print cycle
		solution_set.append(cycle)
		graph.remove_nodes_from(cycle)
		graph,solution_set,largest_scc_size = scc_screening(graph,solution_set)

	print "number of vertices uncovered" + str(graph.nodes())
	return solution_set

def find_most_constricted(graph):
	most_constricted = -1
	smallest_in_degree = 999999999
	for v in graph.nodes():
		in_degree = graph.in_degree(v)
		if in_degree < smallest_in_degree:
			smallest_in_degree = in_degree
			most_constricted = v
	return most_constricted

def scc_screening(graph,solution_set):
	graph, new_solution, largest_scc_size = tarjan_algo(graph)
	solution_set.append(new_solution)
	return graph, solution_set,largest_scc_size

def tarjan_algo(graph):
	largest_scc_size = 0
	dict = construct_graph_for_tarjan(graph)
	sccs =  tj.tarjan(dict)
	dead_people = []
	solution_set = []
	for scc in sccs:
		if len(scc) > largest_scc_size:
			largest_scc_size = len(scc)
		if len(scc) == 1:
			dead_people.append(scc[0])
		elif len(scc)<6:
			solution_set.append(scc)#####order the vertices.
	for person in dead_people:
		graph.remove_node(person)
	for scc in solution_set:
		graph.remove_nodes_from(scc)
	return graph, solution_set, largest_scc_size

def find_all_children_cycle(graph):
	vertices = graph.nodes()
	cycles = []
	for vertex in vertices:
		if graph.node[vertex]['child']:
			cycle = find_one_cycle(graph,vertex,vertex,5)
			if cycle:
				# print cycle
				cycles.append(cycle)
	return cycles

def find_one_cycle_length_five(graph,start,end,depth,path=[]):
	if depth == 0:
		if start == end:
			return path
		return None
	path = path + [start]
	for v in nx.all_neighbors(graph,start):
		if not graph.node[v]['child']:
			continue
		elif v not in path:
			return find_one_cycle(graph,v,end,depth-1,path)

def find_one_cycle(graph, start, end, depth,path=[]):
	if depth == 0:
		return None
	path = path + [start]
	for v in nx.all_neighbors(graph,start):
		if not graph.node[v]['child']:
			continue
		elif v == end:
			return path
		elif v not in path:
			return find_one_cycle(graph,v,end,depth-1,path)

def find_cycle(graph, start, end, depth, path=[]):
	if depth == 0:
		return None
	path = path + [start]
	paths = []
	for v in nx.all_neighbors(graph,start):
		if not graph.node[v]['child']:
			continue
		elif v == end:
			# paths.append(path)
			return [path]
		elif v not in path:
			newpaths = find_cycle(graph,v,end,depth-1,path)
			if newpaths:
				paths += newpaths
	return paths

def find_unique_cycle(cycles, k):
	unique_cycles = []
	remain_cycles = []
	unique = [True] * len(cycles)
	for i in range(0, len(cycles)):
		if not unique[i]:
			remain_cycles.append(cycles[i])
			continue
		for j in range(0, len(cycles)):
			if i == j:
				continue
			if len(list(set(cycles[i]) & set(cycles[j]))) > k:
				unique[i] = False
				unique[j] = False
		if unique[i]:
			unique_cycles.append(cycles[i])
		else:
			remain_cycles.append(cycles[i])
	# print unique_cycles
	# print remain_cycles
	return unique_cycles, remain_cycles

def delete_duplicate_cycle(cycles):
	canonical_cycles = []
	for c in cycles:
		min_index = c.index(min(c))
		canonical_c = c[min_index:] + c[:min_index]
		canonical_cycles.append(canonical_c)
	unique_cycles = []
	unique = [True] * len(canonical_cycles)
	for i in range(0, len(canonical_cycles)):
		if not unique[i]:
			continue
		for j in range(0, len(canonical_cycles)):
			if i == j:
				continue
			if np.array_equal(canonical_cycles[i], canonical_cycles[j]):
				unique[j] = False
		if unique[i]:
			unique_cycles.append(canonical_cycles[i])
	return unique_cycles

def delete_cycle(G, cycles):
	G.remove_nodes_from(cycles)
	return G

# def naive_greedy(G):
# 	donation_chain = []
# 	cycles = find_all_cycle(G)
# 	unique_cycles, remain_cycles = find_unique_cycle(cycles)
# 	for c in unique_cycles:
# 		donation_chain.append(c)
# 		G = delete_cycle(G, c)
# 	for i,c in enumerate(remain_cycles):

def main():
	g = construct_graph("instances/10.in")
	new_g, sccs, size = scc_screening(g, [])
	cycles = find_all_children_cycle(new_g)
	new_cycles = delete_duplicate_cycle(cycles)

if __name__ == "__main__":
	main()