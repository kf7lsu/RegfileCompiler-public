#to generate a custom register file, just modify the parameters below
#ENTRIES: the number of lines in the register file
#BITS: The number of bits per line in the register file
#READS: The number of read ports on the register file
#H_BANKS: used to split the register file along the word axis,
#         allows for large entries without exploding read/write cap
#         NOTE: changing this will create a register file with a number of
#         bits per line equal to greater than the specified number of bits
#         and a multiple of the number of H_BANKS in order to balace the splits
#V_BANKS: used to split the address space among multiple register files to
#         allow for a large number of entries without exploding the bitline cap
#         NOTE: This does not guarantee the specified number of entries.
#         The number of entries will be the closest greater power of 2 multiple
#         of V_BANKS

ENTRIES=16
BITS=16
READS=2
H_BANKS=1
V_BANKS=1

regfile:
	-python make_toplevel.py $(ENTRIES) $(BITS) $(READS) $(H_BANKS) $(V_BANKS)
	-icc_shell -shared_license -gui -f apr.tcl

clean:
	-rm -r regfile_lib
	-rm -r reports
	-rm -r results
	-rm command.log
	-rm icc_output.txt
	-rm regfile.v
	-rm may_need_for_rotated_vias.lef
	-rm -r pna_output
	-rm net.acts
	-rm -r legalizer_debug_plots
