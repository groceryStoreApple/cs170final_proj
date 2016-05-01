f = open("final1.out", 'r')
out = []
for line in f:
	if len(line) == 0:
		print(line)
		out = out + "\n" + "None"
		break
	else:
		print(line[0])
		print(line)
		# out = out + "\n" + str(line[:-2])
out = out[1:]
f.close()
fnew = open("final10.out", "w")
fnew.write(f)
fnew.close()
