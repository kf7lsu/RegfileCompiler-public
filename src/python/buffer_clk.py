#Matthew Trahms
#EE 526
#5/20/21

#this file routes the clock signal to each location where the clock needs to be
#through a series of clock buffers. this includes:
#write data latches: wd_en_(RF#)
#write enable latch: en_wr_en_(RF#)
#write line logic: wr_clk_(RF#)
#write addr latches: wr_addr_en_(RF#)

#takes:
#python file interface to write verilog out to
#register file index
#desired buffer width

#produces:
#the verilog for 4 clock buffers leading to each of the locations listed above

from cell_map import clk_buff

def buffer_clk(verilog_out, rf_idx, buff_w):
	buff_cell = clk_buff
	names = ['buff_wd_', 'buff_wen_', 'buff_wr_', 'buff_waddr_']
	outputs = ['wd_en_', 'en_wr_en_', 'wr_clk_', 'wr_addr_en_']
	for i in range(len(names)):
		line = buff_cell + ' ' + names[i] + str(rf_idx) + ' (.I(clk),'
		line += '.Z(' + outputs[i] + str(rf_idx) + '));\n'
		verilog_out.write(line)
	return

if __name__ == '__main__':
	f = open('buff_clk_test.txt', 'w')
	rf = 0
	w = 1
	buffer_clk(f, rf, w)
	f.close()
