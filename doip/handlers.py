#!/usr/bin/python3

from doip.doip import DoIP_Header
from doip.doip import DoIP_protocol_version
from doip.doip import DoIP_payload_type

class DoIP_Handler(object):

    supported_doip_version = DoIP_protocol_version.DoIPISO1340022012        
    
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