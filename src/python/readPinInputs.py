# Reads the file containing number of read ports, data bits, and addresses


def readPinInputs(pin_read):
    f = open(pin_read, 'r')

    currentLine = f.readline()
    # Get number of data bits
    numDataBits = int(currentLine.split()[1])

    currentLine = f.readline()
    # Get number of addresses
    numAddresses = int(currentLine.split()[1])

    currentLine = f.readline()
    # Get number of read ports
    numReadPorts = int(currentLine.split()[1])

    f.close()

    return numReadPorts, numDataBits, numAddresses
