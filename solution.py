import networkx as nx
import matplotlib.pyplot as plt


def construct_graph():
	f = open("small_instance.in")
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
	# G.draw()
	return G

def find_all_cycle(graph):
	graph_gen = nx.simple_cycles(graph)
	cycles = []
	while (1):
		try:
			cycle = graph_gen.next()
		except:
			break
		if len(cycle) <6:
			cycles.append(cycle)
			# print cycle
	print(len(cycles))
	return cycles

def find_unique_cycle(cycles):
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
			if list(set(cycles[i]) & set(cycles[j])):
				unique[i] = False
				unique[j] = False
		if unique[i]:
			unique_cycles.append(cycles[i])
		else:
			remain_cycles.append(cycles[i])
	# print unique_cycles
	# print remain_cycles
	return unique_cycles, remain_cycles

def delete_cycle(G, cycles):
	G.remove_nodes_from(cycles)
	return G

def naive_greedy(G):
	donation_chain = []
	cycles = find_all_cycle(G)
	unique_cycles, remain_cycles = find_unique_cycle(cycles)
	for c in unique_cycles:
		donation_chain.append(c)
		G = delete_cycle(G, c)
	for i,c in enumerate(remain_cycles):
		

def main():
	g = construct_graph()
	naive_greedy(g)


if __name__ == "__main__":
	main()