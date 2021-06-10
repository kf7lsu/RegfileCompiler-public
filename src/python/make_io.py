#Matthew Trahms
#EE 526
#4/30/21
#This file is used to generate the io ports of the register file
#it takes in the verilog file, the number of reads, the number of bits
#per entry, and the number of entries. It returns the correct syntax verilog
#to produce the io ports for the clock (clk), write enable (wr_en), 
#write data (wr_data), write address (wr_addr), the read data ports 
#(rd_data_(READ#)), and the read address (rd_addr_(READ#)) ports.

import math

def make_io(verilog_out, reads, bits, entries):
	line = make_io_line('input', 1, ['clk', 'wr_en'])
	verilog_out.write(line)
	line = make_io_line('input', bits, ['wr_data'])
	verilog_out.write(line)
	read_data_ports = list()
	address_ports = ['wr_addr']
	for read in range(reads):
		data = 'rd_data_'+str(read)
		addr = 'rd_addr_'+str(read)
		read_data_ports.append(data)
		address_ports.append(addr)
	line = make_io_line('output', bits, read_data_ports)
	verilog_out.write(line)
	addr_bits = int(math.ceil(math.log(entries, 2)))
	line = make_io_line('input', addr_bits, address_ports)
	verilog_out.write(line)

def make_io_line(io_type, io_bw, io_names):
	io_line = io_type + ' '
	if io_bw > 1:
		io_line += '[' + str(io_bw - 1) + ':0] '
	io_line += io_names[0]
	io_names.pop(0)
	for name in io_names:
		io_line += ', ' + name
	io_line += ';\n'
	return io_line

if __name__ == '__main__':
	f = open('io_test.txt', 'w')
	make_io(f, 2, 64, 16)
	f.write('test') #ensure line ends correctly
	f.close()
