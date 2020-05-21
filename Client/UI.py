import Client
from getpass import getpass

class UI:
    def __init__(self, client):
        self.state = 0
        self.client = client

    def Run(self):
        while True:
            if self.state == 0:
                cmd = input("Register/Login??? ")
                if cmd == "Register":
                    self.client.Connect()
                    username = input("Username: ")
                    password = getpass("Password: ")
                    if not self.client.Register(username, password):
                        self.client.close()
                    else:
                        self.state = 1
                elif cmd == "Login":
                    self.client.Connect()
                    username = input("Username: ")
                    password = getpass("Password: ")
                    if not self.client.Login(username, password):
                        self.client.close()
                    else:
                        self.state = 1

            elif self.state == 1:
                cmd = input("Command: ")
                if cmd == "done":
                    self.client.close()
                    self.state = 2

            elif self.state == 2:
                break
