#this function generates the low enable latches used to hold the data to be
#written to the main grid of latches. This function may be called multiple times
#in the case of multiple, smaller regfiles used to compose larger regfiles

#takes the verilog file interface to write the latches,
#the number of bits to determine how many latches to create,
#the numbered witdh of the standard cell to use,
#and the index of the regfile that the latches are being generated for

#wr data outputs are named same as data latch inputs as est in make_store_cell
#wr data inputs are named to the following format: wd_(RF#)_(BIT#)
#wr data latch enable is the following format: wd_en_(RF#)

#Matthew Trahms
#EE 526
#5/4/21

from cell_map import low_latch

def make_wr_data_latches(verilog_out, bits, latch_w, regfile_num):
	latch_cell = (low_latch % latch_w)
	regfile_num = str(regfile_num) #don't actually need as int
	for bit in range(bits):
		bit = str(bit) #don't need it as an int
		#wr_dat latches named to the following format:
		#wr_dat_latch_(RF#)_(BIT#)
		latch_line = latch_cell + ' wr_dat_latch_' + regfile_num + '_' + bit + ' ('
		latch_line += '.D(wd_'+regfile_num+'_'+bit+'), '
		latch_line += '.EN(clk), '
		latch_line += '.Q(li_'+bit+'_'+regfile_num+'));\n'
		verilog_out.write(latch_line)
	return

if __name__ == '__main__':
	f = open('wdata_latch_test.txt', 'w')
	bits = 4
	latch_w = 2
	rf_num = 0
	make_wr_data_latches(f, bits, latch_w, rf_num)
	f.close()
