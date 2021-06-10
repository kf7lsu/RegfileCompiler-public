# Python script to create the pin_placement.txt file for where the physically go
import math

def createPinPlacement(numReads, numDataBits, numAddresses, maxcoords):
    pinFile = "pin_placement.txt"

    numAddressBits = int(math.ceil(math.log(numAddresses, 2)))
    # print(numAddressBits)

    # Keep track of pin and number of bits it is, separate into location on grid
    pinsE = {}
    pinsN = {}
    pinsS = {}

    # Set read data bits and address ports
    for x in range(numReads):
        rd_data = "rd_data_" + str(x)
        pinsS[rd_data] = numDataBits
        rd_addr = "rd_addr_" + str(x)
        pinsE[rd_addr] = numAddressBits
    # Set clk and write enable
    pinsN['clk'] = 1
    pinsE['wr_en'] = 1
    # Set write address and data
    pinsE['wr_addr'] = numAddressBits
    pinsN['wr_data'] = numDataBits

    # Measure size of floorplan, approximate and at least encompasses custom placement parts
    # 10.8 is width of power ring around grid, times two since on both sides
    totalheight = maxcoords[0] + (2 * 10.8)
    totalwidth = maxcoords[1] + (2 * 10.8)

    divideN = 0
    divideE = 0
    divideS = 0
    for key in pinsN:
        divideN += pinsN[key]
    for key in pinsE:
        divideE += pinsE[key]
    for key in pinsS:
        divideS += pinsS[key]

    # Shrink just a little so no conflicts at corners
    northSpace = (totalwidth / divideN) / 1.1
    eastSpace = (totalheight / divideE) / 1.1
    southSpace = (totalwidth / divideS) / 1.1

    # Place pins
    pinLine = "type = offset\n"
    pinLine += "defaultOffset = 300.0\n"
    pinLine += "\n"
    # Place North Pins
    pinLine += "#N, 0\n"
    pinLine += "wr_data[0:{0}], layer=M4, pitch={1} +{2}\n".format(str(pinsN["wr_data"]), str(northSpace),
                                                                   str(northSpace/2))
    pinLine += "clk, layer=M4 +{0}\n".format(str(northSpace))
    # Place South Pins
    pinLine += "#S, 0\n"
    for x in range(numReads):
        pinLine += "rd_data_{0}[0:{1}], layer=M4, pitch={2} +{3}\n".format(str(x), str(pinsS["rd_data_0"]),
                                                                           str(southSpace), str(southSpace))
    # Place East Pins
    pinLine += "#E, 0\n"
    pinLine += "wr_en, layer=M4 +{0}\n".format(str(eastSpace))
    pinLine += "wr_addr[0:{0}], layer=M4, pitch={1} +{2}\n".format(str(numAddressBits-1), str(eastSpace), str(eastSpace/2))
    for x in range(numReads):
        pinLine += "rd_addr_{0}[0:{1}], layer=M4, pitch={2} +{3}\n".format(str(x), str(numAddressBits-1),
                                                                           str(eastSpace), str(eastSpace/2))

    # print(pinLine)

    file = open("../src/apr/pin_placement.txt", 'w')
    file.write(pinLine)
    file.close()

if __name__ == '__main__':
    numReads = 2
    numDataBits = 16
    numAddresses = 16
    maxcoords = [48, 164]
    createPinPlacement(numReads, numDataBits, numAddresses, maxcoords)
