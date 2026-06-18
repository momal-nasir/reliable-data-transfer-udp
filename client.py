import socket
import zlib  # for chksummmm
import time

def for_checksum(data):
    # using zlib for checksum and 4 bytes for checksummmm
    chksum= zlib.crc32(data) & 0xffffffff
    return chksum.to_bytes(4, 'big')

sequence_offset = 0
flag_offset = 1
chksm_offset = 2
hdr_size = 6
# creting the packets 
def pkt_creation(seq, data, if_ack=False):
    flags = 0x01 if if_ack else 0x00
    checksum = for_checksum(data) if not if_ack else b'\x00'*4
    return bytes([seq, flags]) + checksum + data

#creating the client socket
socket_for_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_for_client.settimeout(1.0)
add_server = ('localhost', 1271)

no_of_pkts = 20
size_of_wnd = 4
BASE = 1
nxt_seq = 1
for_dup_ack = 4
pkts_to_lost = {2}  # pkts want to lost 

#pkt dictionary 
pkts = {i: pkt_creation(i, f"Packet {i}".encode()) for i in range(1, no_of_pkts+1)}
ACK_count = {i: 0 for i in range(1, no_of_pkts+1)} #ack 0 to every pkt in start 

crruption_snt = False
t_start = None

print("CLIENT sending the pktss......\n")

while BASE <= no_of_pkts:
    # snding pkt in wnd
    while nxt_seq < BASE + size_of_wnd and nxt_seq <= no_of_pkts:
        # pkt 4 corrupted
        if nxt_seq == 4 and not crruption_snt:
            corrupted = bytearray(pkts[4])
            # add 1 to chksum to corrupt the chksum
            corrupted[2] = (corrupted[2] + 1) % 256
            socket_for_client.sendto(bytes(corrupted), add_server)
            print("Pkt # 4 is corrupted and sent")
            crruption_snt = True

         # lost pkt 
        
        # if nxt_seq in pkts_to_lost:
        #  print(f"Pkt #{nxt_seq} lost not sent")

        else:
            socket_for_client.sendto(pkts[nxt_seq], add_server)
            print(f"Pkt #{nxt_seq} sent")

        # START the timer when frst pkt sent in wnd
        if t_start is None:
            t_start = time.time()

        nxt_seq += 1

    try:
        packet, _ = socket_for_client.recvfrom(1024)
        seq = packet[sequence_offset]
        flags = packet[flag_offset]

        if flags & 0x01:  # ack receiveddd
            print(f"ACK #{seq} received (count: {ACK_count[seq]})")
            ACK_count[seq] += 1

            if seq >= BASE:
                # forwrd the slide wnd
                BASE = seq + 1
                #rest the imer if there are outstanding pkts 
                t_start = time.time() if BASE != nxt_seq else None

            # fast transmit
            if ACK_count[seq] == for_dup_ack:
                lost_packet = seq + 1
                if lost_packet in pkts:
                    print(f"3 dup ack fst retransmit of Pkt#{lost_packet}")
                    socket_for_client.sendto(pkts[lost_packet], add_server)
                   # reset next_seq to base + 1
                    nxt_seq = BASE + 1

    except socket.timeout:
        # retranmit all pkts 
        if BASE == nxt_seq:
            # No  pkt stop  the timer
            t_start = None
            continue

        print(f"time out so resending the #{BASE} to #{nxt_seq - 1}")
        for i in range(BASE, nxt_seq):
            socket_for_client.sendto(pkts[i], add_server)
            print(f"timeout retranmt the #{i}")
        t_start = time.time()

print("\npkts sent successfuly")
socket_for_client.close()