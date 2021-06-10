#Matthew Trahms
#EE 526
#5/25/21

#This file serves as the toplevel generation script. The user will enter
#at least the number entries, bits, and reads, with options to specify
#that the regfile should be split into banks. Vertical banks (v_banks) means
#that the address space will be split between multiple banks. This comes in
#handy when creating a register file with a large number of entries.
#Horizontal banks (h_banks) means that the data being read/written is split
#across multiple register files. This comes in handy when creating a register
#file with lots of bits per entry in the register file.

from make_store_grid import make_store_grid as grid
from make_module_decl import make_module_decl as module
from make_io import make_io as io
from make_wr_data_latches import make_wr_data_latches as wr_latches
from make_wr_data_buffers import make_wr_data_buffers as wr_buff
from route_rdata import route_rdata as rdata
from make_decoder import make_decoder as decoder
from make_wr_addr_latches import make_wr_addr_latches as waddr_latch
from make_wr_en_latch import make_wr_en_latch as wen_latch
from connect_w_logic import connect_w_logic as w_logic
from buffer_clk import buffer_clk
from cell_map import low_widths, tristate_w
from size_buffers_latches import size_tristate, size_wr_data_latch
import math
import argparse

def make_toplevel(out_file, pins_file, entries, bits, reads, v_banks, h_banks):
	if v_banks > 4:
		print("WARNING: Only 4 vertical banks supported at this time")
		print("setting vertical banks to 4")
		v_banks = 4
	
	#figuring out the actual entries and bits based on regfile division
        #entries_per_regfile = int(math.ceil(entries/v_banks))
        #entries = int(entries_per_regfile * v_banks)
	entries_per_regfile = entries
	if v_banks > 1:
		approx_rf_entries = entries / v_banks
		rf_addr_bits = int(math.ceil(math.log(approx_rf_entries, 2)))
		entries_per_regfile = int(2**rf_addr_bits)
		entries = entries_per_regfile * v_banks
        bits_per_regfile = int(math.ceil(bits/h_banks))
        bits = int(bits_per_regfile * h_banks)

	#write the module header and io
        module(out_file, reads)
        io(out_file, reads, bits, entries)
        out_file.write('\n')

	#calculate the number of address bits
	addr_bits = int(math.ceil(math.log(entries, 2)))

	#calculate the number of regfiles to generate
	num_rf = v_banks * h_banks

	#calculate static cell widths
	tri_w = size_tristate(entries_per_regfile)
	wlatch_w = size_wr_data_latch(entries_per_regfile)
	
	#grabbing lowest latch width for unoptimized logic
	lowest_latch_w = low_widths[0]
	
	#start doing custom placement
	out_file.write('// START_CUSTOM_PLACE\n')
	for rf_idx in range(num_rf):
		grid(out_file, entries_per_regfile, bits_per_regfile, reads, tri_w, rf_idx)
		wr_latches(out_file, bits_per_regfile, wlatch_w, rf_idx)
	out_file.write('// END_CUSTOM_PLACE\n')
	
	#decoders, write logic, and signal routing
	wr_buff(out_file, num_rf, bits, bits_per_regfile, 1)
	rdata(out_file, reads, addr_bits, bits, bits_per_regfile, num_rf, 1)
	for rf_idx in range(num_rf):
		waddr_latch(out_file, rf_idx, entries_per_regfile, lowest_latch_w)
		wen_latch(out_file, rf_idx, bits_per_regfile, bits, entries_per_regfile, entries, lowest_latch_w)
		w_logic(out_file, rf_idx, entries_per_regfile, 1)
		#buffer_clk(out_file, rf_idx, 1)
		decoder(out_file, rf_idx, entries_per_regfile, -1, 1, 1)
		for i in range(reads):
			decoder(out_file, rf_idx, entries_per_regfile, i, 1, 1)
	out_file.write("endmodule")

	#creating pin information file for apr
	pins_file.write('bits: ' + str(bits) + '\n')
	pins_file.write('entries: ' + str(entries) + '\n')
	pins_file.write('reads: ' + str(reads))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('entries', 
	   help='the number of entries found in the finished register file',
	   type=int)
	parser.add_argument('bits', 
	   help='the number of bits per entry in the register file',
	   type=int)
	parser.add_argument('reads', 
	   help='the number of read ports in the register file', type=int)
	parser.add_argument('word_banks',
	   help='splits the word among multiple banks to lower cap (default 1)',
	   type=int)
	parser.add_argument('address_banks', 
	   help='splits addr space among banks to lower cap (default 1)',
	   type=int)
	args = parser.parse_args()

	out_file = open('regfile.v', 'w')
	pins_file = open('../src/apr/pin_config.txt', 'w')
	entries = args.entries
	bits = args.bits
	reads = args.reads
	h_banks = args.word_banks
	v_banks = args.address_banks
	make_toplevel(out_file, pins_file, entries, bits, reads, v_banks, h_banks)
	out_file.close()
	pins_file.close()
