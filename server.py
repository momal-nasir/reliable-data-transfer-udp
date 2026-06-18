import socket
import zlib  # for crc32 checksum


def calculate_checksum(data):
    # Use zlib.crc32 and take lower 4 bytes as checksum
    checksum = zlib.crc32(data) & 0xffffffff
    return checksum.to_bytes(4, 'big')

sequence_offset = 0
chksm_offset = 2
hdr_size = 6

socket_for_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_for_server.bind(('localhost', 1271))
print("Server is running and listening on port 1291...\n")

Exptd_sequence = 1
LAST_ACK_SENTT = 0

while True:
    packet, client_addr = socket_for_server.recvfrom(1024)
    SEQUENC = packet[sequence_offset]
    recv_checksum = packet[chksm_offset:chksm_offset+4]
    DATAA = packet[hdr_size:]

    calc_checksum = calculate_checksum(DATAA)

    # Chking the pkt
    if calc_checksum != recv_checksum:
        print(f"Packet #{SEQUENC} corrupted! Checksum mismatch.")
        if LAST_ACK_SENTT > 0:
            # RESend Last ACKK for losT pkt
            pkt_ack = bytes([LAST_ACK_SENTT, 0x01]) + b'\x00'*4
            socket_for_server.sendto(pkt_ack, client_addr)
            print(f"Resent ACK #{LAST_ACK_SENTT} due to corruption")
        continue

    if SEQUENC == Exptd_sequence:
        print(f"Pkt  #{SEQUENC} accepted")
        
        # ACK 5 lost
        # if SEQUENC == 5:
        #     print("SIMULATING ACK LOST FOR PKT 5 ")
        # else:
            #ack for successfully tranmitted pktss
        pkt_ack = bytes([SEQUENC, 0x01]) + b'\x00'*4
        socket_for_server.sendto(pkt_ack, client_addr)
        print(f"ACK #{SEQUENC} sent")

        LAST_ACK_SENTT = SEQUENC
        Exptd_sequence += 1

    else:
        # pkt out of order
        print(f"out of order pkt #{SEQUENC}, expecting #{Exptd_sequence}")
        if LAST_ACK_SENTT > 0:
            pkt_ack = bytes([LAST_ACK_SENTT, 0x01]) + b'\x00'*4
            socket_for_server.sendto(pkt_ack, client_addr)
            print(f"Rsnd ack #{LAST_ACK_SENTT} in case of out of order pkts")