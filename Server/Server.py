import socket
import threading
import Database
import Service

HEADER_LENGTH = 10

class Server:
    def __init__(self, socket, numthread = 10):
        self.socket = socket 
        self.numthread = numthread
        self.database = Database.Database()
        self.lock = threading.Lock()
        self.serviceList = {}
        self.shutdown = False
        self.admin_socket = None
        self.admin_addr = None

    def Listen(self):
        #Start listen 

        self.socket.listen()

    def Run(self):
        self.Listen()
        
        while not self.shutdown:
            conn, addr = self.socket.accept()
            print("Connected by: ", addr)
            service = Service.Service(conn, addr, self.database, self.lock)
            thread = threading.Thread(target=self.Verify_thread, args=(service,))
            thread.start()
        
        self.socket.close()

    def Verify_thread(self, service):
        #Start thread
        #Args: Service object
        service.verify()
        username = service.username
        if username == 'admin':
            self.admin_socket = service.socket
            self.addr = service.addr
            self.Administration()
        elif username is not None:
            self.lock.acquire()
            if len(serviceList) < self.numthread:
                self.serviceList[username] = service
            else:
                return
            self.lock.release()

            service()
            service.shut_down()

            self.lock.acquire()
            del self.serviceList[username]
            self.lock.release()

    def Administration(self):
        while True:
            command = self.admin_socket.recv(HEADER_LENGTH)
            command = command.decode('utf-8')
            if command == 'Shutdown':
                self.lock.acquire()
                self.shutdown = True
                self.lock.release()


