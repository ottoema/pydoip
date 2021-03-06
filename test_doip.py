#!/usr/bin/python3

from doip.handlers import DoIP_Handler, DoIP_Header_Handler
from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes, DoIP_Message
import unittest
import threading

#vam_vir_payload_too_long = bytes.fromhex('FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
payload_bytes_vam_vir_too_long = b'__YV1LFA2BCG1038271\x10\x01\x00\x01\x02\x03\x04\x05\x05\x04\x03\x02\x01\x00\x00'
payload_bytes_vam_vir = b'YV1LFA2BCG1038271\x10\x01\x00\x01\x02\x03\x04\x05\x05\x04\x03\x02\x01\x00\x00'
header_bytes_vam_vir = bytes.fromhex('01 fe 00 04 00 00 00 20')
header_bytes_with_incorrect_pattern_format = bytes.fromhex('02 12 00 00 00 00 00 01 00')

header_bytes_nack_with_correct_pattern_format = bytes.fromhex('01 fe 00 00 00 00 00 01 00')
header_nack = DoIP_Header(DoIP_protocol_version.DoIPISODIS1340022010,DoIP_payload_type.Generic_DoIP_header_negative_Acknowledge,1)

list_of_header_bytes_and_header_with_correct_pattern_format = [
                (header_bytes_nack_with_correct_pattern_format, 
                header_nack),
                (header_bytes_vam_vir + payload_bytes_vam_vir, 
                DoIP_Header(DoIP_protocol_version.DoIPISODIS1340022010,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32)),
                (bytes.fromhex('FF 00 00 04 00 00 00 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'), 
                DoIP_Header(DoIP_protocol_version.VEHCILE_IDENTIFICATION_REQUEST,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,33))]

list_of_header_bytes_with_correct_payload_type = [ bytes.fromhex('02 fd 00 00 00 00 00 01 00'),
                                                            bytes.fromhex('02 fd 00 01 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 02 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 03 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 04 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 05 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 06 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 07 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 08 00 00 00 00'),
                                                            bytes.fromhex('02 fd 40 01 00 00 00 00'),
                                                            bytes.fromhex('02 fd 40 02 00 00 00 00'),
                                                            bytes.fromhex('02 fd 40 03 00 00 00 00'),
                                                            bytes.fromhex('02 fd 40 04 00 00 00 00'),
                                                            bytes.fromhex('02 fd 80 01 00 00 00 00'),
                                                            bytes.fromhex('02 fd 80 02 00 00 00 00'),
                                                            bytes.fromhex('02 fd 80 03 00 00 00 00')]

class Test_DoIP_Message(unittest.TestCase):
    def test_wrong_header_type(self):
        with self.assertRaises(TypeError):
            message = DoIP_Message(12,bytes.fromhex('01 00'))

    def test_wrong_payload_length(self):
        
        header = DoIP_Header(DoIP_protocol_version.DoIPISO1340022012,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32)
        with self.assertRaises(AssertionError):
            message = DoIP_Message(header,payload_bytes_vam_vir_too_long)

    def test_correct_message(self):
        header = DoIP_Header(DoIP_protocol_version.DoIPISO1340022012,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32)
        message = DoIP_Message(header,payload_bytes_vam_vir)
        self.assertTrue(message.header == header,"Header not equal after creating DoIP_Message")
        self.assertTrue(message.payload == payload_bytes_vam_vir,"Payload not correct after creating DoIP_Message")

class TesterThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.doip_handler = DoIP_Handler()

    def run(self):
        self.doip_handler.get_vehicle_announcements()

class Test_DoIP_Handler(unittest.TestCase):
    def setUp(self):

        import socket
        import sys

        self.tester = TesterThread()
        self.tester.start()

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_address = ('10.0.2.15', DoIP_Protocol.UDP_DISCOVERY)
        
    def tearDown(self):
        self.tester.join()

    def test_tester_socket_connection(self):

        try:
            
            # Send data
            sent = self.sock.sendto(header_bytes_vam_vir, self.server_address)

        finally:
            self.sock.close()

class Test_DoIP_VA_VIR_Handler(unittest.TestCase):
    def setUp(self):
        from doip.payload_handlers import VA_VIR_Handler
        self.va_vir_handler = VA_VIR_Handler()

    def test_decode_payload_with_correct_data(self):
        from doip.doip import DoIP_VA_VIR 
        result = self.va_vir_handler.decode(payload_bytes_vam_vir)
        #self.assertEqual

