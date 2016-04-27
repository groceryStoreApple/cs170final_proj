import networkx as nx
import matplotlib.pyplot as plt


def construct_graph():
	f = open("test_instance")
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




def main():
	g = construct_graph()

if __name__ == "__main__":
	main()