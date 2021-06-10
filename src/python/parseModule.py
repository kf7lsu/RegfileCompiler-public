
# Parse the verilog module passed in to save only the name of the cell
# Lump cells of the same block together
def parseModule(module):
    # 2d array saving names of the cells, each [] is a block with all the latches/tri-state buffers in a block
    cellNames = []
    # Keep track of number of rows and columns in the placement
    location = []
    # Keep track of number of cells in write data latch
    numWLatch = 0

    # Read the module passed in until first line where cells are defined
    file1 = open(module, 'r')
    currentLine = ""
    while True:
        currentLine = file1.readline()
        # print(currentLine)
        # Read until the line is // START_CUSTOM_PLACE, so next line is lines of cells
        if currentLine == "// START_CUSTOM_PLACE\n":
            currentLine = file1.readline()
            break

    rowMax = 0
    repeat = 1

    # Start parsing out the cells, break out of while loop forcebly since unknown cells in module
    # Start with parsing out the data storage grid


    while repeat == 1:
        complete1 = 0
        while complete1 == 0:
            # Track name of current cell
            currentCell = currentLine.split()[1]

            # Get row and column number from current cell
            rows = int(currentCell.split("_")[2])
            # print(currentCell.split("_")[2])
            columns = int(currentCell.split("_")[3])
            regnum = int(currentCell.split("_")[1])
            # location.append([rows, columns, regnum])
            location.append([columns, rows, regnum])

            if rows > rowMax:
                rowMax = rows

            checkCurrentBlock = 0
            # Keep track of all cells in current block, append to cellNames at end
            currentBlock = []
            while checkCurrentBlock == 0:
                # Track name of current cell
                currentCell = currentLine.split()[1]

                # Add current cell to 2d list of all cells
                currentBlock.append(currentCell)

                # Incremeant to next line in module
                currentLine = file1.readline()
                
                # If next line is write data, then its done with latch/buffer parsing
                if str(currentLine.split()[1].split("_")[0]) == "write_data":
                    complete1 = 1
                    checkCurrentBlock = 1
                # If current line is latch, leave loop
                if str(currentLine.split()[0][0]) == "latch":
                    checkCurrentBlock = 1
            # Add all the cells in same block to list of cells
            cellNames.append(currentBlock)

        rowMax += 1

        # Now parse the write data latches
        complete2 = 0
        numWLatch = 0
        while complete2 == 0:
            # Track name of current cell
            currentCell = currentLine.split()[1]
            #print("current line in write data latch is " + str(currentLine))

            # Get row and column number from current cell
            # Row set since write data latches all on same row
            rows = int(rowMax)
            columns = int(currentCell.split("_")[4])
            regnum = int(currentCell.split("_")[3])
            # location.append([rows, columns, regnum])
            location.append([columns, rows, regnum])

            # Track name of current cell
            currentCell = currentLine.split()[1]

            # Add to cell names list
            cellNames.append(currentCell)

            # Incremeant to next line in module
            currentLine = file1.readline()
            #print("currentLine split at [0] " + str(currentLine.split()[0]))
            numWLatch += 1
            # If next line is next register bank
            if str(currentLine.split()[1][0]) == "register_bank":
                complete2 = 1
                #print("Changing complete2 to 1")
            # If next line is end of custom placement
            elif str(currentLine.split()[0]) == "//":
                complete2 = 1
                repeat = 0

    # Count number of cells not in custom cells, help with floorplan
    cellNums = 0
    while currentLine != "endmodule":
        cellNums += 1
        currentLine = file1.readline()

    print("parse modules cellNames " + str(cellNames))
    print("number of data latches " + str(numWLatch))

    return cellNames, location, cellNums, numWLatch


if __name__ == '__main__':
    module = "regfile.v"
    cellNames, location = parseModule(module)
    print(cellNames)
