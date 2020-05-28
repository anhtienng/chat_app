import socket
import Service_client
import threading
import Buffer
HEADER_LENGTH = 10

HOST = "127.0.0.1"
PORT = 5050

class Client:
    def __init__(self):
        self.socket = None
        self.listen_socket = None
        self.buff_dict = {}
        self.lock = threading.Lock()

    def Connect(self):
        #This method will connect client socket to server socket 
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        res = self.Receive_message()['data']
        if res == 'done':
            self.close_response()
            return False

        return True

    def Listen(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((HOST,0))
        self.setPort()
        self.listen_thread = threading.Thread(target=self.listen_run, args=())
        self.listen_thread.start()

    def setPort(self):
        print('setPort')
        self.Send_message('setPort')
        port = self.listen_socket.getsockname()[1]
        port = f"{port:<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(port)
        
    def requestPort(self, username):
        self.Send_message('requestPort')
        self.Send_message(username)
        response = self.Receive_message()['data']
        if response == 'Successed':
            port = self.socket.recv(HEADER_LENGTH)
            port = int(port.decode('utf-8').strip())
            return port
        else:
            return None

    def Receive_message(self):
        #This method is used to receive message from server
       
        message_header = self.socket.recv(HEADER_LENGTH)

        if not len(message_header):
            self.close()
            return {'header': None,'data': None}

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': self.socket.recv(message_length).decode('utf-8')}

    def Send_message(self, message):
        #This method is used to send message to server
        #Arg: message: a string object

        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(message_header + message)        

    def Register(self, username, password):
        #Register services
        
        self.Send_message("Register")
        self.Send_message(username)
        self.Send_message(password)

        message_recv = self.Receive_message()
        if message_recv['data'] == "Successed":
            self.username = username
            return True
        else:
            return False

    def Login(self, username, password):
        # Login 

        self.Send_message("Login")
        self.Send_message(username)
        self.Send_message(password)

        message_recv = self.Receive_message()
        if message_recv['data'] == "Successed":
            self.username = username
            return True
        else:
            return False

    def showFriend(self):
        self.Send_message("showFriend")
        response = self.Receive_message()['data']
        if response == "Successed":
            length = self.socket.recv(HEADER_LENGTH)
            length = int(length.decode('utf-8').strip())
            friendDict = {}
            for _ in range(length):
                username = self.Receive_message()['data']
                status = self.Receive_message()['data']
                friendDict[username] = status
            return friendDict

        else:
            return None

    def showFriendRequest(self):
        self.Send_message("showFriendRequest")
        response = self.Receive_message()['data']
        if response == "Successed":
            length = self.socket.recv(HEADER_LENGTH)
            length = int(length.decode('utf-8').strip())
            requestList = []
            for _ in range(length):
                username = self.Receive_message()['data']
                #status = self.Receive_message()['data']
                requestList.append(username)
            return requestList

        else:
            return None
            
    def acceptFriendRequest(self, username2):
        self.Send_message("acceptFriendRequest")
        self.Send_message(username2)
        response = self.Receive_message()['data']
        if response == "Successed":
            return True
        else:
            return False
        
    def rejectFriendRequest(self, username2):
        self.Send_message("rejectFriendRequest")
        self.Send_message(username2)
        response = self.Receive_message()['data']
        if response == "Successed":
            return True
        else:
            return False

    def addFriend(self, username2):
        self.Send_message("addFriend")
        self.Send_message(username2)
        response = self.Receive_message()['data']
        if response == "Successed":
            return True
        else:
            return False

    def shutdown(self):
        self.Send_message("shutdown")

    def close(self):
        self.Send_message('done')
        self.socket.close()

    def close_response(self):
        self.socket.close()

    def listen_run(self):
        self.listen_socket.listen()
        while True:
            conn, addr = self.listen_socket.accept()
            buff = Buffer.Buffer()
            service = Service_client.Service_client(conn, buff, self.lock, self.username)
            self.buff_dict[service.peer] = service.buffer
            service.start()

    def startChatTo(self, username):
        port = self.requestPort(username)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        buff = Buffer.Buffer()
        service = Service_client.Service_client(s, buff, self.lock, self.username, peer = username)
        self.buff_dict[username] = service.buffer
        service.connectTo(port)
        service.start()

    def chatTo(self, username, message):
        print(message)
        self.buff_dict[username].assign(message)


