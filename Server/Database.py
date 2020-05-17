import User

class Database:
    def __init__(self):
        self.userDict = {}

    def Username_Availability(self, username):
        if username in self.userDict:
            return False
        else:
            return True

    def addUser(self, username, password):
        if not self.Username_Availability(username):
            return False
        self.userDict[username] = User.User(username, password)
        return True


