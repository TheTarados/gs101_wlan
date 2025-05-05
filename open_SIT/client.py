import socket
from time import sleep

from sit_lib import *

HOST = '127.0.0.1'  # Server address
PORT = 65432        # Same port as the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#print(sdrc_op(client_socket, "SIT_SET_PREFERRED_DATA_MODEM", b'\x00'))
print(sdrc_op(client_socket, "SIT_VERIFY_SIM_PIN2", sim_unlock_data("0000")))
