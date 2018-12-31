#!/usr/bin/python3

from doip.handlers import DoIP_Handler, DoIP_Header_Handler
from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes
import unittest
import threading

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
        message = bytes.fromhex('01 fe 00 04 00 00 00 20')

        try:
            
            # Send data
            sent = self.sock.sendto(message, self.server_address)

        finally:
            self.sock.close()


class Test_DoIP_Header_Handler_(unittest.TestCase):
    def setUp(self):
        self.header_handler = DoIP_Header_Handler(DoIP_protocol_version.DoIPISO1340022012,
        [DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message])        

    def test_decode_header_with_incorrect_pattern_format(self):
        _header_bytes_with_incorrect_pattern_format = bytes.fromhex('02 12 00 04 00 00 00 20')

        result, payload = self.header_handler.decode_header(_header_bytes_with_incorrect_pattern_format)
        self.assertEqual(result,Generic_DoIP_NACK_codes.Incorrect_pattern_format,"Wrong decoding of header:")
        
    def test_decode_header_with_correct_pattern_format(self):

        _list_of_header_bytes_with_correct_pattern_format = [
                (bytes.fromhex('01 fe 00 04 00 00 00 20'), 
                DoIP_Header(DoIP_protocol_version.DoIPISODIS1340022010,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32)),
                (bytes.fromhex('02 fd 00 04 00 00 00 20'), 
                DoIP_Header(DoIP_protocol_version.DoIPISO1340022012,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32)),
                (bytes.fromhex('FF 00 00 04 00 00 00 20'), 
                DoIP_Header(DoIP_protocol_version.VEHCILE_IDENTIFICATION_REQUEST,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32))]

        for header_bytes, header in _list_of_header_bytes_with_correct_pattern_format:
            result, payload = self.header_handler.decode_header(header_bytes)
            self.assertTrue(result == header,'Wrong decoding of header')

    def test_decode_header_with_known_payload_type(self):

        _list_of_header_bytes_with_correct_payload_type = [bytes.fromhex('02 fd 00 00 00 00 00 00'),
                                                        bytes.fromhex('02 fd 00 01 00 00 00 00'),
                                                        bytes.fromhex('02 fd 00 02 00 00 00 00'),
                                                        bytes.fromhex('02 fd 00 03 00 00 00 00'),
                                                        bytes.fromhex('02 fd 00 04 00 00 00 20'),
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

        for header in _list_of_header_bytes_with_correct_payload_type:
            result, payload = self.header_handler.decode_header(header)
            self.assertNotEqual(result,Generic_DoIP_NACK_codes.Unknown_payload_type,'Payload header should be supported but received NACK Unknown payload type')

    def test_decode_header_with_unknown_payload_type(self):
        _list_of_header_bytes_with_incorrect_payload_type = [  bytes.fromhex('02 fd 00 09 00 00 00 00'),
                                                                bytes.fromhex('02 fd 40 00 00 00 00 00'),
                                                                bytes.fromhex('02 fd 40 05 00 00 00 00'),
                                                                bytes.fromhex('02 fd 80 00 00 00 00 00'),
                                                                bytes.fromhex('02 fd 80 04 00 00 00 00'),
                                                                bytes.fromhex('02 fd EF FF 00 00 00 00') ]

        for header in _list_of_header_bytes_with_incorrect_payload_type:
            result, payload = self.header_handler.decode_header(header)
            self.assertEqual(result,Generic_DoIP_NACK_codes.Unknown_payload_type,'Payload header should not be supported, expected NACK Unknown payload type')

    def test_decode_header_with_payload_size_bigger_than_processable(self):
        _header_bytes_with_big_payload_length = bytes.fromhex('02 fd 00 08 ff ff ff ff')
        length = self.header_handler.MAXIMUM_PROCESSABLE_LENGTH
        self.header_handler.MAXIMUM_PROCESSABLE_LENGTH = int(b'fffffffe',16)
        result, payload = self.header_handler.decode_header(_header_bytes_with_big_payload_length)
        self.header_handler.MAXIMUM_PROCESSABLE_LENGTH = length
        self.assertEqual(result,Generic_DoIP_NACK_codes.Message_too_large,'Expected NACK Message_too_large')

    def test_decode_header_with_correct_payload_length(self):
        _list_of_header_bytes_with_correct_payload_length = [   bytes.fromhex('02 fd 00 00 00 00 00 00'),
                                                                bytes.fromhex('02 fd 00 04 00 00 00 20') ]
        for header in _list_of_header_bytes_with_correct_payload_length:
            result, payload = self.header_handler.decode_header(header)
            self.assertNotEqual(result,Generic_DoIP_NACK_codes.Invalid_payload_length,'Did not expect NACK Invalid payload length')

    def test_decode_header_with_wrong_payload_length(self):
        _list_of_header_bytes_with_wrong_payload_length = [ bytes.fromhex('02 fd 00 00 00 00 00 02'),
                                                            bytes.fromhex('02 fd 00 04 00 00 00 02') ]
        for header in _list_of_header_bytes_with_wrong_payload_length:
            result, payload = self.header_handler.decode_header(header)
            self.assertEqual(result,Generic_DoIP_NACK_codes.Invalid_payload_length,'Excpected NACK Invalid payload length')

    
if __name__ == '__main__':
    unittest.main()