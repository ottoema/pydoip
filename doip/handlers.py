#!/usr/bin/python3

from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes
import socket

class DoIP_Header_Handler(object):

    def __init__(self,supported_doip_version,supported_payload_types):
        self.supported_doip_version = supported_doip_version
        self.supported_payload_types = supported_payload_types

    def decode_header(self, data):
        import struct
        #print(data.hex())
        protocol_version = struct.unpack('>B',data[0:1])[0]
        inverse_protocol_version = struct.unpack('>B',data[1:2])[0]
        payload_type = struct.unpack('>H',data[2:4])[0]
        payload_length = struct.unpack('>I',data[4:8])[0]
        payload_type_specific_message_content = data[8:]

        if not self._check_generic_doip_synchronization_pattern(protocol_version,inverse_protocol_version):
            #Send generic DoIP header NACK (NACK code)
            return Generic_DoIP_NACK_codes.Incorrect_pattern_format
            
        if not self._check_payload_type(DoIP_payload_type(payload_type)):
            #Send generic DoIP header NACK (NACK code)
            return Generic_DoIP_NACK_codes.Unknown_payload_type

        if not self._check_whether_the_message_length_exceeds_the_maximum_processable_length():
            #Send generic DoIP header NACK (NACK code)
            return Generic_DoIP_NACK_codes.Message_too_large

        if not self._check_current_doip_protocol_handler_memory():
            #Send generic DoIP header NACK (NACK code)
            return Generic_DoIP_NACK_codes.Out_of_memory

        if not self._check_payload_type_specific_length():
            return Generic_DoIP_NACK_codes.Invalid_payload_length

        return DoIP_Header( DoIP_protocol_version(protocol_version),
                            inverse_protocol_version,
                            DoIP_payload_type(payload_type),
                            payload_length,
                            payload_type_specific_message_content)

    def _check_generic_doip_synchronization_pattern(self,version,inverse):
        return version + inverse == 255

    def _check_payload_type(self,payload_type):
        return payload_type in DoIP_payload_type

    def _check_whether_the_message_length_exceeds_the_maximum_processable_length(self):
        return True

    def _check_payload_type_specific_length(self):
        return True
       
    def _check_current_doip_protocol_handler_memory(self):
        return True

class DoIP_Handler(object): 

    supported_doip_version = DoIP_protocol_version.DoIPISO1340022012
    supported_payload_types = [DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message]   

    def __init__(self,tester=True):

        if (not tester):
            print ("DoIP entity not supported, only tester")
            raise 

        self._generic_doip_nack_handlers =   {Generic_DoIP_NACK_codes.Incorrect_pattern_format : self._handle_incorrect_pattern_format,
                                     Generic_DoIP_NACK_codes.Unknown_payload_type : self._handle_unknown_payload_type,
                                     Generic_DoIP_NACK_codes.Message_too_large : self._handle_message_too_large,
                                     Generic_DoIP_NACK_codes.Out_of_memory : self._handle_out_of_memory,
                                     Generic_DoIP_NACK_codes.Invalid_payload_length : self._handle_invalid_payload_length}


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
        
        header = self.header_handler.decode_header(data)

        if (header in Generic_DoIP_NACK_codes):
            _handle_generic_doip_nack(header)
        
        print("DoIP header:")
        print("DoIP_protocol_version: " + header.protocol_version.name)
        print("DoIP inverse protocol version:" + str(header.inverse_protocol_version))
        print("DoIP payload type: " + header.payload_type.name)
        print("DoIP payload length: " + str(header.payload_length))
        
        print(header.payload_type_specific_message_content)

        # TODO: decode VA

    def _handle_generic_doip_nack(self,nack_code):
        _handle_generic_doip_nack[nack_code]()

    def _handle_incorrect_pattern_format(self):
        #Send generic DoIP header NACK (NACK code)
        #Close socket
        #ExitPoint - Socket has been closed
        pass

    def _handle_unknown_payload_type(self):
        #Send generic DoIP header NACK (NACK code)
        #Read and discard payload length bytes
        #ExitPoint - Message discarded
        pass

    def _handle_message_too_large(self):
        #Send generic DoIP header NACK (NACK code)
        #Read and discard payload length bytes
        #ExitPoint - Message discarded
        pass

    def _handle_out_of_memory(self):
        #Send generic DoIP header NACK (NACK code)
        #Read and discard payload length bytes
        #ExitPoint - Message discarded
        pass

    def _handle_invalid_payload_length(self):
        #Send generic DoIP header NACK (NACK code)
        #Close socket
        #ExitPoint - Socket has been closed        
        pass