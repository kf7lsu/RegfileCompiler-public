#Matthew Trahms
#EE 526
#5/20/21

#this file generates the AND gates to and together the write decoder output
#with the output of the write enable latch, as well as the clock and of that
#signal and a buffered clock signal

#takes:
#python file interface to generate output verilog
#register file index
#number of entries in the register file
#desired output width

#produces:
#verilog instantiations of an AND gate to generate the individual write signal
#as well as the logical and of that and the clock signal

#intermediate signal is wr_line_(RF#)_(ENTRY#)
#clock signal is wr_clk_(RF#)
#AND name format is and_wen_dec_(RF#)_(ENTRY#)
#clock AND name format is clk_and_(RF#)_(ENTRY#)

from cell_map import and2, clk_and

def connect_w_logic(verilog_out, rf_idx, entries, out_w):
	and_cell = and2
	clk_cell = clk_and
	write_en = 'wr_en_l_' + str(rf_idx)
	and_name_form = 'and_wen_dec' + str(rf_idx) + '_'
	clk_name_form = 'clk_and_' + str(rf_idx) + '_'
	intermed_sig_form = 'wr_line_' + str(rf_idx) + '_'
	input_line = 'we_p_'
	clk_sig = 'wr_clk_' + str(rf_idx)
	for i in range(entries):
		i = str(i) #only need string
		line1 = and_cell + ' ' + and_name_form + i + ' (.A1(' + write_en
		line1 += '), .A2(' + input_line + i + '_' + str(rf_idx)
		line1 += '), .Z(' + intermed_sig_form + i + '));\n'
		line2 = clk_cell + ' ' + clk_name_form + i + ' (.A1(clk'
		line2 += '), .A2(' + intermed_sig_form + i + '), .Z(we_' + i
		line2 += '_' + str(rf_idx) + '));\n'
		verilog_out.write(line1)
		verilog_out.write(line2)
	return

if __name__ =='__main__':
	f = open('w_logic_test.txt', 'w')
	rf = 0
	entries = 4
	w = 1
	connect_w_logic(f, rf, entries, w)
	f.close()
