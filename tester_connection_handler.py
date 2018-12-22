import socket

class Tester_Connection_Handler(object):
    def __init__(self,port,transport_protocol):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', port)
        print('starting up on {} port {}'.format(*server_address))
        self.socket.bind(server_address)

    def receive(self):
        while True:
            print('\nwaiting to receive message')
            data, address = self.socket.recvfrom(4096)

            print('received {} bytes from {}'.format(
                len(data), address))
            print(data)