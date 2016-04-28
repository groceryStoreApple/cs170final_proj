
import numpy as np
def main():
	rand_inst_generator("small_instance.in")

def rand_inst_generator(filename):
	string = ""
	n = np.random.randint(10,15)
	string += str(n) + "\n"
	string += child_random(n)
	for i in range(n):
		string += rand_matrix_line(n,i)
	write_to_file(string, filename)

def child_random(n):
	s = []
	for i in range(np.random.randint(0,n)):
		s.append(np.random.randint(0,n))
	s = set(s)
	string = ""
	for item in s:
		string += str(item) + " "
	return string[:-1] + "\n"

def rand_matrix_line(n,line_num):
	string = ""
	for i in range(n):
		if i == line_num:
			string += "0 "
		else:
			if np.random.randint(0,100) < 30:
				string += "0 "
			else:
				string += "1 "

	return string[:-1] + "\n"

def write_to_file(string, filename):
	output_file = open(filename,"w")
	output_file.write(string)
	output_file.close()

if __name__ == "__main__":
	main()