import socket
import multiprocessing as mp
import time
import os
from select import select
from sit_lib import *


HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Arbitrary non-privileged port
fd_name = {}
def ope(s):
    fd = os.open("/dev/"+s, os.O_RDWR)
    fd_name[fd] = s
    return fd

devs = ["umts_ipc0",
        "umts_rfs0",
        "umts_ipc1",
        "umts_router",
        "umts_dm0",
        "umts_loopback",
        "umts_rcs0",
        "umts_rcs1",
        "umts_toe0",
        "umts_wfc0",
        "umts_wfc1"]
fds = [ope(i) for i in devs] + [ope("oem_ipc"+str(i)) for i in range(8)]

handler_list = []
def handle_client_connection(seq_conn):
    """This function handles the socket connection and writes to a file."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        process = mp.Process(target=handle_messages,
                                          args = (conn, addr, seq_conn))
        process.start()
        handler_list.append(process)


def handle_messages(conn, addr, seq_conn):
    """This function handles the socket connection and writes to a file."""
    seqnum = 1
    while True:
        data = conn.recv(1024)
        #data: 2 bytes of type | 2 bytes of op | N bytes of data
        if not data:
            continue

        do_format = data[0]
        rfs_send = data[1]
        data = data[2:]
        if do_format != b'\x00':
            #insert len seqnum
            packet = data[:4] +\
                (len(data)+8).to_bytes(2, 'little') +\
                seqnum.to_bytes(2, 'little') +\
                b'\x00\x00\x00\x00'+\
                data[4:]
        
        else:
            packet = data
            byt_seq = data[6:8]
            if byt_seq != b'\x00\x00':
                seqnum = int.from_bytes(byt_seq, "little")
        seq_conn[seqnum] = conn
        # Write received data to a file
        os.write(fds[rfs_send == b'\x00'], packet)
        print_sit(packet, f"{seqnum} sending to  {fd_name[fds[rfs_send == b'\x00']]}")
        seqnum += 1
        seqnum &= 0xffff
        if seqnum == 0:
            seqnum = 1

def read_file_and_respond(seq_conn):
    """This function reads the file and sends data back to the client."""
    while True:
        (readfds, _, _) = select(fds, [], [])
        for fd in readfds:
            data = os.read(fd, 1000)
            seqnum = int.from_bytes(data[6:8], "little")
            print_sit(data, f"{fd_name[fd]}: {seqnum} received")
            if seqnum not in seq_conn:
                print(data)
                print(list(map(hex,data)))
                continue
            seq_conn[seqnum].send(data)
            


def main():
    """Main function to initiate processes."""
    # Create two processes
    manager = mp.Manager()

    seq_conn = manager.dict()
    process2 = mp.Process(target=read_file_and_respond,
                          args=(seq_conn,))
    process1 = mp.Process(target=handle_client_connection,
                          args=(seq_conn,))

    # Start the processes
    process1.start()
    process2.start()

    # Join the processes so the main process waits for them
    process1.join()
    process2.join()

if __name__ == "__main__":
    main()

