#this function generates a single storage cell for a storage grid
#takes in the output file, entry number, bit position, number of reads, tristate
#buffer width, and the index of which regfile is being created (relevant in the
#case of composing a larger regfile of smaller regfiles)

#(all indices below are zero indexed)
#Expecting: write enable wires of form we_(ENTRY#)_(REGFILE#) (ex. we_1_0)
#latch output wires of the form lo_(ENTRY#)_(BIT#)_(RF#) (ex. lo_3_5_0)
#latch input wires of the form li_(BIT#)_(RF#) (ex. li_4_0)
#buffer output wires of the form bo_(BIT#)_(READ#)_(RF#) (ex bo_3_2_0_0)
#read enable wires of the form re_(ENTRY#)_(READ#)_(RF#) (ex re_3_0_0)

#Matthew Trahms
#EE 526
#4/20/21

from cell_map import high_latch, tristate_buff

def make_store_cell(out_file, entry, bit, num_read, buff_w, regfile_num):
	#don't need entry #, but # as ints. Do need them as strings
	entry = str(entry)
	bit = str(bit)
	regfile = str(regfile_num)
	
	#determining which cells to use
	latch_name = high_latch
	buff_name = (tristate_buff % buff_w)

	#generating code for the high enable latch
	#latches named with the form dlatch_(RF#)_(ENTRY#)_(BIT#)
	latch_line = latch_name + ' ' + 'dlatch_' + regfile + '_'  + entry + '_' + bit + ' ('
	latch_line += '.D(li_' + bit + '_' + regfile + '), '
	latch_line += '.E(we_'+ entry + '_' + regfile + '), '
	latch_line += '.Q(lo_' + entry + '_' + bit + '_' + regfile + '));\n'
	out_file.write(latch_line)

	#generating code for each read tristate buffer
	#tristate buffers named with format tri_(RF#)_(ENTRY#)_(BIT#)_(READ#)
	for read in range(num_read):
		#don't need read as an int, need it as a string
		read = str(read)
		buff_line = buff_name + ' ' + 'tri_' + regfile + '_'  + entry + '_' + bit + '_' + read + ' ('
		buff_line += '.I(lo_' + entry + '_' + bit + '_' + regfile + '), '
		buff_line += '.OE(re_' + entry + '_' + read + '_' + regfile + '), '
		buff_line += '.Z(bo_' + bit + '_' + read + '_' + regfile +  '));\n'
		out_file.write(buff_line)
	return

if __name__ == "__main__":
	f = open('store_cell_test.txt', 'w')
	rows = 4
	cols = 2
	reads = 2
	for row in range(rows):
		for col  in range(cols):
			make_store_cell(f, row, col, reads, 1, 0)
	f.close()
