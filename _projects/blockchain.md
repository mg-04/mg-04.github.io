---
title: "Blockchain"
excerpt: "Fully functional peer-to-peer blockchain network in Python with proof-of-work, digital signatures, Merkle trees, and a GUI wallet."
collection: projects
date: 2025-05-17
authors: Griffin Newbold, Amir Hossein Zarandi, Ming Gong, Neasha Mittal
teaser: '/images/projects/blockchain.jpg'
course: Computer Networks, Spring 2025
---

{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}

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

