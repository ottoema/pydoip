#!/usr/bin/python3

from doip.doip import DoIP_Header
from doip.doip import DoIP_protocol_version
from doip.doip import DoIP_payload_type
from doip.doip import DoIP_Protocol
import socket


class DoIP_Handler(object):

    supported_doip_version = DoIP_protocol_version.DoIPISO1340022012       

    def __init__(self,tester=True):
        if (not tester):
            print ("DoIP entity not supported, only tester")
            raise 

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('10.0.2.15', DoIP_Protocol.UDP_DISCOVERY)
        print('Starting up on {} port {}'.format(*server_address))
        self.socket.bind(server_address)

    def get_vehicle_announcements(self):
        print('\nwaiting to receive message')
        data, address = self.socket.recvfrom(4096)

        print('received {} bytes from {}'.format(
            len(data), address))
        
        header = self.decode_header(data)
        
        print("DoIP header:")
        print("DoIP_protocol_version: " + header.protocol_version.name)
        print("DoIP inverse protocol version:" + str(header.inverse_protocol_version))
        print("DoIP payload type: " + header.payload_type.name)
        print("DoIP payload length: " + str(header.payload_length))
        
        print(header.payload_type_specific_message_content)

        # TODO: decode VA

   # def get_available_vehicles(self):
    
    def decode_header(self, data):

        protocol_version = DoIP_protocol_version(self._bytes_to_int(data[0:1]))
        inverse_protocol_version = self._bytes_to_int(data[1:2])

        #if (not self.protocol_version.value == ~self.inverse_protocol_version):
        #    raise ValueError("DoIP header, invalid protocol version or inverse.")
        #print(int(data[2:4].hex())) #how to convert binary to dec?
        payload_type = DoIP_payload_type(self._bytes_to_int(data[2:4]))
        payload_length = self._bytes_to_int(data[4:7])
        payload_type_specific_message_content = data[8:]

        return DoIP_Header(protocol_version,inverse_protocol_version,payload_type,payload_length,payload_type_specific_message_content)
        
    def _bytes_to_int(self,data, order='big',sign=False):
        return int.from_bytes(data,byteorder='big')
        return DoIP_Header(data)

    #def encode_header():