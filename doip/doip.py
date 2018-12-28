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

class Generic_DoIP_NACK_codes(Enum):
    Incorrect_pattern_format = 0x00
    Unknown_payload_type = 0x01
    Message_too_large = 0x02
    Out_of_memory = 0x03
    Invalid_payload_length = 0x04

class DoIP_Header(object):


    def __init__(self,protocol_version,inverse_protocol_version,payload_type,payload_length,payload_type_specific_message_content):
        
        if (isinstance(protocol_version,DoIP_protocol_version) and
            isinstance(payload_type,DoIP_payload_type)):   

            self.protocol_version = protocol_version        
            self.inverse_protocol_version = ~protocol_version.value
            self.payload_type = payload_type
            self.payload_length = payload_length
            self.payload_type_specific_message_content = payload_type_specific_message_content
        else:
            raise ValueError("DoIP header, invalid type.")

    def __eq__(self,other):
        if (    self.protocol_version == other.protocol_version and
                self.inverse_protocol_version == other.inverse_protocol_version and
                self.payload_type == other.payload_type and
                self.payload_length == other.payload_length):
            return True
        return False

    def __ne__(self,other):
        if (    self.protocol_version == other.protocol_version and
                self.inverse_protocol_version == other.inverse_protocol_version and
                self.payload_type == other.payload_type and
                self.payload_length == other.payload_length):
            return False
        return True

class DoIP_Protocol(object):

    TCP_DATA = 13400                        #[DoIP-001]
    UDP_DISCOVERY = 13400                   #[DoIP-008]
    UDP_TEST_EQUIPMENT_REQUEST = 0          #[DoIP-135], dynamically assigned

    def __init__(self):
        print("""I'm DOIP""")
