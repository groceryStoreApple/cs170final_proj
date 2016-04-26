import networkx as nx
import matplotlib.pyplot as plt


def construct_graph():
	f = open("test.in")
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

def find_all_cycle(graph):
	graph_gen = nx.simple_cycles(graph)
	while (1):
		cycle = graph_gen.next()
		if len(cycle) <6:
			print cycle

def find_unique_cycle(cycles):
	unique_cycles = []
	unique = [True] * len(cycles)
	for i in range(0, len(cycles)):
		if not unique[i]:
			continue
		for j in range(i+1, len(cycles)):
			if list(set(cycles[i]) & set(cycles[j])):
				unique[i] = False
				unique[j] = False
		if unique[i]:
			unique_cycles.append(cycles[i])
	print unique_cycles
	return unique_cycles


def main():
	# g = construct_graph()
	# find_all_cycle(g)
	
	find_unique_cycle(cycles)


if __name__ == "__main__":
	main()