import sys
import socket
import struct

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  ", serverPort, "\n")

# The light by default turns ON with a white color when you first switch it ON without a specified color
# And by default, the bulb is switched OFF

colorlst = ['White']
swtchlst = [0]
while True:
    swtchRT = 0
    data, address = serverSocket.recvfrom(1040)

    error = 1

    msg_type, rspCode, msgID, colorLen = struct.unpack("!hhii", data[:12])
    form = "!" + str(colorLen) + "s" + "i"
    bulbColor, switch = struct.unpack(form, data[12:])
    color = bulbColor.decode()

    if switch == 1 or switch == 2:
        swtchlst.append(switch)
        swtchRT = switch
    elif switch == 3:
        swtchRT = swtchlst[-1]


    if switch in range(1, 4):
        error = 0
        if color != "None" and color != "none":
            colorlst.append(color)

    form1 = "!hhii" + str(len(colorlst[-1])) + "s" + "i"
    data = struct.pack(form1, 2, error, msgID, len(colorlst[-1]), colorlst[-1].encode(), swtchRT)

    if switch != -1:
        serverSocket.sendto(data, address)