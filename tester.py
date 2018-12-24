#!/usr/bin/python3

from doip.doip import DoIP_Protocol  
from tester_connection_handler import Tester_Connection_Handler

class Tester(object):

    def __init__(self):
        self.protocol =  DoIP_Protocol()
        self.connection = Tester_Connection_Handler(self.protocol.UDP_DISCOVERY)
        self.connection.receive()


def main():
    tester = Tester()
    print('Assuming DoIP server is running...')


if __name__ == "__main__": 
    main()


