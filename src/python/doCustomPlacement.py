# Creates the TCL script that does the custom placement of the cells
# Run this after calling the doWidthCheck.py script and widthChecker.tcl file
from createPinPlacement import createPinPlacement
from customPlacement import customPlacement
from parseModule import parseModule
from readPinInputs import readPinInputs
from widthMeasure import widthMeasure


# Get cellNames and location
module = "regfile.v"
cellNames, location, cellNums, numWLatch = parseModule(module)


# Get number of read ports, data bits, and addresses
pin_read = "../src/apr/pin_config.txt"
numReads, numDataBits, numAddresses = readPinInputs(pin_read)

width_files = "../src/apr/widths.txt"
# Use a tcl script to run widthMeasure to read the widths.txt file created by TCL script
widths = widthMeasure(cellNames, width_files, numWLatch)

# Run customplacement.py with cellNames and locations from createTCLWidth.py and widths from widthMeasure.py
# Get custom placement width and height, used to determine floorplan size
out_file = "../src/apr/customPlacement.tcl"
out_file_floor = "../src/apr/floorplanSizes.tcl"
custom_width, custom_height, maxcoords = customPlacement(out_file, out_file_floor, cellNames, cellNums, location,
                                                         widths, numReads, numDataBits, numAddresses)




print("number of read ports: " + str(numReads))
print("number of data bits: " + str(numDataBits))
print("number of addresses: " + str(numAddresses))

# Create pin_placement.txt file
createPinPlacement(numReads, numDataBits, numAddresses, maxcoords)
