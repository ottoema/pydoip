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
    Alive_check_response = 0x0008
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

class Further_Action_Required(Enum):
    No_further_action_required = 0x00
    Routing_activation_required_to_initiate_central_security = 0x10

class DoIP_Header(object):

    def __init__(self,protocol_version,payload_type,payload_length):
        
        if (isinstance(protocol_version,DoIP_protocol_version) and
            isinstance(payload_type,DoIP_payload_type)):   

            self.__protocol_version = protocol_version        
            self.__inverse_protocol_version = ~protocol_version.value
            self.__payload_type = payload_type
            self.__payload_length = payload_length
        else:
            raise TypeError("DoIP header, invalid type.")
    
    @property
    def protocol_version(self):
        return self.__protocol_version
    
    @property
    def inverse_protocol_version(self):
        return self.__inverse_protocol_version

    @property
    def payload_type(self):
        return self.__payload_type

    @property
    def payload_length(self):
        return self.__payload_length

    def __eq__(self,other):
        if (isinstance(other,DoIP_Header) and    
                self.protocol_version == other.protocol_version and
                self.inverse_protocol_version == other.inverse_protocol_version and
                self.payload_type == other.payload_type and
                self.payload_length == other.payload_length):
            return True
        return False

    def __ne__(self,other):
        if (isinstance(other,DoIP_Header) and 
                self.protocol_version == other.protocol_version and
                self.inverse_protocol_version == other.inverse_protocol_version and
                self.payload_type == other.payload_type and
                self.payload_length == other.payload_length):
            return False
        return True

    def __str__(self):
        return """Protocol version: {0}
                Inverse_protocol_version: {1}
                Payload_type: {2}
                Payload_length: {3}""".format(self.protocol_version,self.inverse_protocol_version,self.payload_type,self.payload_length)

class DoIP_Payload(object):

    def __init__(self,payload_type):
        if (not isinstance(payload_type,DoIP_payload_type)):
            raise TypeError("DoIP_Payload not instansiated correctly through a subclass")
        else:
            self.__payload_type = payload_type

    @property
    def payload_type(self):
        return __payload_type

class DoIP_Message(object):
    def __init__(self,header,payload):
        if (not isinstance(header,DoIP_Header)):
            raise TypeError("Header not a DoIP_Header")
        if (not header.payload_length == len(payload)):
            raise AssertionError("Payload length according to header not matching with actual payload length.")

        self.__header = header
        self.__payload = payload

    @property
    def header(self):
        return self.__header

    @property
    def payload(self):
        return self.__payload

class DoIP_VA_VIR(DoIP_Payload):
    
    def __init__(self,vin,logical_address,eid,gid,far,vin_gid_sync_status=0):
        super().__init__(DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message)

        self.__vin = vin
        self.__logical_address = logical_address
        self.__eid = eid
        self.__gid = gid
        self.__far = far
        self.__vin_gid_sync = vin_gid_sync_status

    @property
    def vin(self):
        return self.__vin
    
    @property
    def logical_address(self):
        return self.__logical_address

    @property
    def eid(self):
        return self.__eid

    @property
    def gid(self):
        return self.__gid

    @property
    def far(self):
        return self.__far

    @property
    def vin_gid_sync(self):
        return self.__vin_gid_sync


class DoIP_Protocol(object):

    TCP_DATA = 13400                        #[DoIP-001]
    UDP_DISCOVERY = 13400                   #[DoIP-008]
    UDP_TEST_EQUIPMENT_REQUEST = 0          #[DoIP-135], dynamically assigned

    def __init__(self):
        pass