#Matthew Trahms
#EE 526
#5/17/21

#this file generates a decoder for reading or writing to specific addresses
#in a register file.
#NOTE: To use this to generate a write decoder, put -1 for the read number

#takes the output verilog interface, the index of the register file, the number
#of entries in the register file, the desired width of the output inverter,
#and the desired width of the input inverters
import math

from cell_map import inv, and2, and3, buff

def make_decoder(verilog_out, rf_idx, num_entries, read_idx, out_w, in_w):
	addr_bits = int(math.ceil(math.log(num_entries, 2)))
	make_addr_inp_invs(verilog_out, rf_idx, read_idx, in_w, addr_bits)
	for i in range(num_entries):
		make_and_tree(verilog_out, addr_bits, num_entries, out_w, i, read_idx, rf_idx)

#helper function to build input inverters
#takes read address ports directly, translates to rd_a_(READ#)_(RF#)_(ADDR BIT#)
#and rd_a_b_(READ#)_(RF#)_(ADDR BIT#) for noninverting and inverting 
#(or wr_a(_b)_(RF#)_(ADDR BIT#) in the case of write addresses)
#takes in the output of the wr_addr latches in the form wr_addr_l_(RF#)_(ADDR
#BIT#)
def make_addr_inp_invs(verilog_out, rf_idx, read_idx, in_w, addr_bits):
	addr_in = None
	addr_inv = None
	addr_buf = None
	inv1 = None
	inv2 = None
	if read_idx == -1:
		addr_in = 'wr_addr_l_' + str(rf_idx) + '_'
		addr_inv = 'wr_a_b_' + str(rf_idx) + '_'
		addr_buf = 'wr_a_' + str(rf_idx) + '_'
		#inverter names of form inv_wr_a_(RF#)_(ADDR BIT#) and
		#inv_wr_a_b_(RF#)_(ADDR BIT#)
		inv1 = 'inv_wr_a_' + str(rf_idx) + '_'
		inv2 = 'inv_wr_a_b_' + str(rf_idx) +'_'
	else:
		addr_in = 'rd_addr_' + str(read_idx) +'['
		addr_inv = 'rd_a_b_' + str(read_idx) + '_' + str(rf_idx) + '_'
		addr_buf = 'rd_a_' + str(read_idx) + '_' + str(rf_idx) + '_'
		#inverter names of the form:
		#inv_rd_a_(READ#)_(RF#)_(ADDR BIT#) and
		#inv_rd_a_b_(READ#)_(RF#)_(ADDR_BIT#)
		inv1 = 'inv_rd_a_' + str(read_idx) + '_' + str(rf_idx) + '_'
		inv2 = 'inv_rd_a_b_' + str(read_idx) + '_' + str(rf_idx) + '_'
	for bit in range(addr_bits):
		bit = str(bit) #only actually need the string
		first_inv = inv1 + bit
		second_inv = inv2 + bit
		first_addr = addr_in + bit
		if not (read_idx == -1):
			first_addr += ']'
		second_addr = addr_inv + bit
		third_addr = addr_buf + bit
		line1 = inv + ' ' + first_inv + ' (.I(' + first_addr + '), .ZN('
		line1 += second_addr + '));\n'
		line2 = inv + ' ' + second_inv + ' (.I(' + second_addr + '), .ZN('
		line2 += third_addr + '));\n'
		verilog_out.write(line1)
		verilog_out.write(line2)

