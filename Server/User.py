import sys
import socket
import selectors
import traceback

class User:
    def __init__(self, username, password):
        self.userName = username
        self.password = password
        self.status = False
        self.friendRequest = []
        self.friendList = []  # store userName of friend



