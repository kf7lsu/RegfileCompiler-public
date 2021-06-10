#Matthew Trahms
#EE 526
#5/10/21

#this file controls the routing of rdata bitlines to the pins. If there is only
#1 row of register files, then those rdata outputs are fed straight to the
#pins through buffers. If there are multiple rows, then the rows are muxed using
#the higher order read address pins. NOTE: at the current time, there can be a
#maximum of 4 rows of register files, due to the limited number of standard cell
#muxes. This could potentially be expanded in the future with cascaded muxes.

#The toplevel function checks if there are multiple rows of register files
#from there, it calls one of two helper functions for the case that there is
#either one row, or 2-4 rows of register files.

#make_wr_data.py goes over the order of layout for register files
#make_store_cell.py goes over the wire naming conventions
#make_module_decl.py goes over the port naming conventions

#requires: number of reads, number of address bits, number of bits per read,
#	   number of bits in each regfile row, total number of regfiles,
#	   and the width of the output driver
#produces: the necessary verilog to map the internal signals of rdata to the
#	   rdata pins

from cell_map import buff, mux2, mux3, mux4

def route_rdata(verilog_out, num_reads, num_addr_bits, read_bits, regfile_bits, num_regfiles, output_width):
	regfiles_per_row = int(read_bits / regfile_bits)
	num_rows = int(num_regfiles / regfiles_per_row)
	if num_rows == 1:
		route_rdata_single(verilog_out, num_reads, read_bits, regfile_bits, num_regfiles, output_width)
	elif num_rows >= 2 and num_rows <= 4:
		route_rdata_2_4(verilog_out, num_reads, read_bits, regfile_bits, num_regfiles, output_width, num_addr_bits)
	else:
		route_rdata_5_up()

def route_rdata_single(verilog_out, num_reads, read_bits, regfile_bits, num_regfiles, output_width):
	std_cell = buff
	port_idx = 0
	for rf in range(num_regfiles):
		rf = str(rf)
		for bit in range(regfile_bits):
			bit = str(bit)
			for read in range(num_reads):
			#buffer name format:
			#rd_buff_(READ#)_(OUTPUT BIT #)
				read = str(read)
				cell_name = ' rd_buff_' + read + '_' + str(port_idx)
				out_line = std_cell + ' ' + cell_name + ' (.I(bo_'
				out_line += bit + '_' + read + '_' + rf + '), '
				out_line += '.Z(rd_data_' + read + '['
				out_line += str(port_idx) + ']));\n'
				verilog_out.write(out_line)
			port_idx += 1

def route_rdata_2_4(verilog_out, num_reads, read_bits, regfile_bits, num_regfiles, output_width, num_addr_bits):
	regfiles_per_row = int(read_bits / regfile_bits)
	num_rows = int(num_regfiles / regfiles_per_row)
	std_cell = None
	if num_rows == 2:
		std_cell = mux2
	elif num_rows == 3:
		std_cell = mux3
	else:
		std_cell = mux4
	port_idx = 0
	for rf in range(regfiles_per_row):
		for bit in range(regfile_bits):
			bit = str(bit)
			idx = str(port_idx)
			for read in range(num_reads):
				read = str(read)
				#mux name format:
				#rd_mux_(READ#)_(OUTPUT BIT #)
				line = std_cell + ' rd_mux_' + read + '_'
				line += idx + ' (.Z(rd_data_' + read + '['
				line += idx + ']), '
				for row in range(num_rows):
					line += '.I' + str(row) + '(bo_' + bit
					line += '_' + read
					rf_idx = rf + (row * regfiles_per_row)
					line += '_' + str(rf_idx) + '), '
				if num_rows == 2:
					line += '.S(rd_addr_' + read + '['
					line += str(num_addr_bits-1) + ']));\n'
				else:
					line += '.S0(rd_addr_' + read + '['
					line += str(num_addr_bits-2) + ']), '
					line += '.S1(rd_addr_' + read + '['
					line += str(num_addr_bits-1) + ']));\n'
				verilog_out.write(line)
			port_idx += 1

def route_rdata_5_up():
	raise Exception("5+ rows of register files not supported")

if __name__ == "__main__":
	f = open('route_rdata_test.txt', 'w')
	route_rdata(f, 2, 8, 4, 4, 1, 1)
	f.write('\n')
	route_rdata(f, 2, 8, 4, 4, 2, 1)
	f.write('\n')
	route_rdata(f, 2, 8, 4, 4, 3, 1)
	f.write('\n')
	route_rdata(f, 2, 8, 4, 4, 4, 1)
	f.close()