#helper function to generate a tree of 2 input AND gates
#NOTE: since the ICC is optimizing the logic, it's okay that this is an
#inefficient decoder structure. If future improvement is made to the decoder
#structure, then this portion will need to be reimplemented to use an actual
#architecture
#internal signals will have the following naming format:
#dec_(RF#)_(wr/rd#)_(ENTRY#)_(DEPTH)_(DEPTH IDX)
#where DEPTH is the distance into the tree starting at 0 after the first AND
#and DEPTH IDX is the index at that level of depth
def make_and_tree(verilog_out, addr_bits, num_entries, out_w, entry_idx, read_idx, rf_idx):
	std_and_gate = and2
	extra_and_gate = and3
	weird_case_cell = buff
	read_identifier = 'rd' + str(read_idx)
	if read_idx == -1:
		read_identifier = 'wr'
	name_templ = 'dec_an_' + str(rf_idx) + '_' + read_identifier + '_'
	name_templ += str(entry_idx) + '_'
	#names will have the format of
	#dec_an_(RF#)_(wr/rd#)_(ENTRY#)_(AND DEPTH)_(AND DEPTH IDX)
	bit_idx_arr = range(addr_bits)
	bit_idx_arr.reverse()
	running_idx = entry_idx
	bit_status = list()
	for bit in bit_idx_arr:
		bit_mag = 2**bit
		check_fit = running_idx - bit_mag
		if check_fit >= 0:
			running_idx = check_fit
			bit_status.append(1)
		else:
			bit_status.append(0)
	bit_status.reverse()
	
	#determining the output line, if it's a read port then it goes straight
	#to the read line as described in make_store_cell.py
	#if it's a write port, then it goes to an intermediate net to feed into
	#a 3 input and with the clock and latched wen signal.
	#defining that term as we_p_(ENTRY#)_(REGFILE#)
	output_line = 're_' + str(entry_idx) + '_' + str(read_idx) + '_'
	output_line += str(rf_idx)
	if read_idx == -1:
		output_line = 'we_p_' + str(entry_idx) + '_' + str(rf_idx)
	
	#time to do level 0 and gates, if there's an extra bit, there will
	#be a 3 input and gate to make sure it's included
	num_and_out = int(math.floor(addr_bits/2))
	num_inp_remaining = addr_bits
	pos_inp_form = 'rd_a_' + str(read_idx) + '_' + str(rf_idx) + '_'
	neg_inp_form = 'rd_a_b_' + str(read_idx) + '_' + str(rf_idx) + '_'
	if read_idx == -1:
		pos_inp_form = 'wr_a_' + str(rf_idx) + '_'
		neg_inp_form = 'wr_a_b_' + str(rf_idx) + '_'
	inp_list = [neg_inp_form, pos_inp_form]
	intermed_sig_form = 'dec_' + str(rf_idx) + '_' + read_identifier
	intermed_sig_form += '_' + str(entry_idx) + '_'
	for i in range(num_and_out):
		intermed_sig = intermed_sig_form + '0_' + str(i)
		first_bit = i * 2
		second_bit = first_bit + 1
		third_bit = first_bit + 2
		if num_inp_remaining > 3 or num_inp_remaining == 2:
			#normal case where inputs go to 2 inp and gate
			num_inp_remaining -= 2
			line = std_and_gate + ' ' + name_templ + '0_' + str(i)
			line += ' (.A1(' + inp_list[bit_status[first_bit]]
			line += str(first_bit) + '), .A2('
			line += inp_list[bit_status[second_bit]] 
			line += str(second_bit) + '), .Z('
			if num_and_out == 1:
				line += output_line + '));\n'
			else:
				line += intermed_sig + '));\n'
			verilog_out.write(line)
		elif num_inp_remaining == 3:
			#case where there's an extra remaining input, wrap into
			#3 input and gate
			num_inp_remaining -= 3
			line = extra_and_gate + ' ' + name_templ + '0_' + str(i)
			line += ' (.A1(' + inp_list[bit_status[first_bit]]
			line += str(first_bit) + '), .A2('
			line += inp_list[bit_status[second_bit]]
			line += str(second_bit) + '), .A3('
			line += inp_list[bit_status[third_bit]] + str(third_bit)
			line += '), .Z('
			if num_and_out == 1:
				line += output_line + '));\n'
			else:
				line += intermed_sig + '));\n'
			verilog_out.write(line)
		else:
			#really odd case, only for 1-2 entry reg file, buffer
			#input directly to output line
			num_inp_remaining -= 1
			line = weird_case_cell + ' ' + name_templ + '0_0 (.I('
			line += inp_list[bit_status[first_bit]] + str(first_bit)
			line += '), .Z(' + output_line + '));\n'
			verilog_out.write(line)
	num_inp = num_and_out
	num_and_out = int(math.floor(num_and_out / 2))
	layer = 1
	while num_and_out > 0:
		num_inp_remaining = num_inp
		loc_intermed_sigs = intermed_sig_form + str(layer) + '_'
		prev_sigs = intermed_sig_form + str(layer-1) + '_'
		for i in range(num_and_out):
			intermed_sig = loc_intermed_sigs + str(i)
			first_bit = i * 2
			second_bit = i + 1
			third_bit = i + 2
			first_sig = prev_sigs + str(first_bit)
			second_sig = prev_sigs + str(second_bit)
			third_sig = prev_sigs + str(third_bit)
			if num_inp_remaining > 3 or num_inp_remaining == 2:
				#standard case, 2 input and gate
				num_inp_remaining -= 2
				line = std_and_gate + ' ' + name_templ
				line += str(layer) + '_' + str(i) + ' (.A1('
				line += first_sig + '), .A2(' + second_sig
				line += '), .Z('
				if num_and_out == 1:
					line += output_line + '));\n'
				else:
					line += intermed_sig + '));\n'
				verilog_out.write(line)
			else:
				#case where exactly 3 inputs remaining
				#already taken care of case where only 1 inp
				num_inp_remaining -= 3
				line = extra_and_gate + ' ' + name_templ
				line += str(layer) + '_' + str(i) + ' (.A1('
				line += first_sig + '), .A2(' + second_sig
				line += '), .A3(' + third_sig + '), .Z('
				if num_and_out == 1:
					line += output_line + '));\n'
				else:
					line += intermed_sig + '));\n'
				verilog_out.write(line)
		num_inp = num_and_out
		num_and_out = int(math.floor(num_and_out / 2))
		layer += 1
	return

if __name__ == '__main__':
	f = open('decoder_test.txt', 'w')
	rf = 0
	entries = 8
	read = 1
	in_w = 2
	out_w = 8
	make_decoder(f, rf, entries, read, out_w, in_w)
