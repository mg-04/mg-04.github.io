---
title: "Blockchain"
excerpt: "Final Project for Computer Networks<br/><img src='/images/projects/blockchain.jpg' style='width:500px;'>"
collection: projects
date: 2025-05-17
---
We implemented a fully functional peer-to-peer blockchain network written in Python. This system supports decentralized transaction validation, dynamic mining difficulty, Merkle tree-based verification, cryptographic signatures, and automated testing — all with a GUI wallet interface.

## Features
### Blockchain with Proof-of-Work:
- Adjustable mining difficulty based on mining frequency
- Reward transaction for the block miner

### Digital Signatures
- ECDSA signatures for all transactions
- Peers auto-generate public/private key pairs
- Transactions are signed by sender and verified before inclusion

### Merkle Trees
- Merkle root stored in each block
- Enables Simplified Payment Verification

### Peer-to-Peer Networking
- Peers discover others via a central tracker
- Peers broadcast transactions and blocks to the network
- Syncs longest valid chain automatically

### Dynamic Mining Difficulty
- Mining difficulty increases if certain conditions are met.

### GUI Payment System
- Visualizes blockchain & peers
- Sends transactions, mines blocks, verifies transactions by ID

