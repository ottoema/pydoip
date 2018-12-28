#!/usr/bin/python3

from doip.handlers import DoIP_Handler, DoIP_Header_Handler
from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes
import unittest

class Test_DoIP_Header_Handler_(unittest.TestCase):
    def setUp(self):
        self.header_handler = DoIP_Header_Handler(DoIP_protocol_version.DoIPISO1340022012,
        [DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message])

        # test_decode_header_with_incorrect_pattern_format:
        self._header_with_incorrect_pattern_format = bytes.fromhex('02 12 00 04 00 00 00 00')

        # test_decode_header_with_correct_pattern_format: 
        self._header_with_correct_pattern_format = bytes.fromhex('02 fd 00 04 00 00 00 00')
        self._correct_header = DoIP_Header(DoIP_protocol_version.DoIPISO1340022012,-3,DoIP_payload_type.Vehicle_announcement_message__vehicle_identification_response_message,0,0)

    def test_decode_header_with_incorrect_pattern_format(self):
        result = self.header_handler.decode_header(self._header_with_incorrect_pattern_format)

        self.assertEqual(result,Generic_DoIP_NACK_codes.Incorrect_pattern_format,'Wrong decoding of header')
        
    def test_decode_header_with_correct_pattern_format(self):
        result = self.header_handler.decode_header(self._header_with_correct_pattern_format)

        self.assertTrue(result == self._correct_header,'Wrong decoding of header')

    
if __name__ == '__main__':
    unittest.main()