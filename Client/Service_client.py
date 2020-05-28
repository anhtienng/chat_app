import threading
import os

HEADER_LENGTH = 10
HOST = '127.0.0.1'
Destination = 'download/'

class Service_client(threading.Thread):
    def __init__(self, socket, buff, username, peer = None):
        super(Service_client, self).__init__()
        self.socket = socket
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

    def Send_message(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(message_header + message)

    def Receive_byte(self):
        data_header = self.socket.recv(HEADER_LENGTH)

        if not len(data_header):
            return {'header': None, 'data': None}

        # Convert header to int value
        data_length = int(data_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': data_header, 'data': self.socket.recv(data_length)}

    def Send_byte(self, data):
        data_header = f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(data_header + data)    

    def connectTo(self, host, port):
        self.socket.connect((host,port))

    def Send_SMS(self, message):
        self.Send_message("sendSMS")
        self.Send_message(message)

    def Receive_SMS(self):
        mess = self.Receive_message()['data']
        return mess

    def Send_File(self, filename):
        if os.path.exists(filename):
            self.Send_message("sendFile")
            self.Send_message(filename)
            
            with open(filename, "rb") as in_file:
                while True:
                    data = in_file.read(256)
                    if len(data) == 0:
                        self.Send_message('EOF')
                        break
                    else:
                        self.Send_message('Data')
                        self.Send_byte(data)
            return True
        else:
            print('No such file')
            return False


    def Receive_File(self):
        filename = Destination + self.Receive_message()['data']
        with open(filename, "wb") as out_file:
            while True:
                response = self.Receive_message()['data']
                if response == 'EOF':
                    break
                elif response == 'Data':
                    data = self.Receive_byte()['data']
                    out_file.write(data)
                    
            
    def run(self):
        while True:
            if len(self.buffer) == 0:
                self.Send_message("Idle")
                cmd = self.Receive_message()['data']
                if cmd == 'Idle':
                    continue

                # send username to peer
                elif cmd == 'Verify':
                    self.on_verify()

                #receive sms from peer
                elif cmd == 'sendSMS':
                    mess = self.Receive_SMS()
                    print(mess)

                elif cmd == 'sendFile':
                    self.Receive_File()

            else:
                cmd, content = self.buffer.string()
                if cmd == 'SendSMS':
                    self.Send_SMS(content)

                elif cmd == 'SendFile':
                    self.Send_File(content)

                self.buffer.assign('', '')

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
