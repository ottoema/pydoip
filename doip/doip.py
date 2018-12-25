#!/usr/bin/python3

from enum import Enum

class DoIP_protocol_version(Enum):

    DoIPISODIS1340022010 = 0x01
    DoIPISO1340022012 = 0x02
    VEHCILE_IDENTIFICATION_REQUEST = 0xFF

class DoIP_payload_type(Enum):

    Generic_DoIP_header_negative_Acknowledge = 0x0000
    Vehicle_identification_request_message = 0x0001
    Vehicle_identification_request_message_with_EID = 0x0002
    Vehicle_identification_request_message_with_VIN = 0x0003
    Vehicle_announcement_message__vehicle_identification_response_message = 0x0004
    Routing_activation_request = 0x0005
    Routing_activation_response = 0x0006
    Alive_check_request = 0x0007
    DoIP_entity_status_request = 0x4001
    DoIP_entity_status_response = 0x4002
    Diagnostic_power_mode_information_request = 0x4003
    Diagnostic_power_mode_information_response = 0x4004
    Diagnostic_message = 0x8001
    Diagnostic_message_positive_acknowledgement = 0x8002
    Diagnostic_message_negative_acknowledgement = 0x8003


class DoIP_Header(object):

    protocol_version = 0
    inverse_protocol_version = 0
    payload_type = 0
    payload_length = 0
    payload_type_specific_message_content = 0

    def __init__(self,protocol_version,payload_type,payload_length,payload_type_specific_message_content):
        
        if (isinstance(protocol_version,DoIP_protocol_version) and
            isinstance(payload_type,DoIP_payload_type)):        
            self.protocol_version = protocol_version        
            self.inverse_protocol_version = ~protocol_version.value
            self.payload_type = payload_type
            self.payload_type_specific_message_content = payload_type_specific_message_content
        else:
            raise ValueError("DoIP header, invalid type.")

    def __init__(self,data):
        print(data[0:7].hex())
        self.protocol_version = DoIP_protocol_version(self.bytes_to_int(data[0:1]))
        self.inverse_protocol_version = self.bytes_to_int(data[1:2])

        #if (not self.protocol_version.value == ~self.inverse_protocol_version):
        #    raise ValueError("DoIP header, invalid protocol version or inverse.")
        #print(int(data[2:4].hex())) #how to convert binary to dec?
        self.payload_type = DoIP_payload_type(self.bytes_to_int(data[2:4]))
        self.payload_length = self.bytes_to_int(data[4:7])
        self.payload_type_specific_message_content = data[8:]
        
    def bytes_to_int(self,data, order='big',sign=False):
        return int.from_bytes(data,byteorder='big')

    #def to_bytes(self):

class DoIP_Protocol(object):

    TCP_DATA = 13400                        #[DoIP-001]
    UDP_DISCOVERY = 13400                   #[DoIP-008]
    UDP_TEST_EQUIPMENT_REQUEST = 0          #[DoIP-135], dynamically assigned

    def __init__(self):
        print("""I'm DOIP""")

class DoIP_Handler(object):
    
    def decode_header(self, data):
        return DoIP_Header(data)

    #def encode_header():