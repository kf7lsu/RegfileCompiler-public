#Matthew Trahms
#EE 526
#5/19/21

#This function generates the low enable latches to store the write data address
#this file is called multiple times in the case of multiple regfiles

#syntax for the post latch address bits is defined in make_decoder.py
#clock signal expected is wr_addr_en_(RF#)

#takes:
#the python file interface to write the verilog output
#the index of the register file
#the number of entries
#the desired latch output width

#produces the line by line modules for all the latches

import math

from cell_map import low_latch

def make_wr_addr_latches(verilog_out, rf_idx, num_entries, latch_w):
	latch_cell = (low_latch % latch_w)
	addr_bits = int(math.ceil(math.log(num_entries, 2)))
	#latch name template: latch_waddr_(RF#)_(ADDR BIT#)
	name_templ = 'latch_waddr_'+str(rf_idx)+'_'
	for i in range(addr_bits):
		line = latch_cell + ' ' + name_templ + str(i) + ' (.D(wr_addr['
		line += str(i) + ']), .EN(clk), .Q('
		line += 'wr_addr_l_' + str(rf_idx) + '_' + str(i) + '));\n'
		verilog_out.write(line)
	return

if __name__ == '__main__':
	f = open('wr_addr_latch_test.txt','w')
	rf = 0
	entries = 12
	w = 1
	make_wr_addr_latches(f, rf, entries, w)
	f.close()
