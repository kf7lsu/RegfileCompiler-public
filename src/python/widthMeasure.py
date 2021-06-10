# Inputs:
# file: File to read widths from
# cellNames: list of cell names, used to know how to order the widths list in same order
# returns:
# widths: widths list of widths of the cells, same order as cellNames
# When calling this method , store output as return value so can be input in customPlacement
from createTCLWidth import createTCLWidth

# Reads the widths of the cells from the txt file
from parseModule import parseModule


def widthMeasure(cellNames, width_files, numWLatch):
    widths = []
    file = open(width_files, 'r')
    currentLine = float(file.readline())
    #for x in range(len(cellNames)):
    x = 0

    repeat = 1
    blocksize = len(cellNames[0])
    while repeat == 1:
        leave = 0
        while leave == 0:
            if len(cellNames[x]) != blocksize:
                leave = 1
            if leave == 0:
                currentWidthB = []
                for y in range(len(cellNames[0])):
                    currentWidthB.append(currentLine)
                    #print(currentLine)
                    currentLine = file.readline()
                    if currentLine != '':
                        currentLine = float(currentLine)
                widths.append(currentWidthB)
                x += 1

        
        for z in range(numWLatch):
            widths.append(currentLine)
            
            currentLine = file.readline()
            x += 1
            if currentLine != '':
                currentLine = float(currentLine)
            else:
                repeat = 0
                

    file.close()
    return widths


if __name__ == '__main__':
    out_file = "widthChecker.tcl"
    module = "moduleTest.v"
    file = open(out_file, 'w')
    createTCLWidth(file, module)

    cellNames, locations = parseModule(module)

    width_files = "widths.txt"
    widths = widthMeasure(cellNames, width_files)
    # print(widths)
    # print(len(widths))
    # print(len(cellNames))


