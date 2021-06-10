#this code will generate the structural verilog for a single entry in the register file
#takes in the output file manager, the entry number, the number of bits, the number of reads, and the width of the
#tristate buffers on the read outputs

#expects the same things as make_store_cell, ensure code is valid there

#Matthew Trahms
#EE 526
#4/20/21

from make_store_cell import make_store_cell

def make_store_entry(out_file, entry_number, bits, reads, buff_width, regfile_num):
	#just need to create the correct number of bits
	#this and the make_store_array are going to be pretty simple
	for bit in range(bits):
		make_store_cell(out_file, entry_number, bit, reads, buff_width, regfile_num)
	return

if __name__ == '__main__':
	f = open('store_entry_test.txt', 'w')
	rows = 4
	cols = 2
	reads = 2
	for row in range(rows):
		make_store_entry(f, row, cols, reads, 1, 0)
	f.close()
