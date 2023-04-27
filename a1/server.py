__author__      = "Zehao Liu", "Zhenggan Luo"
__copyright__   = "Copyright 2022, CP372"

# Import socket module
from socket import *
from struct import *
import time
import sys  # In order to terminate the program
from random import randint as ri

import SocketServer, threading, time

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8888

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()



# Assign a port number
serverPort = 12000
while True:
	serverSocket = socket(AF_INET, SOCK_DGRAM)

	# Bind the socket to server address and server port
	serverSocket.bind(("", serverPort))

	recsentence, clientAddress = serverSocket.recvfrom(1024)

	# server - output A
	data_length, pcode, entity, data = unpack('!IHH16s', recsentence)
	data = data.decode()
	print("receiving from the client: data_length: {}  pcode: {}  entity: {}  data: {}\n".format(
	    data_length, pcode, entity, data))

	# server - input A
	data_length = 12
	pcode = 0
	entity = 2
	repeat = ri(5, 20)
	udp_port = ri(20000, 30000)
	length = ri(50, 100)
	codea = ri(100, 400)


	# print
	print("------------ Starting Stage A  ------------")
	print("sending to the client: data_length: {}  pcode: {}  entity: {}  repeat: {}  udp_port: {}  len: {} codeA: {}".format(
	    data_length, pcode, entity, repeat, udp_port, length, codea))

	# sent mes
	FORMAT = '!IHHIIHH'
	sentence = pack(FORMAT, data_length, pcode, entity,
	                repeat, udp_port, length, codea)

	serverSocket.sendto(sentence, clientAddress)

	# newport phase b
	serverPort = udp_port

	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(("", serverPort))

	# print
	print("SERVER: Server ready on the new UDP port: {}".format(serverPort))
	print("------------ End of Stage A  ------------\n")

	# B-1
	print("------------ Starting Stage B  ------------")
	repacket_id_list=[]
	for i in range(repeat):
	    recsentence, clientAddress = serverSocket.recvfrom(1024)
	    data_len, pcode, entity, repacket_id = unpack('!IHHI', recsentence[:12])
	    assert len(recsentence)%4==0, "message received should be divsible by 4"#packet has correct length 
	    if repacket_id_list: # if the list is not empty
	        assert max(repacket_id_list)<= repacket_id, "packet_id sent by sender should in order"
	    if repacket_id not in repacket_id_list:
	        repacket_id_list.append(repacket_id)
	        print("received_packet_id =  {} data_len =  {}  pcode: {}".format(
	        repacket_id, data_len, pcode))

	    # sent
	    sentence = ""
	    data_len = 4
	    entity = 2
	    acked_packet_id = repacket_id
	    sentence = pack('!IHHI', data_len, pcode, entity, acked_packet_id)
	    time.sleep(0.5)
	    serverSocket.sendto(sentence, clientAddress)

	# B-2
	sentence = ""
	data_len = 8
	tcp_port = ri(20000, 30000)
	codeb = ri(100, 400)
	sentence = pack('!IHHII', data_len, pcode, entity, tcp_port, codeb)
	time.sleep(0.5)
	serverSocket.sendto(sentence, clientAddress)
	print("B2: sending tcp_port {} codeB {}".format(tcp_port, codeb))
	print("------------ End of Stage B  ------------\n")
	serverSocket.close()

	# TCP phase C
	serverPort = tcp_port

	# Bind
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(("", serverPort))
	serverSocket.listen(1)
	print("------------ Stating Stage C ------------")
	print("The server is ready to receive on tcp port:  {}".format(serverPort))

	connectionSocket, addr = serverSocket.accept()

	pcode = codeb
	entity = 2
	repeat2 = ri(5, 20)
	len2 = ri(50, 100)
	codec = ri(100, 400)
	char = 'K'
	data_length = 12 + len(char)
	sentence = pack('!IHHIII', data_length, pcode,
	                entity, repeat2, len2, codec)
	sentence += char.encode()
	connectionSocket.send(sentence)
	print("Server Sending to the client:  data_length: {} code: {}  entity: {}  repeat2: {}  len2: {} codeC:  {}".format(
	    data_length, pcode, entity, repeat2, len2, codec, char))
	print("------------ End of Stage C    ------------\n")

	#phase D
	print("------------ Starting Stage D  ------------")
	print("Starting to Receive packets from client")
	i = 0
	for i in range(repeat2):
	    # connectionSocket, addr = serverSocket.accept()
	    recsentence = connectionSocket.recv(1024)
	    data_length, pcode, entity = unpack('!IHH', recsentence[:8])
	    data = recsentence[8:].decode()
	    print("i =  {} data_len:  {} pcode:  {} entity:  {} data:  {}".format(
	        i, data_len, pcode, entity, data))

	entity = 2
	coded = ri(100, 400)
	sentence = pack('!IHHI', 4, pcode, entity, coded)
	connectionSocket.send(sentence)

	# close
	connectionSocket.close()

# sys.exit()  # Terminate the program after sending the corresponding data
