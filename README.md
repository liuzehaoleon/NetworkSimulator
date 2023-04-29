# NetworkSimulator
## a1 simulate the process of Socket programming in python using datagram sockets (UDP).
The client and server communicate according to the protocol specifications. The protocol consists of four phases. In the first two phases, the client and the server use UDP protocol to communicate and in the last two phases they use TCP protocol for communication. The client and server communicate by sending packets.

## a2 simulate a reliable transport protocol
The simulator provides the interface to the application layer (output and deliverData) and the interface provided by the network layer to the transport layer (udt_send, input).

Common.py: include the definitions of classes: Packet, Message, Event, EventType and EventList. You need to know about Packet and Message classes. The rest are used by the simulator. In addition, the constant variables that are needed within different files are defined here. For example, A, to represent the sender entity and B to represent the receiver entity. When the sender/receiver objects are initialized (inside the iniSimulator function of NetworkSimulator.py, they are assigned the correct entity name. The implementation of checksum function is placed in this file as it is used by both the sender and receiver.
main.py: It asks the user to enter the parameters needed to initialize the simulator. You can hardcode some values when testing your code. It initializes an object of type NetworkSimulator.

NetworkSimulator.py: The main code for simulator. It includes the implementations for all the interfaces needed to communicate with application layer and network layer. You should not change this code. When initialized, it also creates the sender and receiver objects.The sender and receiver objects are initialized from within the simulator. When the sender and receiver are initialized, they are passed a reference to the current network simulator object.
sender.py: The functions on the sending side of the transport protocol should be implemented here. It includes the declarations for some other auxiliary functions such as isDuplicate, etc. that is needed in the functions you are going to implement. Each sender/receiver class has a member named networkSimulator. So each sender/receiver object has access to the simulator methods through this member variable.



## a3 Implementing a distributed asynchronous distance vector routing protocol
Common.py: include the definitions of classes: RTPacket, Event, EventType and EventList. You need to know about the RTPacket class. The rest are used by the simulator.

NetworkSimulator.py: The main code for simulator. It asks the user to enter the parameters needed to initialize the simulator. You can hardcode some values when testing your code. It initializes an object of type NetworkSimulator.

Node.py: It includes the constructor for a Node as well as recvUpdate method. Each Node has an attribute named ns that points to the NetworkSimulator object. So each router has access to the simulator methods through this member variable. For example, if you want to call tolayer2 function from one of the methods in Node.py, you should call it like the following:
