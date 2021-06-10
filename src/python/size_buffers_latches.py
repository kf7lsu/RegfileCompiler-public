#Matthew Trahms
#EE 526
#6/8/21

#This file contains the process node specifics for sizing buffers and latches
#based on the number of entries in the register file. Each of these functions
#should be adjusted to the process node in order to maximize efficiency.
#The functions should return the integer sizing of the latches based on the
#size tuples defined in cell_map.py

#this code uses a lookup table structure to allow for nonlinear approximation
#depending on the specifics of the process node

from cell_map import tristate_w, low_widths

#for this example, sizing will increase as a factor of entries / 8
def size_tristate(entries):
	width_idx = -1	#default to last idx
	if entries < 8:
		width_idx = 0
	elif entries < 16:
		width_idx = 1
	elif entries < 24:
		width_idx = 2
	elif entries < 32:
		width_idx = 3
	elif entries < 40:
		width_idx = 4
	elif entries < 48:
		width_idx = 5
	elif entries < 56:
		width_idx = 6
	elif entries < 64:
		width_idx = 7
	elif entries < 72:
		width_idx = 8
	elif entries < 80:
		width_idx = 9
	return tristate_w[width_idx]

#again, for this example, sizing by multiples of 8
def size_wr_data_latch(entries):
        width_idx = -1  #default to last idx
        if entries < 8:
                width_idx = 0
        elif entries < 16:
                width_idx = 1
        return low_widths[width_idx]
