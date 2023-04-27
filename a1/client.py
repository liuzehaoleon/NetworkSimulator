__author__      = "Zehao Liu", "Zhenggan Luo"
__copyright__   = "Copyright 2022, CP372"

# Import socket module
from socket import *
from struct import *
import time
import sys  # In order to terminate the program


def check_server_response(response):
    data_len, pcode, entity = struct.unpack_from('!IHH', response)
    if pcode==555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return
    
# serverName = 'localhost'
#serverName = '10.84.88.53'
serverName = '34.69.60.253'
# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)

data = 'Hello World!!!'
while len(data) % 4 != 0: # make data|4
    data += ' '
data_length = len(data)
pcode = 0
entity = 1
data = data.encode()

sentence = pack('!IHH16s', data_length, pcode, entity, data)

# clientSocket.connect((serverName, serverPort))
clientSocket.sendto(sentence, (serverName, serverPort))

receivesentence, serverAddress = clientSocket.recvfrom(2048)

serverFormat = '!IHHIIHH'
data_length, pcode, entity, repeat, udp_port, length, codea = unpack(
    serverFormat, receivesentence)

# print
print("------------ Starting Stage A  ------------")
print("Received packet from server: data_len: {}  pcode: {}  entity: {}  repeat: {}  len: {}  udp_port: {}  codeA: {}".format(
    data_length, pcode, entity, repeat, length, udp_port, codea))
print("------------ End of Stage A  ------------\n")

# change port
serverPort = udp_port

# phase b-1
while length % 4 != 0:
    length += 1
data = bytearray(length)
data_length_Client = length + 4

print("------------ Starting Stage B  ------------")
clientSocket.settimeout(0.5)

acked_packet_id_list=[]
for i in range(repeat):
    sentence = ""
    pcode = codea
    entity = 1
    packet_id = i
    sentence = pack('!IHHI', data_length_Client, pcode, entity, packet_id)
    sentence += data
    clientSocket.sendto(sentence, (serverName, serverPort))

    
    while True:
        try:
            receivesentence, serverAddress = clientSocket.recvfrom(2048)
            break
        except timeout:
            clientSocket. sendto(sentence, (serverName, serverPort))
            pass

    # receivesentence, serverAddress = clientSocket.recvfrom(2048)
    data_length_Server, pcode, entity, acked_packet_id = unpack('!IHHI', receivesentence)

    if acked_packet_id not in acked_packet_id_list:
        print("Received acknowledgement packet from server: data_len:  {} pcode:  {} entity:  {} acknumber:  {}".format(
        data_length_Server, pcode, entity, acked_packet_id))
        acked_packet_id_list.append(acked_packet_id)
clientSocket.settimeout(None)

receivesentence, serverAddress = clientSocket.recvfrom(2048)
data_length, pcode, entity, tcp_port, codeb = unpack('!IHHII', receivesentence)
print("Received final packet: data_len:  {} pcode:  {} entity:  {} tcp_port: {}  codeB: {}".format(
    data_length, pcode, entity, tcp_port, codeb))
print("------------ End of Stage B  ------------\n")
clientSocket.close()

# TCP - phase c
serverPort = tcp_port

# Bind tcp socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# connect
time.sleep(1)
clientSocket.connect((serverName, serverPort))

# print
print("------------ Starting Stage C  ------------")
print("connecting to server at tcp port {}".format(serverPort))

# receive
receivesentence = clientSocket.recv(1024)
data_length, pcode, entity, repeat2, len2, codec = unpack(
    '!IHHIII', receivesentence[:20])
char = receivesentence[20:].decode()
print("Received packet from server: data_len: {}  pcode: {}   entity: {}   repeat2: {}   len2: {}   codeC: {}   char:  {}".format(
      data_length, pcode, entity, repeat2, len2, codec, char))
print("------------ End of Stage C  ------------\n")

# phase d
print("------------ Starting Stage D  ------------")
i = 0
data = ""
for i in range(len2):
    data = data + char
while (len(data) % 4 != 0):
    data += ' '
data_length = len(data)
pcode = codec
entity = 1
data = data.encode()

# send
i = 0
for i in range(repeat2):
    sentence = ""
    sentence = pack('!IHH', data_length, pcode, entity)
    sentence += data
    time.sleep(0.5)
    clientSocket.send(sentence)
print("sending  {} to server for {} times".format(data.decode(), repeat2))

# receive
receivesentence = clientSocket.recv(1024)
data_length, pcode, entity, coded = unpack('!IHHI', receivesentence)
print("Received from server: data_len: {}  pcode: {}  entity: {}  codeD: {}".format(
    data_length, pcode, entity, coded))
