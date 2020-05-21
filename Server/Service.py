import Server
import User

HEADER_LENGTH = 10

class Service:
    def __init__(self, socket, addr, database, lock):
        self.socket = socket
        self.addr = addr
        self.database = database
        self.lock = lock
        self.username = None
        
    def Receive_message(self):
        message_header = self.socket.recv(HEADER_LENGTH)

        if not len(message_header):
            self.close()
            return {'header': None,'data': None}

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': self.socket.recv(message_length).decode('utf-8')}

    def Send_message(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(message_header + message)

    def Register(self):
        username = self.Receive_message()['data']
        password = self.Receive_message()['data']

        print(username)
        print(password)
        if username is None or password is None:
            self.Send_message('Failed')
            return

        if self.database.addUser(username, password):
            self.Send_message('Successed')
            self.username = username
            self.password = password
            self.database.online(username)
            print("Welcome", username)
        else:
            self.Send_message('Failed')

    def Login(self):
        username = self.Receive_message()['data']
        password = self.Receive_message()['data']   

        if username is None or password is None:
            self.Send_message('Failed')
            return

        if self.database.Login(username, password):
            self.Send_message('Successed')
            self.username = username
            self.password = password
            self.database.online(username)
            print("Welcome", username)

        else:
            self.Send_message('Failed')

    def showFriend(self):
        friendList = self.database.showFriend(self.username)
        if friendList == None:
            self.Send_message('Failed')

        else:
            self.Send_message('Successed')
            length = len(friendList)
            length = f"{length:<{HEADER_LENGTH}}".encode('utf-8')
            self.socket.send(length)

            for key, val in friendList:
                self.Send_message(key)
                if val:
                    self.Send_message("Online")
                else:
                    self.Send_message("Offline")

    def showFriendRequest(self):
        requestList = self.database.showFriendRequest(self.username)
        if requestList == None:
            self.Send_message('Failed')

        else:
            self.Send_message('Successed')
            length = len(requestList)
            length = f"{length:<{HEADER_LENGTH}}".encode('utf-8')
            self.socket.send(length)

            for username in requestList:
                self.Send_message(username)

    def addFriend(self):
        username = self.Receive_message()['data']
        if self.database.addFriend(self.username, username):
            self.Send_message("Successed")
        else:
            self.Send_message("Failed")

    def acceptFriendRequest(self):
        username = self.Receive_message()['data']
        if self.database.acceptFriendRequest(self.username, username):
            self.Send_message("Successed")
        else:
            self.Send_message("Failed")

    def rejectFriendRequest(self):
        username = self.Receive_message()['data']
        if self.database.rejectFriendRequest(self.username, username):
            self.Send_message("Successed")
        else:
            self.Send_message("Failed")

    def __call__(self):
        while True:
            cmd = self.Receive_message()['data']
            if cmd == 'done':
                self.close_response()
                break
            else:
                self.Send_message(cmd)
            #elif... 

    def accept(self):
        self.Send_message('accept')

    def close(self):
        self.Send_message('done')
        self.socket.close()

    def close_response(self):
        self.database.offline(self.username)
        self.socket.close()

    def verify(self):
        while True:
            cmd = self.Receive_message()['data']
            if cmd == 'Register':
                self.Register()
                break
            elif cmd == 'Login':
                self.Login()
                break
            #elif... 
            
