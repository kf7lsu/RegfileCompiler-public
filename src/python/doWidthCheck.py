# Creates the TCL script that is used in ICC to measure the widths of the cells
from createTCLWidth import createTCLWidth

out_file = "../src/apr/widthChecker.tcl"
module = "regfile.v"
file = open(out_file, 'w')
createTCLWidth(file, module)
file.close()
