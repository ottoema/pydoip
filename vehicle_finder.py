#!/usr/bin/python3

from doip.doip import DoIP_Header
from doip.handlers import DoIP_Handler

class Vehicle_Finder(object):

    def __init__(self):
        self.doip_handler = DoIP_Handler(tester=True)

    def get_available_vehicles(self):
        self.doip_handler.get_vehicle_announcements()