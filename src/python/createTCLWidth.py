# Creates the TCL file to read the widths of cells from
# Also will get and return the cellNames and locations to be used later
# When calling this method , need to create variable which store the cellNames and locations
# as inputs into customPlacement.py

# Inputs:
# file: string file to write TCL script to
# module: module to parse cell names from
from parseModule import parseModule


def createTCLWidth(out_file, module):
    # variable to write to
    tclLines = ""
    # Get list of cellNames and their locations
    cellNames, location, cellNums, numWLatch = parseModule(module)

    # Create TCL File
    tclLines = "set fp [open " + "\"../src/apr/widths.txt\"" + " w+]\n"
    total = len(cellNames) * len(cellNames[0])
    # print("size is " + str(total))
    count = 0
    repeat = 1

    

    blockSize = len(cellNames[0])

    while repeat == 1:
        leave = 0
        while leave == 0:
            # Break out of for loops when hit write data latches
            # print("cell name " + str(cellNames[count]) + " " + str(len(cellNames[count])))
            if len(cellNames[count]) != blockSize:
                leave = 1
            if leave == 0:
                # Iterate through length of block
                for y in range(len(cellNames[0])):
                    variable = cellNames[count][y]
                    tclLines += "set " + variable + " \"" + variable + "\"\n"
                    tclLines += "set " + variable + "_WIDTH [get_attribute $" + variable + " width]\n"
                    tclLines += "puts $fp $" + variable + "_WIDTH\n"
                count += 1

        # print(len(cellNames))
        # print(count)

        # for x in range(count, len(cellNames)):
        leave2 = 0
        while leave2 == 0:
            variable = cellNames[count]
            # print(variable)
            tclLines += "set " + variable + " \"" + variable + "\"\n"
            tclLines += "set " + variable + "_WIDTH [get_attribute $" + variable + " width]\n"
            tclLines += "puts $fp $" + variable + "_WIDTH\n"
            count += 1
            if count == len(cellNames):
                # Check to see if finished writing all custom placement
                repeat = 0
                leave2 = 1
            elif cellNames[count][0][0] == "d":
                # Check to see if moving onto next register bank
                leave2 = 1


    tclLines += "close $fp"

    out_file.write(tclLines)

    # return cellNames, location


if __name__ == '__main__':
    out_file = "widthChecker.tcl"
    module = "regfile.v"
    file = open(out_file, 'w')
    createTCLWidth(file, module)
