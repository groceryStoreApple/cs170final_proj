import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tarjan as tj
import heapq


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

def output(solution,inst_num,flag):
	print inst_num,flag
	if flag == 1:
		filename = "complete/inst" + str(inst_num)+".out"
		output_func(solution,filename)
	if flag == 2:
		filename = "partial/inst" + str(inst_num)+".out"
		output_func(solution,filename)


def output_func(solutions,filename=""):
	print("hiih")
	f = open("final.out", 'w')
	for sol in solutions:
		for s in sol:
			string = ""
			for num in s:
				string += str(num) + " "
			string = string[:-1]
			string += "; "
			f.write(string)
		f.write("\n")
	f.close()

def output_per(pers,filename=""):
	f = open("per.out", 'w')
	for p in pers:
		f.write(str(p)+"\n")
	f.close()

def cycle_checker(graph, cycle):
	cycle_len = len(cycle)
	for i in range(cycle_len-1):
		if not graph.has_edge(cycle[i],cycle[i+1]):
			print "nooooooooooooooooooooooooooooooooo"
			return False
	if graph.has_edge(cycle[-1],cycle[0]):
		return True
	else:
		return False

def construct_graph_for_tarjan(graph):
	result = {}
	num_of_vertex = 0
	for v in nx.nodes(graph):
		result[v] = nx.all_neighbors(graph,v)
		num_of_vertex += 1
	# print "there are " +str(num_of_vertex) + "vertices"
	return result

def solve_all(x, y):
	# complete = []
	# partial = []
	solutions = []
	pers = []
	for i in range(x,y):
		filename = "phase1-processed/"+str(i)+".in"
		print filename
		g = construct_graph(filename)
		solution,flag, per = instance_solver(g)
		# output_func(solution, "")
		# output_per(per, "")
		# if flag ==1:
		# 	complete.append(i)
		# elif flag == 2:
		# 	partial.append(i)
		# output(solution,i,flag)
		solutions.append(solution)
		pers.append(per)
	return solutions, pers

	# f = open("temp_results","w")
	# f.write("complete:\n")
	# f.write(str(complete)+"\n")
	# f.write("partially done:\n")
	# f.write(str(partial)+"\n")
	# f.close()

def instance_solver(graph):
	original_vertices_no = len(graph.nodes())
	original_edges_no = len(graph.edges())
	final_solution_set = []
	flag = 999
	graph,final_solution_set,largest_scc_size = scc_screening(graph,final_solution_set)
	# children_cycles = find_all_children_cycle(graph)
	# children_cycles = delete_duplicate_cycle(children_cycles)
	# children_cycles,_ = find_unique_cycle(children_cycles,0)
	# print "children_cycles are " 
	# print children_cycles
	# for cycle in children_cycles:
	# 	if cycle:
	# 		solution_set.append(cycle)
	# 		for item in cycle:
	# 			graph.remove_node(item)
	functions = [sort_v_according_to_indegree,sort_v_according_to_outdegree,sort_v_according_to_connectedness]
	solutions = []
	for function in functions:
		solution_set = final_solution_set[:]
		graph_cp = graph.copy()
		cycle = one_cycle_from_most_constricted(graph_cp,function)
		if cycle and cycle_checker(graph_cp,cycle):
			print cycle
			solution_set.append(cycle)
			graph_cp.remove_nodes_from(cycle)
		graph_cp,solution_set,_ = scc_screening(graph_cp,solution_set)

		while cycle:
			cycle = one_cycle_from_most_constricted(graph_cp, function)
			if cycle and cycle_checker(graph_cp,cycle):
				solution_set.append(cycle)
				graph_cp.remove_nodes_from(cycle)
			graph_cp,solution_set,largest_scc_size = scc_screening(graph_cp,solution_set)
		solution = [len(graph_cp.nodes()),solution_set,graph_cp, function]
		solutions.append(tuple(solution))

	v_left = 999999999
	final_sol = None
	for sol in solutions:
		if sol[0]<v_left:
			v_left = sol[0]
			final_sol = sol

	print "out of " +str(original_vertices_no) +" vertices, " + str(len(final_sol[2].nodes()))+" vertices uncovered "
	print "number of edges left " + str(nx.number_of_edges(final_sol[2]))
	print "solution comes from " + str(final_sol[3])
	

	if len(final_sol[2].nodes()) == 0:
		flag = 1
	elif len(final_sol[2].nodes())/float(original_vertices_no) < 0.03:
		flag = 2
	return final_sol[1],flag, "% = " + str(round(len(final_sol[2].nodes())/float(original_vertices_no), 2)) + "; #uncovered = " + str(len(final_sol[2].nodes())) + "; #vertex = " + str(original_vertices_no) + "; #edges = " + str(original_edges_no) + "; from " + str(final_sol[3])



def one_cycle_from_most_constricted(graph,function):
	pq = function(graph)
	cycle = None
	while not cycle:
		try:
			curr_v = pq.pop()
		except:
			break
		cycle = find_one_cycle(graph,curr_v,curr_v,5)

	return cycle

def sort_v_according_to_indegree(graph):
	pq = PriorityQueue()
	for v in graph.nodes():
		in_degree = graph.in_degree(v)
		pq.push(v,-in_degree)
	return pq