class Test_DoIP_Header_Handler_(unittest.TestCase):
    def setUp(self):
        self.header_handler = DoIP_Header_Handler(DoIP_protocol_version.DoIPISO1340022012,
        [DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message])        

    def test_decode_header_with_incorrect_pattern_format(self):
        from doip.handlers import DoIP_Header_Error, Incorrect_pattern_format_error
        
        with self.assertRaises(Incorrect_pattern_format_error) as cm:
            message = self.header_handler.decode_header(header_bytes_with_incorrect_pattern_format)
        self.assertEqual(cm.exception.nack_code,Generic_DoIP_NACK_codes.Incorrect_pattern_format)
        
    def test_decode_header_with_correct_pattern_format(self):

        for header_bytes, header in list_of_header_bytes_and_header_with_correct_pattern_format:
            message = self.header_handler.decode_header(header_bytes)
            self.assertTrue(message.header == header,"Wrong decoding of header\n" + str(header_bytes) + "\n" + str(message.header) + "\n" + str(header))

    def test_decode_header_with_known_payload_type(self):
        from doip.handlers import DoIP_Header_Error, Unknown_payload_type_error

        for header in list_of_header_bytes_with_correct_payload_type:
            message = self.header_handler.decode_header(header)
            self.assertNotEqual(message,Generic_DoIP_NACK_codes.Unknown_payload_type,'Payload header should be supported but received NACK Unknown payload type')

    def test_decode_header_with_unknown_payload_type(self):
        _list_of_header_bytes_with_incorrect_payload_type = [  bytes.fromhex('02 fd 00 09 00 00 00 00'),
                                                                bytes.fromhex('02 fd 40 00 00 00 00 00'),
                                                                bytes.fromhex('02 fd 40 05 00 00 00 00'),
                                                                bytes.fromhex('02 fd 80 00 00 00 00 00'),
                                                                bytes.fromhex('02 fd 80 04 00 00 00 00'),
                                                                bytes.fromhex('02 fd EF FF 00 00 00 00') ]

        for header in _list_of_header_bytes_with_incorrect_payload_type:
            from doip.handlers import DoIP_Header_Error, Unknown_payload_type_error
            with self.assertRaises(Unknown_payload_type_error) as cm:
                message = self.header_handler.decode_header(header)
            
    def test_decode_header_with_payload_size_bigger_than_processable(self):
        from doip.handlers import DoIP_Header_Error, Message_too_large_error
        _header_bytes_with_big_payload_length = bytes.fromhex('02 fd 00 08 ff ff ff ff')
        length = self.header_handler.MAXIMUM_PROCESSABLE_LENGTH
        self.header_handler.MAXIMUM_PROCESSABLE_LENGTH = int(b'fffffffe',16)
        with self.assertRaises(Message_too_large_error) as cm:
            message = self.header_handler.decode_header(_header_bytes_with_big_payload_length)
        self.header_handler.MAXIMUM_PROCESSABLE_LENGTH = length
        self.assertEqual(cm.exception.nack_code,Generic_DoIP_NACK_codes.Message_too_large)

    def test_decode_header_with_correct_payload_length(self):
        _list_of_header_bytes_with_correct_payload_length = [   bytes.fromhex('02 fd 00 00 00 00 00 01 00'),
                                                                bytes.fromhex('02 fd 00 04 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'),
                                                                bytes.fromhex('02 fd 00 04 00 00 00 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00') ]
        for header in _list_of_header_bytes_with_correct_payload_length:
            message = self.header_handler.decode_header(header)
            self.assertNotEqual(message,Generic_DoIP_NACK_codes.Invalid_payload_length,'Did not expect NACK Invalid payload length')

    def test_decode_header_with_wrong_payload_length(self):
        from doip.handlers import DoIP_Header_Error, Invalid_payload_length_error, Generic_DoIP_NACK_codes
        _list_of_header_bytes_with_wrong_payload_length = [ bytes.fromhex('02 fd 00 00 00 00 00 02 00'),
                                                            bytes.fromhex('02 fd 00 04 00 00 00 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 04 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 04 00 00 00 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'),
                                                            bytes.fromhex('02 fd 00 04 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00') ]
        for header in _list_of_header_bytes_with_wrong_payload_length:
            with self.assertRaises(Invalid_payload_length_error) as cm:
                message = self.header_handler.decode_header(header)
            self.assertEqual(cm.exception.nack_code,Generic_DoIP_NACK_codes.Invalid_payload_length)

    
if __name__ == '__main__':
    unittest.main()