#This file contains a series of functions to generate the necessary
#wires to drive the storage grid. The standards for the wires are laid out
#in make_store_cell

#takes in the output file manager, the number of entries, the number of bits
#and the number of reads

#Matthew Trahms
#EE 526
#4/20/21

def make_store_grid_wires(out_file, entries, bits, reads, num_regfiles):
	#make write enables
	make_wires(out_file, 'we', (entries, num_regfiles))
	#make latch output wires
	make_wires(out_file, 'lo', (entries, bits, num_regfiles))
	#make latch input wires
	make_wires(out_file, 'li', (bits, num_regfiles))
	#make buffer output wires
	make_wires(out_file, 'bo', (bits, reads, num_regfiles))
	#make read enables
	make_wires(out_file, 're', (entries, reads, num_regfiles))
	return


#generic function to generate a set of string wire names based on a prefix
#and tuple of dimensions, returns a list of strings
#dimensions are in an n-entry tuple treated as an n-dim rectangle
#DO NOT HAVE A VALUE OF 0 FOR ONE OF THE DIMS
def make_wire_names(prefix, dims):
	prog = [prefix]
	for dim in dims:
		lastprog = prog
		prog = list()
		for wirename in lastprog:
			for index in range(dim):
				new_wire = wirename + '_' + str(index)
				prog.append(new_wire)
	return prog

#translates from a list of wire names to a string corresponding to the correct
#syntax for wire declarations
def make_wire_line(wire_names):
	output = "wire " + wire_names[0]
	wire_names = wire_names[1:]
	for name in wire_names:
		output += ', '
		output += name
	output += ';\n'
	return output

#creates a set of wires based on a prefix and a set of dimensions
#writes the correct syntax of wires to the output file
def make_wires(output_file, prefix, dims):
	names = make_wire_names(prefix, dims)
	line = make_wire_line(names)
	output_file.write(line)

if __name__ == "__main__":
	f = open('make_wire_names_test.txt', 'w')
	names = make_wire_names('test', (3,2,1,2))
	print(len(names) == (3*2*1*2))
	f.write(make_wire_line(names))
	f.close()
