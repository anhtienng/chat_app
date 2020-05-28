import threading

HEADER_LENGTH = 10
HOST = '127.0.0.1'

class Service_client(threading.Thread):
    def __init__(self, socket, buff, lock, username, peer = None):
        super(Service_client, self).__init__()
        self.socket = socket
        self.lock = lock
        self.username = username
        if peer is not None:
            self.peer = peer
        else:
            self.peer = self.verify()
        self.buffer = buff

    def Receive_message(self):
        message_header = self.socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return {'header': None, 'data': None}

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': self.socket.recv(message_length).decode('utf-8')}

    def connectTo(self, port):
        self.socket.connect((HOST,port))

    def Send_message(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(message_header + message)

    def Send_SMS(self, message):
        self.Send_message("sendSMS")
        self.Send_message(message)

    def Receive_SMS(self):
        mess = self.Receive_message()['data']
        return mess

    def sendFile(self):
        file = self.Receive_message()['data']
        f = open('file/' + file, 'wb')
        len_pieces = int(self.Receive_message()['data'])  # number of pieces
        print("len pieces ", len_pieces)
        for i in range(len_pieces):
            data = self.socket.recv(1024)
            f.write(data)
        f.close()
        print("sending successful")

    def run(self):
        while True:
            if len(self.buffer) == 0:
                self.Send_message("Idle")
                cmd = self.Receive_message()['data']
                if cmd == 'Idle':
                    continue
                elif cmd == 'Verify':
                    self.on_verify()
                elif cmd == 'sendSMS':
                    mess = self.Receive_SMS()
                    print(mess)
            else:
                self.Send_SMS(self.buffer.string())
                self.lock.acquire()
                self.buffer.assign('')
                self.lock.release()

    def accept(self):
        self.Send_message('accept')

    def close(self):
        self.Send_message('done')
        self.socket.close()

    def close_response(self):
        self.database.offline(self.username)
        self.socket.close()

    def verify(self):
        self.Send_message('Verify')
        data = 'Idle'
        while data == 'Idle':
            data = self.Receive_message()['data']
        print(data)
        return data

    def on_verify(self):
        self.Send_message(self.username)
