# Reliable Data Transfer Protocol over UDP

## Overview

This project implements a custom reliable data transfer protocol on top of UDP. Since UDP does not guarantee reliability, this system introduces mechanisms such as error detection, retransmission, and flow control to ensure correct and ordered delivery of packets.

## Features

* Sliding Window Protocol for efficient transmission
* CRC32 Checksum for error detection
* Timeout-based retransmission
* Duplicate ACK-based fast retransmit
* Handling of packet loss and corruption
* Client-server communication model

## Technologies Used

* Python
* Socket Programming
* Networking Concepts (TCP/UDP)
* CRC32 (zlib)

## How It Works

1. The client sends packets using a sliding window mechanism
2. Each packet contains:

   * Sequence number
   * Flags (ACK/data)
   * Checksum
3. The server:

   * Verifies checksum
   * Sends ACK for valid packets
   * Resends last ACK for corrupted or out-of-order packets
4. The client:

   * Retransmits packets on timeout
   * Uses duplicate ACKs to trigger fast retransmission

## Running the Project

### Step 1: Start Server

```bash
python server.py
```

### Step 2: Run Client

```bash
python client.py
```

## Concepts Implemented

* Reliable Data Transfer (RDT)
* Sliding Window Protocol
* Error Detection and Recovery
* Fast Retransmit Mechanism

## Learning Outcomes

* Understanding of how TCP ensures reliability over unreliable networks
* Hands-on implementation of networking protocols
* Experience with low-level socket programming

## Future Improvements

* Add congestion control (TCP Tahoe/Reno)
* Dynamic window size adjustment
* GUI for visualization
