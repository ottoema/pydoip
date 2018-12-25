#!/usr/bin/python3

import socket
from doip.doip import DoIP_Header
from doip.doip import DoIP_Handler

class Tester_Connection_Handler(object):



    def __init__(self,port):
        self.doip_handler = DoIP_Handler()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('10.0.2.15', port)
        print('starting up on {} port {}'.format(*server_address))
        self.socket.bind(server_address)

    def receive(self):
        while True:
            print('\nwaiting to receive message')
            data, address = self.socket.recvfrom(4096)

            print('received {} bytes from {}'.format(
                len(data), address))
            
            header = self.doip_handler.decode_header(data)
            
            print("DoIP header:")
            print("DoIP_protocol_version: " + header.protocol_version.name)
            print("DoIP inverse protocol version:" + str(header.inverse_protocol_version))
            print("DoIP payload type: " + header.payload_type.name)
            print("DoIP payload length: " + str(header.payload_length))
            
            print(header.payload_type_specific_message_content)