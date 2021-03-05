import socket
import sys
args = sys.argv
serverIp = args[1]
serverPort = int(args[2])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while (True):
	webAdress = input()
	s.sendto(bytes(str(webAdress), "utf-8"), (str(serverIp),  int(serverPort))) # send to server.
	data, addr = s.recvfrom(1024)
	print(str(data).split(",")[1]) # print website ip.
s.close()
 