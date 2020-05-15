import sys
import socket
import selectors
import traceback

class Server:
    def __init__(self, socket, address):
        self.socket = socket
        self.port = 5050
        self.ip = address
        self.numThread = 10
        self.userList = []
        self.serviceList = []



