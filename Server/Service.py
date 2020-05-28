import Server
import User
import threading

HEADER_LENGTH = 10

class Service:
    def __init__(self, socket, addr, database, lock):
        self.socket = socket
        self.addr = addr
        self.database = database
        self.lock = threading.Lock()
        self.username = None
        
    def Receive_message(self):
        message_header = self.socket.recv(HEADER_LENGTH)

        if not len(message_header):
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
        friendDict = self.database.showFriend(self.username)
        if friendDict == None:
            self.Send_message('Failed')

        else:
            self.Send_message('Successed')
            length = len(friendDict)
            length = f"{length:<{HEADER_LENGTH}}".encode('utf-8')
            self.socket.send(length)
            for key, val in friendDict.items():
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

    def setPort(self):
        print('ok')
        port = self.socket.recv(HEADER_LENGTH)
        self.listen_port = int(port.decode('utf-8').strip())
        print(self.listen_port)
        self.database.setPort(self.username, self.listen_port)

    def requestPort(self):
        username = self.Receive_message()['data']
        print(username)
        port = self.database.port_dict[username]
        if port is None:
            self.Send_message('Failed')
        else:
            self.Send_message('Successed')
            port = f"{port:<{HEADER_LENGTH}}".encode('utf-8')
            self.socket.send(port)

    def __call__(self):
        while True:
            cmd = self.Receive_message()['data']
            if cmd == 'done':
                self.lock.acquire()
                self.close_response()
                self.lock.release()
                break
            elif cmd == 'addFriend':
                self.lock.acquire()
                self.addFriend()
                self.lock.release()
            elif cmd == 'acceptFriendRequest':
                self.lock.acquire()
                self.acceptFriendRequest()
                self.lock.release()
            elif cmd == 'rejectFriendRequest':
                self.lock.acquire()
                self.rejectFriendRequest()
                self.lock.release()
            elif cmd == 'showFriendRequest':
                self.lock.acquire()
                self.showFriendRequest()
                self.lock.release()
            elif cmd == 'showFriend':
                self.lock.acquire()
                self.showFriend()
                self.lock.release()
            elif cmd == 'setPort':
                self.lock.acquire()
                self.setPort()
                self.lock.release()
            elif cmd == 'requestPort':
                self.lock.acquire()
                self.requestPort()
                self.lock.release()
            elif cmd == 'shutdown':
                if self.username == 'admin':
                    return True

    def accept(self):
        self.Send_message('accept')

    def close(self):
        self.database.offine(self.username)
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
            
