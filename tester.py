#!/usr/bin/python3

from doip.doip import DoIP_Protocol  
from vehicle_finder import Vehicle_Finder

class Tester(object):

    def __init__(self):
        self.protocol =  DoIP_Protocol()
        self.vehicle_finder = Vehicle_Finder()
        

    def start(self):
        
        #TODO:
        # Get list of available vehicles from this method:
        self.vehicle_finder.get_available_vehicles()
        # Present list of vehicle..

def main():
    tester = Tester()
    tester.start()

if __name__ == "__main__": 
    main()


