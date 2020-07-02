import socket
import Service_client
import threading
import Buffer
import GUII
HEADER_LENGTH = 10

HOST = "192.168.2.15" # Server's IP
DEVICE_HOST = "192.168.0.103"#"192.168.2.15"
PORT = 13000

class Client:
    def __init__(self):
        self.socket = None
        self.listen_socket = None
        self.buff_dict = {}
        self.message_list_dict = {}
        self.lock = threading.Lock()
        self.target = None
        self.listen_flag = True

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
        self.listen_socket.bind(("", 0))
        self.setPort()
        self.listen_thread = threading.Thread(target=self.listen_run, args=())
        self.listen_thread.start()

    def setPort(self):
        print('setPort')
        self.Send_message('setPort')
        host = self.ip
        port = self.listen_socket.getsockname()[1]

        self.Send_message(host)
        port = f"{port:<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(port)
        
    def requestPort(self, username):
        self.Send_message('requestPort')
        self.Send_message(username)
        response = self.Receive_message()['data']
        if response == 'Successed':
            host = self.Receive_message()['data']
            port = self.socket.recv(HEADER_LENGTH)
            port = int(port.decode('utf-8').strip())
            return (host, port)
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
        for username in self.buff_dict:
            self.buff_dict[username].assign('done', '')

        host = self.ip
        self.listen_flag = False
        if self.listen_socket is not None:
            port = self.listen_socket.getsockname()[1]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.close()

    def close_response(self):
        self.socket.close()

    def listen_run(self):
        self.listen_socket.listen()
        while self.listen_flag:
            print('accept1')
            conn, addr = self.listen_socket.accept()
            if self.listen_flag:
                buff = Buffer.Buffer(self.lock)
                message_list = GUII.Message_list(self.chatui.Message_box_frame)
                service = Service_client.Service_client(conn, buff, message_list, self.username, ip = self.ip)
                self.buff_dict[service.peer] = service.buffer
                if service.peer in self.message_list_dict:
                    service.message_list = self.message_list_dict[service.peer]
                else:
                    self.message_list_dict[service.peer] = service.message_list
                self.chatui.update()
                service.start()
            
        print('closed')

    def startChatTo(self, username):
        addr = self.requestPort(username)
        if addr is None:
            return False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        buff = Buffer.Buffer(self.lock)
        if username in self.message_list_dict:
            service = Service_client.Service_client(s, buff, self.message_list_dict[username], self.username, peer = username, ip = self.ip)
            self.buff_dict[username] = service.buffer 
        else:
            message_list = GUII.Message_list(self.chatui.Message_box_frame)
            service = Service_client.Service_client(s, buff, message_list, self.username, peer = username, ip = self.ip)
            self.buff_dict[username] = service.buffer
            self.message_list_dict[username] = service.message_list
        print(addr)
        service.connectTo(addr)
        service.start()
        self.chatui.update()
        return True

    def chatTo(self, message):
        if self.target is None:
            return
        username = self.target
        if username in self.buff_dict and self.buff_dict[username].status == True:
            self.buff_dict[username].assign('SendSMS', message)
            print('yet')
        else:
            check = self.startChatTo(username)
            if check:
                self.buff_dict[username].assign('SendSMS', message)
            else:
                self.chatui.update()

    def sendFileTo(self, filename):
        username = self.target
        if username in self.buff_dict and self.buff_dict[username].status == True:
            self.buff_dict[username].assign('SendFile', filename)
        else:
            check = self.startChatTo(username)
            if check:
                self.buff_dict[username].assign('SendFile', filename)
            else:
                print("Not friend")

    def run(self):
        self.loginui = GUII.LoginWindow(self, ('Helvetica', 13))
        self.loginui.run()
        
        self.chatui = GUII.ChatWindow(self, ('Helvetica', 13))
        self.chatui.run()

    def configIP(self, ip):
        self.ip = ip