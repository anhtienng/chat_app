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
            return None,None

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': self.socket.recv(message_length).decode('utf-8')}
    def Send_message(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(message_header + message)

    def Register(self):
        self.Send_message('Input username: ')
        username = self.Receive_message()['data']
        self.Send_message('Input password: ')
        password = self.Receive_message()['data']

        if username is None or password is None:
            self.Send_message('Failed')
            return

        if self.database.addUser(username, password):
            self.Send_message('Successed')
            self.username = username
            self.password = password
            print("Welcome", username)
        else:
            self.Send_message('Failed')

    def verify(self):
        while True:
            cmd = self.socket.recv(HEADER_LENGTH)
            if cmd.decode('utf-8') == 'Register':
                self.Register()
            #elif cmd.decode('utf-8') == 'Login':
            #    self.Login()
            elif cmd.decode('utf-8') == 'Exit':
                break
            
