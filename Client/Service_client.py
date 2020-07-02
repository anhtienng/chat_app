import threading
import socket
import os

HEADER_LENGTH = 10
HOST = "192.168.2.15"
DEVICE_HOST = '192.168.0.103'
Destination = 'download/'


class Service_client(threading.Thread):
    def __init__(self, socket, buff, message_list, username, peer = None, ip = ''):
        super(Service_client, self).__init__()
        self.socket = socket
        self.username = username
        if peer is not None:
            self.peer = peer
        else:
            self.peer = self.verify()
        self.buffer = buff
        self.message_list = message_list
        self.ip = ip

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

    def connectTo(self, addr):
        self.socket.connect(addr)

    def Send_SMS(self, message):
        self.Send_message("sendSMS")
        self.Send_message(message)
        self.message_list.write('Me: ' + message + '\n')

    def Receive_SMS(self):
        mess = self.Receive_message()['data']
        self.message_list.write(self.peer + ': ' + mess + '\n')
        return mess

    def Send_File(self, filename):
        if os.path.exists(filename):
            self.Send_message("sendFile")
            self.Send_message(filename)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            host = self.ip
            port = s.getsockname()[1]
            s.listen()
            self.Send_message(host)
            port = f"{port:<{HEADER_LENGTH}}".encode('utf-8')
            self.socket.send(port)
            conn, addr = s.accept()
            thread = threading.Thread(target=self.Send_File_thread, args=(filename,conn))
            thread.start()
        else:
            print('No such file')
            return False

    def Receive_File(self):
        filename = self.Receive_message()['data']
        filename = filename.split('/')[-1]
        filename = Destination + filename
        host = self.Receive_message()['data']
        port = self.socket.recv(HEADER_LENGTH)
        port = int(port.decode('utf-8').strip())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(host)
        print(port)
        s.connect((host,port))
        
        
        
        thread = threading.Thread(target=self.Receive_File_thread, args=(filename,s))
        thread.start()

    def Send_File_thread(self, filename, conn):
        with open(filename, "rb") as in_file:
            while True:
                data = in_file.read(2048)
                if not data:
                    break
                conn.send(data)
        conn.close()

    def Receive_File_thread(self, filename, conn):
        with open(filename, "wb") as out_file:
            while True:
                print('reading...')
                data = conn.recv(1024)
                if not data:
                    break
                out_file.write(data)
        print('readed')
        conn.close()


    def run(self):
        while True:
            if len(self.buffer) == 0:
                try:
                    self.Send_message("Idle")
                except:
                    self.close_response()
                    print('close not safe')
                    break

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

                elif cmd == 'done':
                    self.close_response()
                    print('close')
                    break

            else:
                cmd, content = self.buffer.string()
                if cmd == 'SendSMS':
                    self.Send_SMS(content)

                elif cmd == 'SendFile':
                    self.Send_File(content)

                elif cmd == 'done':
                    self.close()
                    print('close')
                    break

                self.buffer.assign('', '')
        

        self.buffer.off()
        
    def accept(self):
        self.Send_message('accept')

    def close(self):
        self.Send_message('done')
        data = self.socket.recv(1024)
        while data:
            data = self.socket.recv(1024)
        self.socket.close()

    def close_response(self):
        self.message_list.write(self.peer + ' is offline! \n')
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
