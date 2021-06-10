#Matthew Trahms
#EE 526
#4/30/21
#this module generates the module declaration line for the register file
#inputs: clk, wr_en, wr_addr, wr_data, rd_addr_(READ#)
#outputs: rd_data_(READ#)
#NOTE: READ# is 0 indexed

def make_module_decl(verilog_out, reads):
	out_line = "module regfile ( clk, wr_en, wr_addr, wr_data"
	for read in range(reads):
		read = str(read)
		out_line += ", rd_addr_" + read + ', '
		out_line += "rd_data_" + read
	out_line += " );\n"
	verilog_out.write(out_line)
	return

if __name__ == '__main__':
	f = open('module_decl_test.txt', 'w')
	make_module_decl(f, 3)
	f.write('test\n') #ensure that line ends properly
	f.close()
