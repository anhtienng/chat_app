import Server
import User

class Service:
    def __init__(self, user, socket):
        self.user = user
        self.socket = socket

    def register(self, server, name, password, ip):
        for user in server.userList:
            if user.userName == name:
                return False
        newUser = User(address=ip, name=name, password=password)
        server.userList.append(newUser)
        return True

    def login(self, server, name, password, ip):
        for user in server.userList:
            if user.userName == name and user.password == password:
                user.status = True
                user.ip = ip
                return True
        return False

    def addFriend(self, server, sender, receiver):  # userName of sender and receiver
        for user in server.userList:
            if user.userName == receiver:  # if exist receiver
                if receiver in sender.friendList:  # if be friend already, return false
                    return False
                receiver.friendRequest.append(sender)
                return True

