#!/usr/bin/python3

from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes, DoIP_Payload, DoIP_Message
from doip.payload_handlers import VA_VIR_Handler
import socket
import sys

class DoIP_Header_Error(Exception):
    """Base class for exceptions related to decoding a DoIP header."""
    def __init__(self,nack_code):
        if (not isinstance(nack_code,Generic_DoIP_NACK_codes)):
            raise TypeError()
        self.__nack_code = nack_code

    def __str__(self):
        return str(self.__nack_code)

    @property
    def nack_code(self):
        return self.__nack_code

class Incorrect_pattern_format_error(DoIP_Header_Error):
    def __init__(self):
        super().__init__(Generic_DoIP_NACK_codes.Incorrect_pattern_format)

class Unknown_payload_type_error(DoIP_Header_Error):
    def __init__(self):
        super().__init__(Generic_DoIP_NACK_codes.Unknown_payload_type)
 
class Message_too_large_error(DoIP_Header_Error):
    def __init__(self):
        super().__init__(Generic_DoIP_NACK_codes.Message_too_large)

class Out_of_memory_error(DoIP_Header_Error):
    def __init__(self):
        super().__init__(Generic_DoIP_NACK_codes.Out_of_memory)

class Invalid_payload_length_error(DoIP_Header_Error):
    def __init__(self):
        super().__init__(Generic_DoIP_NACK_codes.Invalid_payload_length)

class DoIP_Header_Handler(object):

    MAXIMUM_PROCESSABLE_LENGTH = sys.maxsize

    def __init__(self,supported_doip_version,supported_payload_types):
        self.supported_doip_version = supported_doip_version
        self.supported_payload_types = supported_payload_types

    def decode_header(self, data):
        import struct
        #print(data)
        protocol_version = struct.unpack('>B',data[0:1])[0]
        inverse_protocol_version = struct.unpack('>B',data[1:2])[0]
        payload_type = struct.unpack('>H',data[2:4])[0]
        payload_length_header = struct.unpack('>I',data[4:8])[0]
        payload_type_specific_message_content = data[8:]

        if not self._check_generic_doip_synchronization_pattern(protocol_version,inverse_protocol_version):
            raise Incorrect_pattern_format_error()
            
        if not self._check_payload_type(payload_type):
            raise Unknown_payload_type_error()

        if not self._check_whether_the_message_length_exceeds_the_maximum_processable_length(payload_length_header):
            raise Message_too_large_error()

        if not self._check_current_doip_protocol_handler_memory():
            raise Out_of_memory_error()

        if not self._check_payload_type_specific_length(payload_type,payload_length_header,len(payload_type_specific_message_content)):
            raise Invalid_payload_length_error()

        return  DoIP_Message(DoIP_Header( DoIP_protocol_version(protocol_version),
                            DoIP_payload_type(payload_type),
                            payload_length_header), payload_type_specific_message_content)

    def _check_generic_doip_synchronization_pattern(self,version,inverse):
        return version + inverse == 255

    def _check_payload_type(self,payload_type):
        try:
            return DoIP_payload_type(payload_type) in DoIP_payload_type
        except ValueError:
            return False

    def _check_whether_the_message_length_exceeds_the_maximum_processable_length(self,length):
        return length < self.MAXIMUM_PROCESSABLE_LENGTH

    def _check_current_doip_protocol_handler_memory(self):
        # No sense in implementing this at the moment. 
        # Maybe use this: https://airbrake.io/blog/python-exception-handling/memoryerror
        return True
    
    def _check_payload_type_specific_length(self,payload_type,length_header,length):
        
        if (not length_header == length):
            return False
        
        payload_type = DoIP_payload_type(payload_type)
        
        if (payload_type == DoIP_payload_type.Generic_DoIP_header_negative_Acknowledge and not length == 1):
            return False
        if (payload_type == DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message and not length == 32 and not length ==33):
            return False
        return True
    

class DoIP_Handler(object): 

    supported_doip_version = DoIP_protocol_version.DoIPISO1340022012
    supported_payload_types = [DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message]   

    def __init__(self,tester=True):

        if (not tester):
            print ("DoIP entity not supported, only tester")
            raise 

        self._tester_generic_doip_nack_handlers =   {Generic_DoIP_NACK_codes.Incorrect_pattern_format : self._tester_handle_incorrect_pattern_format,
                                     Generic_DoIP_NACK_codes.Unknown_payload_type : self._tester_handle_unknown_payload_type,
                                     Generic_DoIP_NACK_codes.Message_too_large : self._tester_handle_message_too_large,
                                     Generic_DoIP_NACK_codes.Out_of_memory : self._tester_handle_out_of_memory,
                                     Generic_DoIP_NACK_codes.Invalid_payload_length : self._tester_handle_invalid_payload_length}
        
        self._tester_payload_handlers = {DoIP_payload_type.Generic_DoIP_header_negative_Acknowledge : self._generic_doip_header_nack_handler,
                                        DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message : self._vam_vir_handler}


        self.header_handler = DoIP_Header_Handler(self.supported_doip_version,self.supported_payload_types)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('10.0.2.15', DoIP_Protocol.UDP_DISCOVERY)
        print('Starting up on {} port {}'.format(*server_address))
        self.socket.bind(server_address)

    def get_vehicle_announcements(self):
        print('\nwaiting to receive message')
        data, address = self.socket.recvfrom(4096)

        print('received {} bytes from {}'.format(
            len(data), address))
        
        try: 
            message = self.header_handler.decode_header(data)
        except DoIP_Header_Error as err:
            print("Received DoIP NACK code: " + str(err))
            self._tester_handle_generic_doip_nack(err.nack_code)
        else:
            print("DoIP header:")
            print("DoIP_protocol_version: " + message.header.protocol_version.name)
            print("DoIP inverse protocol version:" + str(message.header.inverse_protocol_version))
            print("DoIP payload type: " + message.header.payload_type.name)
            print("DoIP payload length: " + str(message.header.payload_length))
            self._tester_find_payload_handler(message)

    def _tester_find_payload_handler(self,message):
        self._tester_payload_handlers[message.header.payload_type](message)
    
    def _generic_doip_header_nack_handler(self,payload):
        pass

    def _vam_vir_handler(self,message):

        va_vir_handler = VA_VIR_Handler()
        vam__vir = va_vir_handler.decode(message.payload)
        print(vam__vir.vin)
        print(vam__vir.logical_address)
        print(vam__vir.eid)
        print(vam__vir.gid)
        print(vam__vir.far)
        print(vam__vir.vin_gid_sync)

    def _tester_handle_generic_doip_nack(self,nack_code):
        self._tester_generic_doip_nack_handlers[nack_code]()

    def _tester_handle_incorrect_pattern_format(self):
        print("Tester received incorrect pattern format from DoIP entity")
        pass

    def _tester_handle_unknown_payload_type(self):
        print("Tester unknown payload type from DoIP entity")
        pass

    def _tester_handle_message_too_large(self):
        print("Tester received a too large message from DoIP entity")
        pass

    def _tester_handle_out_of_memory(self):
        print("Tester out of memory when handling message from DoIP entity")
        pass

    def _tester_handle_invalid_payload_length(self):
        print("Tester received an invalid payload length from DoIP entity")       
        pass

