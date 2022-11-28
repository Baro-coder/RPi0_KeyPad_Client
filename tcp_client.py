#!/usr/bin/python
# -- KeyPad_Client: tcp_client.py --

import socket


# *** class Request ***

class Request:
    def __init__(self, row : int, text : str) -> None:
        self.row = row
        self.text = text
        
    def __str__(self) -> str:
        return f'ROW={self.row}&TEXT={self.text}{TCP_Client.CLOSE_MSG}'


# -------------------------------------------------------------------------

# *** class TCP Client ***

class TCP_Client:
    CLOSE_MSG = '!SEQ'
    RESPONSE_SEQ = 'SEQ-NEXT'
    RESPONSE_SUCCESS = 'REQ-0'
    RESPONSE_FAILURE = 'REQ-1'
    
    def __init__(self, server_address : str, server_port : int, buffer_size : int, format : str) -> None:
        self.server_address = server_address
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.format = format
        
        
    def send(self, row : int, text : str):
        request = Request(row, text)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_address, self.server_port))
            
            s.sendall(str(request).encode(self.format))
            resp = s.recv(1024)
            
        
    