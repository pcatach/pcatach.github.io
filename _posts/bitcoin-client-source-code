---
layout: post
title:  "The bitcoin client source code"
date:   
categories: tech
---
How to build a minimally working version of the client

```
#!/bin/bash
set -e
./autogen.sh
./configure --without-miniupnpc --without-natpmp\
            --disable-wallet --without-gui --disable-tests\
            --disable-bench --disable-man --disable-util-wallet
make -j4 ./src/bitcoind
```

For cleanup:

```
make clean
```

For debugging automake variables:

```
make print-[VARIABLE]
```

## Basic code organization

The main function for bitcoind is in src/bitcoind.cpp. Initialization and shutdown bits are in src/init.cpp and src/shutdown.cpp. Node struct lives under src/node/, contains references to chain state (node.chain), wallet (not in use) and connection state. Node initialization and network initialization (RPC and HTTP servers) is in src/init.ccp:AppInitMain

The components of a node are:

CMainParams (src/chainparams.cpp and subclasses)

Keeps parameters that influence the chain consensus protocol e.g. blocks where each BIP became active, e.g. defaultAssumeValid hardcodes a block before which all blocks are assumed to be valid.

Fee estimator (src/fees.cpp)

CTxMemPool (src/txmempool.cpp)

Stores transactions that could be included in the next block. Transactions are added when they are emitted or received by the node.

ChainstateManager (src/validation.cpp)

UTXO and chain functionalities. The blockchain is a tree with the genesis in the beginning and multiple possible candidates to be the next block. This tree is structured as a hash table (the block index), and a chain (CChain, src/chain.h) is an indexed chain of blocks.

On the client initialization, ActivateBestChain is called in the loadblk thread, which sets the active block to the chain with the most work done.

Address Manager (src/addrman.cpp)

Keeps a table of addresses. Asynchronously dumps it to peers.dat

Ban Manager (src/banman.cpp)

Keeps a table of addresses with which connections should be refused or discouraged.

Connection Manager (src/net.cpp)

net.h defines network functionalities such as Discover() which finds network interfaces in the host. The connection manager (CConman) holds options such as nMaxConnections and m_peer_connect. It also holds vNodes, the vector of connected nodes.

Maybe the most important bit is the Start() function: 1. Initialize binds: will by default create socket for listening on 0.0.0.0:8333 (ipv4 default) ::8333 (ipv6 default) and 127.0.0.1:8334 (tor, can't disable the port binding) 2. Load addresses from anchor database 3. Initialize networking threads 4. Schedule network addresses dump

Peer Manager (src/net_processing.cpp)

TODO

Scheduler (src/scheduler.h)

Simple class for background tasks that should be run periodically or once "after a while"

Databases in a node

peers.dat (addrman)

mempool.dat (transaction pool (if cached))

fee_estimate.dat (fee estimations)

anchors.dat (Addresses of block-relay-only peers to reconnect at startup)

chainstate (leveldb UTXO cache) NOTE: this db is obfuscated because it used to trigger antivirus software

blocks (leveldb blocks cache)

Threads in a node

Network processing threads started in init.cpp and net.ccp net: "Sends/Receives data from peers on port 8333" addcon: "Opens network connections to added nodes" opencon: "Initiates new connections to peers" (what's the difference?) msghand: "Sending and receiving messages, runs net_processing and validation logic"

script verification threads (i.e. signature verification)

scheduler thread (?)

loadblk thread (imports all blocks since genesis, finds active chain)

Network processing threads

ThreadSocketHandler()

We identify 2 sets of sockets: "receive sockets" (all bound sockets) and "send sockets" (sockets with data to be sent) there's also "error sockets" but I'm not sure about them.

We iterate through receiving sockets calling AcceptConnection() on them. This uses the accept() syscall to retrieve the first connection request in the queue, creates a CNode object representing that request and adds it to the vNodes vector.

In addition to accepting new connections, we "service" each existing nodes. That means that for every node, we send any pending data from "send sockets" and receive any remaining data from "receive sockets" or "error sockets".

ThreadOpenConnections()

Initiates network connections. In the absence of anchors, it will attempt to connect to a list of fixed nodes defined in src/chainparamseeds.h. Once we have a list of anchor/seed addresses, we call OpenNetworkConnection() to initiate the connection to the address and create a CNode from it. Finally, it adds that CNode to vNodes.

ThreadOpenAddedConnections()

TODO

ThreadMessageHandler()

TODO