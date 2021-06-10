#this file generates a series of buffers connecting the write data input port
#to the write data ports of any sub-regfiles. Each set of write data latches
#connected to each grid is designed to be self contained. This is done so that,
#if desired, larger regfiles can be composed of several smaller regfiles.

#this function takes in the verilog output file to write, the number of
#regfiles, the number of bits used for wr_data input, and the number of bits
#in each entry of the smaller regfile unit, as well as the width of the buffers.

#the toplevel write data port is expected to be a multiple of the number of bits
#that can be written to the smaller regfiles so that the regfiles can be aligned
#properly. Regfiles are placed in the ordering as shown below, total number of
#regfiles must result in a rectangle structure.
#	|-------|-------|
#	|	|	|
#	|  1st  |  2nd  |
#	|	|	|
#	|-------|-------|
#	|	|	|
#	|  3rd  |  4th  |
#	|	|	|
#	|-------|-------|

from cell_map import buff

def make_wr_data_buffers(verilog_out, num_rf, wr_data_bits, rf_bits, buff_w):
	rf_per_row = int(wr_data_bits / rf_bits)
	rf_rows = int(num_rf / rf_per_row)
	
	port_idx = 0
	for col in range(rf_per_row):
		for rf_bit in range(rf_bits):
			for row in range(rf_rows):
				rf_idx = col + (row * rf_per_row)
				rf_idx = str(rf_idx)
				bit = str(rf_bit)
				#name buffers to the following form:
				#wd_b_(RF#)_(RF_BIT#)
				line = buff + ' wd_b_' + rf_idx + '_' + bit
				line += ' (.I(wr_data['+str(port_idx)+']), '
				line += '.Z(wd_'+rf_idx+'_'+bit+'));\n'
				verilog_out.write(line)
			port_idx += 1

if __name__ == '__main__':
	f = open('wdata_buff_test.txt', 'w')
	num_rf = 4
	wr_data_bits = 8
	rf_bits = 4
	buff_w = 1
	make_wr_data_buffers(f, num_rf, wr_data_bits, rf_bits, buff_w)
	f.close
