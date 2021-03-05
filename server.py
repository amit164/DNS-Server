import socket
import sys
import time

args = sys.argv
fileName = args[len(args) - 1]
parentIp = args[2]
parentPort = int(args[3])
f = open(fileName, "r+")  # open file for write and read.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(args[1])))

while True:
    # file update.
    f.close()
    f = open(fileName, "r+")
    flag = False
    data, addr = s.recvfrom(1024)  # recive a message.
    lines = f.readlines()  # list of all lines in file.
    for line in lines:
        listLine = line.split(",")  # split every line by ',' for TTL.
        if len(listLine) == 4:  # check if its a non-static website address.
            if (time.time() - float(listLine[3])) > float(listLine[2]):  # checks TTL.
                lines.remove(line)
        if listLine[0] == str(data.decode("utf-8")):  # find website address.
            s.sendto(bytes(line, "utf-8"), addr)
            flag = True
    if not flag and parentIp != "-1":  # the address is not in the file - call for parent.
        s.sendto(data, (parentIp, int(parentPort)))
        pdata, paddr = s.recvfrom(1024)
        lines.append((pdata.decode("utf-8").rstrip()) + "," + str(time.time()))
        s.sendto(pdata, addr)
    new_file = open(fileName, "w")
    # file update.
    count = 0
    for line in lines:
        line = line.rstrip()
        line = line.lstrip()
        if count != len(lines) - 1:
            line = line + "\n"
        new_file.write(line)
    new_file.close()
