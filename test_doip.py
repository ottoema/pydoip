#!/usr/bin/python3

from doip.handlers import DoIP_Handler, DoIP_Header_Handler
from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes
import unittest

class Test_DoIP_Header_Handler_(unittest.TestCase):
    def setUp(self):
        self.header_handler = DoIP_Header_Handler(DoIP_protocol_version.DoIPISO1340022012,
        [DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message])

        # test_decode_header_with_incorrect_pattern_format:
        self._header_bytes_with_incorrect_pattern_format = bytes.fromhex('02 12 00 04 00 00 00 20')

        # test_decode_header_with_correct_pattern_format: 
        self._header_bytes_with_correct_pattern_format = bytes.fromhex('02 fd 00 04 00 00 00 20')
        self._correct_header = DoIP_Header(DoIP_protocol_version.DoIPISO1340022012,-3,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,32)

        # test_decode_header_with_known_payload_type:
        self._list_of_header_bytes_with_correct_payload_type = [bytes.fromhex('02 fd 00 00 00 00 00 00'),
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

        # test_decode_header_with_unknown_payload_type:
        self._list_of_header_bytes_with_incorrect_payload_type = [  bytes.fromhex('02 fd 00 09 00 00 00 00'),
                                                                    bytes.fromhex('02 fd 40 00 00 00 00 00'),
                                                                    bytes.fromhex('02 fd 40 05 00 00 00 00'),
                                                                    bytes.fromhex('02 fd 80 00 00 00 00 00'),
                                                                    bytes.fromhex('02 fd 80 04 00 00 00 00'),
                                                                    bytes.fromhex('02 fd EF FF 00 00 00 00') ]

        # test_decode_header_with_payload_size_bigger_than_processable:
        self._header_bytes_with_big_payload_length = bytes.fromhex('02 fd 00 08 ff ff ff ff')

        # test_decode_header_with_correct_payload_length:
        self._list_of_header_bytes_with_correct_payload_length = [  bytes.fromhex('02 fd 00 00 00 00 00 00'),
                                                                    bytes.fromhex('02 fd 00 04 00 00 00 20') ]
        
        # test_decode_header_with_wrong_payload_length:
        self._list_of_header_bytes_with_wrong_payload_length = [    bytes.fromhex('02 fd 00 00 00 00 00 02'),
                                                                    bytes.fromhex('02 fd 00 04 00 00 00 02') ]

    def test_decode_header_with_incorrect_pattern_format(self):
        result, payload = self.header_handler.decode_header(self._header_bytes_with_incorrect_pattern_format)
        self.assertEqual(result,Generic_DoIP_NACK_codes.Incorrect_pattern_format,"Wrong decoding of header:")
        
    def test_decode_header_with_correct_pattern_format(self):
        result, payload = self.header_handler.decode_header(self._header_bytes_with_correct_pattern_format)
        self.assertTrue(result == self._correct_header,'Wrong decoding of header')

    def test_decode_header_with_known_payload_type(self):
        for header in self._list_of_header_bytes_with_correct_payload_type:
            result, payload = self.header_handler.decode_header(header)
            self.assertNotEqual(result,Generic_DoIP_NACK_codes.Unknown_payload_type,'Payload header should be supported but received NACK Unknown payload type')

    def test_decode_header_with_unknown_payload_type(self):
        for header in self._list_of_header_bytes_with_incorrect_payload_type:
            result, payload = self.header_handler.decode_header(header)
            self.assertEqual(result,Generic_DoIP_NACK_codes.Unknown_payload_type,'Payload header should not be supported, expected NACK Unknown payload type')

    def test_decode_header_with_payload_size_bigger_than_processable(self):
        length = self.header_handler.MAXIMUM_PROCESSABLE_LENGTH
        self.header_handler.MAXIMUM_PROCESSABLE_LENGTH = int(b'fffffffe',16)
        result, payload = self.header_handler.decode_header(self._header_bytes_with_big_payload_length)
        self.header_handler.MAXIMUM_PROCESSABLE_LENGTH = length
        self.assertEqual(result,Generic_DoIP_NACK_codes.Message_too_large,'Expected NACK Message_too_large')

    def test_decode_header_with_wrong_payload_length(self):
        for header in self._list_of_header_bytes_with_correct_payload_length:
            result, payload = self.header_handler.decode_header(header)
            self.assertNotEqual(result,Generic_DoIP_NACK_codes.Invalid_payload_length,'Did not expect NACK Invalid payload length')

    def test_decode_header_with_wrong_payload_length(self):
        for header in self._list_of_header_bytes_with_wrong_payload_length:
            result, payload = self.header_handler.decode_header(header)
            self.assertEqual(result,Generic_DoIP_NACK_codes.Invalid_payload_length,'Excpected NACK Invalid payload length')

    
if __name__ == '__main__':
    unittest.main()