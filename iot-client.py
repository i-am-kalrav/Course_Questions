import sys
import socket
import struct
import random

bulbIP = sys.argv[1]
UDPport = int(sys.argv[2])
bulbColor = sys.argv[3]
switch = sys.argv[4]

# switch:
# 0 = OFF
# 1 = ON
# 3 = Status check only

switch = int(switch)
colorLen = len(str(bulbColor))

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pings = 0
msgID = random.randint(1, 100)

form = "!hhii" + str(colorLen) + "s" + "i"
data = struct.pack(form, 1, 0, msgID, colorLen, bulbColor.encode(), switch)

while True:
    print("Sending Request to ", bulbIP, ", ", str(UDPport), ":")
    if pings == 0:
        print("Message ID: ", msgID)
        print("Light Bulb Color Length: ", colorLen)
        print("Bulb Switch: ", switch)

    pings += 1

    try:
        clientsocket.sendto(data, (bulbIP, UDPport))
        clientsocket.settimeout(1)
        dataEcho, address = clientsocket.recvfrom(1040)
        clientsocket.settimeout(None)
        msg_type, respCode, msgID, colLen = struct.unpack("!hhii", dataEcho[:12])
        form1 = "!" + str(colLen) + "s" + "i"
        bulbCol, swtch = struct.unpack(form1, dataEcho[12:])
        color = bulbCol.decode()

        print("\nReceived Response from ", bulbIP, ", ", str(UDPport), ":")
        if respCode == 1:
            print("Return Code: ", respCode, " (Error in request)")
        elif respCode == 0:
            print("Return Code: ", respCode, " (No errors in the request)")
        print("Message ID: ", msgID)
        print("Light Bulb Color: ", color)
        print("Bulb Switch: ", swtch)
        break

    except socket.timeout:
        if pings <= 3:
            print("Request timed out...\n")
        elif pings == 4:
            print("Request timed out... Exiting Program")
            break
clientsocket.close()
