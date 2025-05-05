import socket
from time import sleep

from sit_lib import *

HOST = '127.0.0.1'  # Server address
PORT = 65432        # Same port as the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#print(sdrc(client_socket, b'\x00\x00' + 0x250.to_bytes(2,"little") + b'\x01\x01\x00\x00\x00'))
print(sdrc_op(client_socket, "SIT_OPEN_SIM_CHANNEL_WITH_P2", sim_channel_data(b'\xA0\x00\x00\x05\x59\x10\x10\xFF\xFF\xFF\xFF\x89\x00\x00\x01\x00')))
print(sdrc_op(client_socket, "SIT_TRANSMIT_SIM_APDU_CHANNEL",  apdu_data(1, 0x81, 0xe2, 0x91, 0x00, 0x06, b'\xBF\x3E\x03\x5C\x01\x5A')))
print(sdrc_op(client_socket, "SIT_TRANSMIT_SIM_APDU_CHANNEL",  apdu_data(1, 0x81, 0xe2, 0x91, 0x00, 0x03, b'\xBF\x3C\x00')))
print(sdrc_op(client_socket, "SIT_TRANSMIT_SIM_APDU_CHANNEL",  apdu_data(1, 0x81, 0xe2, 0x91, 0x00, 0x03, b'\xBF\x2D\x00')))
print(sdrc_op(client_socket, "SIT_TRANSMIT_SIM_APDU_CHANNEL",  apdu_data(1, 0x81, 0xe2, 0x91, 0x00, 0x08, b'\xBF\x2D\x05\x5C\x03\x5A\xBF\x76')))

#print(sdrc_op(client_socket, "SIT_OPEN_SIM_CHANNEL_WITH_P2", sim_channel_data(b'\xa0\x00\x00\x05\x59\x10\x10\xff\xff\xff\xff\x89\x00\x00\x01\x00')))
#print(sdrc_op(client_socket, "SIT_TRANSMIT_SIM_APDU_CHANNEL",  apdu_data(1, 0x81, 0xe2, 0x91, 0x00, 0x10, b'\xbf\x2d\x0d\x5c\x0b\x5a\x90\x91\x92\xb7\x9f\x70\x95\x99\xbf\x76')))
