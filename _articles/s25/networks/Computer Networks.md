Research: Mobile computing, wireless networking
# Intro
IP: common interface between users and networks
- How internet works
	- Architecture
	- Protocols
	- Applications (web, DNS)
- Network programming skills
	- Socket programming
	- Protocol/app implementation and design
- Principles/concepts in networking
	- Layers
	- Protocols
	- Naming
## Topics
- Network apps
	- Web, p2p app, DNS, video streaming
	- How to build multi-computer apps that communicate via the internet
- Network communication protocols
	- TCP, network layer, link layer (medium access control), physical layer


---
- Network edge: hosts, access net

## Internet
- **Devices**
	- Hosts: end systems
	- running network *apps*
- Packet switches: forward packets (chunks of data)
	- Routers, switches
- Communication links
	- Physical medium
	- Transmission rate: bandwidth
- Networks
	- Collection of devices, routers, links managed by an organization
	- E. home network, Columbia network

## Protocol
Control sending and receiving of messages

**Infrastructure** that provides services to apps
- Provides *programming interface* to distributed apps
	- *Hooks* allow sending/receiving apps to "connect to"
	- Provides service options
Rules for 
- What messages to send
- What actions to take when received a message, or other events

Protocols define the <span style="color:rgb(255, 0, 0)">format</span> and <span style="color:rgb(255, 0, 0)">order</span> of messages sent and received among network entities, and <span style="color:rgb(255, 0, 0)">actions taken</span> on message transmission, receipt
<span style="color:rgb(0, 176, 240)">E.</span> TCP
1. TCP connection request
2. TCP connection response
3. `GET`
4. sends file
Helpful to draw **FSM**, states and transition triggers/actions

## Edge
All the end devices: hosts and servers

Network core: interconnected routers, network of networks