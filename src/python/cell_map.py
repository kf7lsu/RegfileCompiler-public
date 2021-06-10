#this file contains all of the formatting necessary for all of the standard
#cells used in this project. In cases where custom width is specified by the
#user, a tuple of relative sizes is also expected to be found

#Matthew Trahms
#EE 526
#6/2/21

#high enable D latch, only need the lowest width one since this drives
#relatively few gates in close proximity
high_latch = 'DLATCH1'

#tristate buffers used to read the output, need all available widths
tristate_buff = 'TRISTATE%d'
tristate_w = (0, 1, 2)

#clock buffers to connect clock signal to relevant pins, only need lowest width
#ICC optimizes this to higher widths
clk_buff = 'CLK0'

#2 input AND gate for decoders and stuff, tool will optimize this, so only need
#lowest width
and2 = 'AND2W0'

#2 input AND used for clock signals, if nonexistent in process node, use same as
#above, only need lowest width to allow tool to optimize
clk_and = 'CLKAND2W0'

#inverter, only need lowest width, allowing ICC to optimize upward
inv = 'INV0'

#3 input AND gate, possibly used in decoder, only need lowest width
and3 = 'AND3W0'

#buffer cell used in signal routing, only need the lowest width to allow ICC
#to optimize
buff = 'BUFFER0'

#low enable D latch used in the write logic areas. Need the widths for custom
#placement of the write data row of cells.
low_latch = 'LOWD%d'
low_widths = (1, 2, 4)

#2, 3, and 4 input muxes used for reading from multiple banks. NOTE: if your
#standard cell library does not have 2, 3, or 4 input noninverting muxes
#for use, then you can not have that number of vertical banks.
mux2 = 'MUX2W0'
mux3 = 'MUX3W0'
mux4 = 'MUX4W0'
