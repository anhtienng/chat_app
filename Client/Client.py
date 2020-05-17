HEADER_LENGTH = 10

HOST = "127.0.0.1"
PORT = 5050

class Client:
    def __init__(self, socket):
        self.socket = socket

    def Connect(self):
        self.socket.connect((HOST, PORT))
        
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
        message_recv = self.Receive_message()
        message_send = input(message_recv['data'])

        self.Send_message(message_send)

        message_recv = self.Receive_message()
        message_send = input(message_recv['data'])

        self.Send_message(message_send)

        message_recv = self.Receive_message()
        print(message_recv['data'])

    def Run(self):
        self.Connect()
        while True:
            self.Send_message('Register')
            self.Register()

