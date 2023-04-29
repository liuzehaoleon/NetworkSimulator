# NetworkSimulator
a1 simulate the process of Socket programming in python using datagram sockets (UDP).
The client and server communicate according to the protocol specifications. The protocol consists of four phases. In the first two phases, the client and the server use UDP protocol to communicate and in the last two phases they use TCP protocol for communication. The client and server communicate by sending packets.

a2 simulate a reliable transport protocol
The simulator provides the interface to the application layer (output and deliverData) and the interface provided by the network layer to the transport layer (udt_send, input).


a3 Implementing a distributed asynchronous distance vector routing protocol

Common.py: include the definitions of classes: RTPacket, Event, EventType and EventList. You need to know about the RTPacket class. The rest are used by the simulator.

NetworkSimulator.py: The main code for simulator. It asks the user to enter the parameters needed to initialize the simulator. You can hardcode some values when testing your code. It initializes an object of type NetworkSimulator.

Node.py: It includes the constructor for a Node as well as recvUpdate method. Each Node has an attribute named ns that points to the NetworkSimulator object. So each router has access to the simulator methods through this member variable. For example, if you want to call tolayer2 function from one of the methods in Node.py, you should call it like the following:
