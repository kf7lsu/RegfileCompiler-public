#this code will generate the structural verilog for the main storage grid of a register file
#takes the output file manager, the number of entries, the number of bits,
#the number of reads, and the width of the tristate buffers on the output

#expects the same things as make_store_cell, ensure code is valid there

#Matthew Trahms
#EE 526
#4/20/21

from make_store_entry import make_store_entry

def make_store_grid(out_file, entries, bits, reads, buff_width, regfile_num):
	#just need to create the correct number of entries using make_store_entry
	for entry in range(entries):
		make_store_entry(out_file, entry, bits, reads, buff_width, regfile_num)
	return

if __name__ == '__main__':
	f = open('store_grid_test.txt', 'w')
	rows = 4
	cols = 2
	reads = 2
	make_store_grid(f, rows, cols, reads, 1, 0)
	f.close()