def sort_v_according_to_outdegree(graph):
	pq = PriorityQueue()
	for v in graph.nodes():
		out_degree = graph.out_degree(v)
		pq.push(v,-out_degree)
	return pq

def sort_v_according_to_connectedness(graph):
	pq = PriorityQueue()
	for v in graph.nodes():
		degree = graph.degree(v)
		pq.push(v,-degree)
	return pq

def scc_screening(graph,solution_set):
	graph, new_solutions, largest_scc_size = tarjan_algo(graph)
	if new_solutions:
		for new_solution in new_solutions:
			solution_set.append(new_solution)
	# print("#scc " + str(len(graph)))
	return graph, solution_set,largest_scc_size

def tarjan_algo(graph):
	largest_scc_size = 0
	dict = construct_graph_for_tarjan(graph)
	sccs =  tj.tarjan(dict)
	dead_people = []
	solution_set = []
	for scc in sccs:
		if len(scc) == 0:
			continue
		if len(scc) > largest_scc_size:
			largest_scc_size = len(scc)
		if len(scc) == 1:
			dead_people.append(scc[0])
		elif len(scc)<6:
			scc = scc_solution_formatter(graph,scc)
			if scc and cycle_checker(graph,scc):
				solution_set.append(scc)#####order the vertices.
	for person in dead_people:
		graph.remove_node(person)
	for scc in solution_set:
		graph.remove_nodes_from(scc)
	# if solution_set:
		# print "solutions from tarjan screening" + str(solution_set)
	return graph, solution_set, largest_scc_size

def scc_solution_formatter(graph,scc):
	curr_v = scc.pop()	
	return scc_formatter_helper(graph,curr_v,scc,[curr_v],len(scc))

def scc_formatter_helper(graph,start, scc, path,remaining):
	if remaining == 0:
		return path
	for n in graph.neighbors(start):
		if not n in path and n in scc:
			path += [n]
			return scc_formatter_helper(graph,n,scc,path,remaining -1)


def find_one_cycle(graph,source,end,depth, path = []):
	if depth == 0:
		return None
	path = path + [source]
	for v in graph.neighbors(source):
		try:
			assert graph.has_edge(source,v)
		except AssertionError:
			print "oh shiiiiiiiiiiiit"
			print v,source
			break
		if v == end:
			return path
		elif not v in path:
			return find_one_cycle(graph,v,end,depth -1,path)


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

def find_all_cycle(graph):
	vertices = graph.nodes()
	cycles = []
	for vertex in vertices:
		cycle = find_one_cycle(graph,vertex,vertex,5)
		if cycle:
			if cycle_checker(graph, cycle):
				# print cycle
				cycles.append(cycle)
			else:
				print("fuckkkk")
	return cycles

# def find_all_cycle(graph):
#  	graph_gen = nx.simple_cycles(graph)
#  	while (1):
#  		cycle = graph_gen.next()
#  		if len(cycle) <6:
#  			print cycle

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

def naive_greedy(graph):
	solution_set = []
	graph,solution_set,largest_scc_size = scc_screening(graph,solution_set)
	children_cycles = find_all_children_cycle(graph)
	children_cycles = delete_duplicate_cycle(children_cycles)
	children_cycles,_ = find_unique_cycle(children_cycles,0)
	print "children_cycles are " 
	print children_cycles
	for cycle in children_cycles:
		if cycle:
			solution_set.append(cycle)
			for item in cycle:
				graph.remove_node(item)

	cycles = find_all_cycle(graph)
	# unique_cycles, remain_cycles = find_unique_cycle(cycles)
	# for c in unique_cycles:
	# 	donation_chain.append(c)
	# 	G = delete_cycle(G, c)
	# for i,c in enumerate(remain_cycles):
	# 	return

def main():
	solutions, pers = solve_all(1, 250)
	output_func(solutions)
	output_per(pers)

	# g = construct_graph("instances/2.in")
	# instance_solver(g)

	# print nx.number_of_edges(g)
	# g = construct_graph("instances/1.in")
	# print nx.cycle_basis(g)
	# nx.draw(g)
	# naive_greedy(g)
	# solutions =  instance_solver(g)
	# ver = set()
	# for sol in solutions:
	# 	if sol:
	# 		for v in sol:
	# 			ver.add(v)
	# print len(ver)
	# instance_solver(g)
	# new_g, sccs, size = scc_screening(g, [])
	# cycles = find_all_children_cycle(new_g)
	# print(cycles)
	# cycles = delete_duplicate_cycle(cycles)
	# print(cycles)
	# unqiue, remain = find_unique_cycle(cycles, 0)
	# print(unqiue)
	# for i in range(1,492):
	# 	filename = "phase1-processed/"+str(i)+".in"
	# 	print filename
	# 	g = construct_graph(filename)
	# instance_solver(g)


	# g = construct_graph("phase1-processed/17.in")
	# print(cycle_checker(g, [4, 5, 6, 7, 8]))
	# print nx.number_of_edges(g)+nx.number_of_nodes(g)
	# cycles = find_all_cycle(g)
	# # cycles = delete_duplicate_cycle(cycles)
	# for c in cycles:
	# 	print c

		

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]



if __name__ == "__main__":
	main()