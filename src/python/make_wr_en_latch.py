#Matthew Trahms
#EE 526
#5/19/21

#this file creates the low enable latch containing the write enable signal
#TODO: add support for multiple vertical stages of register file

#takes:
#python file interface to generate output verilog
#register file index
#number of entries in register file bank
#total number of entries in register file
#desired latch output width

#produces:
#the line of verilog code corresponding to a low enable d latch on the write
#enable line, triggering only if that bank should be written to.
#output line is wr_en_l_(RF#)
#enable signal (clk) is en_wr_en_(RF#)

from cell_map import low_latch, and2, and3, inv
import math

def make_wr_en_latch(verilog_out, rf_idx, rf_bits, tot_bits, rf_entries, tot_entries, latch_w):
	latch_cell = (low_latch % latch_w)
	latch_name = 'latch_wr_en_'+str(rf_idx)
	out_port = 'wr_en_l_' + str(rf_idx)
	
	vertical_banks = tot_entries / rf_entries
	line = latch_cell + ' ' + latch_name + ' (.Q(' + out_port + '), .EN('
	line += 'clk), .D('
	rest_of_line = None
	if vertical_banks == 1:
		rest_of_line = route_wen_single()
	else:
		rest_of_line = route_wen_multi(rf_idx, rf_bits, tot_bits, vertical_banks, tot_entries)
	line += rest_of_line
	verilog_out.write(line)
	return

#these functions will generate the rest of the logic to connect a valid wen
#signal to the write enable latch
def route_wen_single():
	return 'wr_en));\n'

#returns a string that completes the output line with the necessary logic line
#(wr_en_(RF#)) and the necessary AND gate and address inverters. Since the
#number of vertical banks is already limited by muxes, this works using at most
#a 3 input AND gate (wr_en and 2 addr bits)
#inverted signals are wen_addr_inv_(BIT#)_(RF#)
def route_wen_multi(rf_idx, rf_bits, tot_bits, vertical_banks, tot_entries):
	output = 'wr_en_' + str(rf_idx) + '));\n'
	#determine bank index based on horizontal splitting and rf_idx
	rf_per_bank = int(math.floor(tot_bits / rf_bits))
	bank_addr = int(math.floor(rf_idx / rf_per_bank))
	
	addr_bits = int(math.ceil(math.log(tot_entries, 2)))
	if vertical_banks == 2:
		sel_bit = addr_bits - 1 #selection done by most sig bit
		sel_inp = ('wr_addr[%d]' % sel_bit)
		if bank_addr == 0:
			inv_inp = sel_inp
			sel_inp = 'wen_addr_inv_' + str(sel_bit) + '_'
			sel_inp += str(rf_idx)
			#addr inverters have form addr_inv_wen_(BIT#)_(RF#)
			output += inv + ' addr_inv_wen_' + str(sel_bit) + '_'
			output += str(rf_idx) + ' (.I(' + inv_inp + '), .ZN('
			output += sel_inp + '));\n'
		#write enable AND has form wen_and_(RF#)
		output += and2 + ' wen_and_' + str(rf_idx) + ' (.Z(wr_en_'
		output += str(rf_idx) + '), .A1(wr_en), .A2(' + sel_inp + ')'
		output += ');\n'
	elif vertical_banks == 3 or vertical_banks == 4: 
		#v_banks == 3 or 4, throw error otherwise
		#create most significant and least significant bit vars
		msb = addr_bits - 1
		lsb = addr_bits - 2
		ms_sel_inp = ('wr_addr[%d]' % msb)
		ls_sel_inp = ('wr_addr[%d]'% lsb)
		#lsb inversion logic
		if (bank_addr % 2) == 0:
			inv_inp = ls_sel_inp
			ls_sel_inp = 'wen_addr_inv_' + str(lsb) + '_'
			ls_sel_inp += str(rf_idx)
			#addr inverters have form addr_inv_wen_(BIT#)_(RF#)
			output += inv + ' addr_inv_wen_' + str(lsb) + '_'
			output += str(rf_idx) + ' (.I(' + inv_inp + '), .ZN('
			output += ls_sel_inp + '));\n'
		#msb inversion logic
		if bank_addr < 2:
                        inv_inp = ms_sel_inp
                        ms_sel_inp = 'wen_addr_inv_' + str(msb) + '_'
                        ms_sel_inp += str(rf_idx)
                        #addr inverters have form addr_inv_wen_(BIT#)_(RF#)
                        output += inv + ' addr_inv_wen_' + str(msb) + '_'
                        output += str(rf_idx) + ' (.I(' + inv_inp + '), .ZN('
                        output += ms_sel_inp + '));\n'	
		output += and3 + ' wen_and_' + str(rf_idx) + ' (.Z(wr_en_'
		output += str(rf_idx) + '), .A1(wr_en), .A2(' + ms_sel_inp
		output += '), .A3(' + ls_sel_inp + '));\n'
	return output

if __name__ == '__main__':
	f = open('wen_latch_test.txt', 'w')
	rf = 0
	entries = 16
	tot_entries = 64
	bits = 16
	tot_bits = 16
	w = 1
	make_wr_en_latch(f, rf, bits, tot_bits, entries, tot_entries, w)
	f.close()
