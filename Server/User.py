import sys
import socket
import selectors
import traceback

class User:
    def __init__(self, address, name, password):
        self.port = 5050
        self.ip = address
        self.friendList = []  # store userName of friend
        self.userName = name
        self.password = password
        self.status = False
        self.friendRequest = []



