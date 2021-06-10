# Does custom cell placement given the list of cells, locations, and widths
# Inputs:
# out_file: file writing to
# cellNames: cells placing, from createTCLWidth.py
# location: location of where to place cells from cellNames, from createTCLWidth.py
# widths: widths of the cells being used, from widthMeasure.py
# Return:
# returns the width and height of the grid of placed cells, to be used to help determine floorplan size


from createTCLWidth import createTCLWidth
from parseModule import parseModule
from widthMeasure import widthMeasure


def customPlacement(out_file, out_file_floor, cellNames, cellNums, location, cellWidths, numReads, numDataBits, numAddresses):
    
    file = open(out_file, 'w')

    size = len(cellNames)

    # Get max number of columns in register file
    test = location[0][0]
    maxColumns = 0
    loop = 1
    count = 0
    while loop == 1:
        if test != location[count][0]:
            maxColumns = location[count - 1][1] + 1
            loop = 0
        count += 1
    gridfixx = 20 - .2
    gridfixy = 20 - .2

    width = 0
    height = 0
    flip = 0
    x = 0

    totalblockwidth = 0
    blocksize = len(cellNames[0])
    maxheightcoord = 0
    maxwidthcoord = 0
    oneRegWidth = 0
    repeat = 1
    # for x in range(size):
    print("len(cellNames) " + str(len(cellNames)))
    while repeat == 1:
        print("one register file width " + str(oneRegWidth))
        leave = 0
        # Writing placement for data storage grid
        while leave == 0:
            # print("len(cellNames[x]) " + str(len(cellNames[x])))
            # print("cellNames[x] " + str(cellNames[x]))
            if len(cellNames[x]) != blocksize:
                leave = 1
                print("Leaving")
            if leave == 0:
                locationx = location[x][0]
                locationy = location[x][1]
                regnum = location[x][2]
                offset = 0
                count = 0

                # Sum up total width of all cells in a block
                widthSum = 0
                for t in range(len(cellNames[0])):
                    # print("t " + str(t))
                    # print("widthSum type=" + str(type(widthSum)) + " value=" + str(widthSum))
                    # print("cellWidths[x][t] type=" + str(type(cellWidths[x][t])) + " value=" + str(cellWidths[x][t]))
                    widthSum += cellWidths[x][t]
                    # print(len(cellNames[0]))
                    # print(len(cellWidths))

                    # print("cellWidths[x][t] " + str(cellWidths[x][t]))
                totalblockwidth = widthSum
                # Loop through all cells in a block, latch and tri-state buffers, write data latches
                for y in range(len(cellNames[0])):
                    # currentCell = cell
                    currentCell = cellNames[x][y]
                    # print("currentCell " + str(currentCell))

                    # Determine block size here
                    standCellHeight = 1

                    
                    currentWidth = cellWidths[x][y]
                    

                    # Origin x takes offset from last cell, size of the block(by summing up all the cell widths) times a little,
                    # register number times a little, grid offset
                    if regnum == 0:
                        originx = offset + (locationx * widthSum * 1.1) + gridfixx
                    else:
                        originx = (regnum * oneRegWidth) + (offset + (locationx * widthSum * 1.1) + gridfixx)



                    # Origin y is fixed since standard cell height is the same for all cells, include grid offset
                    originy = locationy * standCellHeight + gridfixy

                    # How much to offset each cell in a block, based on width of cells times a little
                    # offset += standCellHeight * 1.5
                    offset += currentWidth * 1.1

                    # check the max x and y coordinates of placing cells
                    if originx - gridfixx > width:
                        width = originx - gridfixx
                        maxwidthcoord = originx
                        # Get the sie of the first register width
                        # Used in placement with multiple register banks
                        if regnum == 0:
                            oneRegWidth = width + cellWidths[0][0]
                    if originy - gridfixy > height:
                        height = originy - gridfixy
                        maxheightcoord = originy




                    # Do custom placement for the cell
                    # Store name of variable
                    variable = str(currentCell)

                    # First name is name of variable , second name is name of cell being placed
                    placement = "set " + variable + " \"" + str(currentCell) + "\"\n"

                    # Get height and width of cell
                    placement += "set " + variable + "_HEIGHT [get_attribute $" + variable + " height]\n"
                    placement += "set " + variable + "_WIDTH [get_attribute $" + variable + " width]\n"

                    # Set origin
                    placement += "set " + variable + "_LLX [expr + " + str(originx) + "]\n"
                    placement += "set " + variable + "_LLY [expr + " + str(originy) + "]\n"

                    

                    # Derive URX and URY corner for placement blockage.
                    placement += "set " + variable + "_URX [expr $" + variable + "_LLX + $" + variable + "_HEIGHT]\n"
                    placement += "set " + variable + "_URY [expr $" + variable + "_LLY + $" + variable + "_WIDTH]\n"

                    # Set guard spacing around cell, no filler cells can be placed in this guard
                    # Attmept to shrink guard cell spacing from 2*cellheight to 1*cellheight
                    placement += "set GUARD_SPACING [expr 1*$CELL_HEIGHT]\n"

                    # Set orientation of the cell
                    # Need to flip cells vertically every other cell
                    if flip == 0:
                        placement += "set_attribute $" + variable + " orientation \"N\"\n"
                        flip = 1
                    else:
                        placement += "set_attribute $" + variable + " orientation \"S\"\n"
                        flip = 0

                    # Set the cell location, place the cell
                    placement += "set_cell_location -coordinates [list [expr $" + variable + "_LLX ] [expr $" + variable \
                                 + "_LLY]] -fixed $" + variable + "\n"
                    

                    # Create blockage for filler cell placement
                    placement += "create_placement_blockage -bbox [list [expr $" + variable + "_LLX - $GUARD_SPACING] [expr $" \
                                 + variable + "_LLY - $GUARD_SPACING] [expr $" + variable + "_URX + $GUARD_SPACING] [expr $" \
                                 + variable + "_URY + $GUARD_SPACING]] -type hard\n"

                    # At end, write to file
                    file.write(placement)
                x += 1

        # Creating placement for write data latches
        leave2 = 0
        # track = 0
        while leave2 == 0:
            locationx = location[x][0]
            locationy = location[x][1]
            regnum = location[x][2]
            offset = 0
            count = 0

            # Total width of all cells in a block
            # widthSum = cellWidths[z] * len(cellNames[0])
            widthSum = totalblockwidth
            # Loop through all cells in a block, latch and tri-state buffers, write data latches
            # currentCell = cell
            currentCell = cellNames[x]

            # Determine block size here
            standCellHeight = 1

            # Need to compare current cell width and next cell width, take larger one, also don't do if no next cell
            currentWidth = cellWidths[x]

            # Origin x takes offset from last cell, size of the block(by summing up all the cell widths) times a little,
            # register number times a little, grid offset
            originx = offset + (locationx * widthSum * 1.1) + (regnum * maxColumns * 1.5) + gridfixx

            # Origin y is fixed since standard cell height is the same for all cells, include grid offset
            originy = locationy * standCellHeight + gridfixy

            

            # How much to offset each cell in a block, based on width of cells times a little
            offset += currentWidth * 1.1

            # check the width and height of the custom placed cells
            # check the max x and y coordinates of placing cells
            if originx - gridfixx > width:
                width = originx - gridfixx
                maxwidthcoord = originx
            if originy - gridfixy > height:
                height = originy - gridfixy
                maxheightcoord = originy

            # Do custom placement for the cell
            # Store name of variable
            variable = str(currentCell)

            # First name is name of variable , second name is name of cell being placed
            placement = "set " + variable + " \"" + str(currentCell) + "\"\n"

            # Get height and width of cell
            placement += "set " + variable + "_HEIGHT [get_attribute $" + variable + " height]\n"
            placement += "set " + variable + "_WIDTH [get_attribute $" + variable + " width]\n"

            # Set origin
            placement += "set " + variable + "_LLX [expr + " + str(originx) + "]\n"
            placement += "set " + variable + "_LLY [expr + " + str(originy) + "]\n"

            # startx -= gapx

            # Derive URX and URY corner for placement blockage.
            placement += "set " + variable + "_URX [expr $" + variable + "_LLX + $" + variable + "_HEIGHT]\n"
            placement += "set " + variable + "_URY [expr $" + variable + "_LLY + $" + variable + "_WIDTH]\n"

            

            # Set orientation of the cell
            # Need to flip cells vertically every other cell
            if flip == 0:
                placement += "set_attribute $" + variable + " orientation \"N\"\n"
                flip = 1
            else:
                placement += "set_attribute $" + variable + " orientation \"S\"\n"
                flip = 0

            # Set the cell location, place the cell
            # Test removing "-fixed" to be able to do optimization
            placement += "set_cell_location -coordinates [list [expr $" + variable + "_LLX ] [expr $" + variable \
                         + "_LLY]] -fixed $" + variable + "\n"
            

    

            # At end, write to file
            file.write(placement)
            x += 1

            # print("x value is " + str(x))
            # print("cellNames[x][0][0] is " + str(cellNames[x][0][0]))

            # Check to leave loop and to see if finish reading all register banks
            if x == len(cellNames) - 1:
                # Check to see if finished writing all custom placement
                repeat = 0
                leave2 = 1
                print("Finished writing custom placement tcl")
            elif cellNames[x][0][0] == "d":
                # Check to see if moving onto next register bank
                leave2 = 1
                print("Changing to next register bank")


            

    # Set floorplan width and height
    file2 = open(out_file_floor, 'w')

                

    numRows = location[len(location) - 1][1] + 1
    

    
    # floor_height being exactly number of rows plus some needed extra buffer plus 2 clock rows
    floor_height = numRows + 2 + 2
    

   # Add to the columns width based on extra number of cells not customed placed
    num_other_columns = (cellNums / (floor_height / 1.8))
                    
    # Standard cell height
    standCellHeight = 1
    # Avg cell width
    avgcellwidth = 1
    
    if (numReads > 1 and numDataBits < 32) or (numDataBits > 63): # For testbench set, always occuring except tb4 
        num_other_columns -= (width / avgcellwidth) / (floor_height / standCellHeight)
    # Need to address problem when too tall and not wide enough(entries > bits), smaller ratio needs more 
    #if numAddresses > numDataBits:
    #    num_other_columns *= 1.3 + ((1 / (numAddresses / numDataBits)))
    #    num_other_columns *= 1.3 # Test with just same number for all
    
    
    if (numAddresses > numDataBits) or (numDataBits > 32 and numAddresses > 32): # Or limit it slightly, tb1 ignore
        if numReads > 2:
            num_other_columns *= 1.5 + ((numReads - 2) * .2) # Causes lots of filler, needed for metal route space
        else:
            num_other_columns *= 1.5

    # If register too large, need to increase width and height to accomodate for metal routing
    if numAddresses > 48 and numDataBits > 48 and numReads > 2:
        num_other_columns *= 1.3
        floor_height += int(numReads * 2)
        


    
    # Calculate the size of the width to add
    num_other_columns *= (1 / standCellHeight)  # MAYBE ADD TO DIVIDE BY 1.1, Just a tad too big
    # print("width divided by height " + str(width / height))
    
    num_other_columns = int(num_other_columns)
    

    # Width is based on standard cell CELL_HEIGHT and width of custom cell, times a little more
    # floor_width = width / 1.8 * 1.05
    # divide by 1.8 because floorplan.tcl multiplies by that number
    floor_width = (width / standCellHeight) + num_other_columns
    print("floor_width " + str(floor_width))
    # print("num_other_columns " + str(num_other_columns))

    print("Number of Data Bits " + str(numDataBits)) 
    print("regnum " + str(regnum))
    
    floorplan = "set CORE_WIDTH_IN_CELL_HEIGHTS " + str(floor_width) + "\n"
    floorplan += "set CORE_HEIGHT_IN_CELL_HEIGHTS " + str(floor_height) + "\n"
    file2.write(floorplan)

    file.close()
    file2.close()
    return width, height, [maxheightcoord, maxwidthcoord]


if __name__ == '__main__':
    # Order of things run
    # Be in the IC Compilier
    # Use a tcl script to run createTCLWidth.py
    out_file = "widthChecker.tcl"
    module = "moduleTest.v"
    file = open(out_file, 'w')
    cellNames, location = createTCLWidth(file, module)
    # print("location " + str(location))
    # print(len(location))
    # print(cellNames)
    # print(len(cellNames))
    # print(len(cellNames[0]))

    # SEPARATE THE CODE INTO TWO PYTHON SCRIPTS AND IN THE MIDDLE RUN THE TCL FILE
    # In this break, run the TCL file, widthChecker.tcl, in apr.tcl

    # Run the parseModule Python Script to get the cellNames and locations
    cellNames, location = parseModule(module)

    width_files = "widths.txt"
    # Use a tcl script to run widthMeasure to read the widths.txt file created by TCL script
    widths = widthMeasure(cellNames, width_files)
    # Run customplacement.py with cellNames and locations from createTCLWidth.py and widths from widthMeasure.py
    out_file = "customPlacement.tcl"
    custom_width, custom_height, maxHeight = customPlacement(out_file, cellNames, location, widths)
