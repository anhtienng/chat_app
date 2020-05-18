import User

class Database:
    def __init__(self):
        self.userDict = {} # Key: username --- Val: class User
        self.userFriend = {} # Key: username -- Val: Friendlist
        self.userFriendRequest = {} # Key: username -- Val: Friend request list
        self.load()

    def save(self):
        # TODO
        # save data to file
        pass

    def load(self):
        # TODO
        # retreive data from file 
        pass

    def Username_Availability(self, username):
        if username in self.userDict:
            return False
        else:
            return True

    def addUser(self, username, password):
        #Add new user

        if not self.Username_Availability(username):
            return False
        self.userDict[username] = User.User(username, password)
        self.userFriend[username] = {}
        return True

    def addFriend(self, username1, username2):
        # TODO
        # Args: username1, username2
        # Send a friend request from user whose name is username1 to user whose name is username2
        pass

    def showFriendList(self, username):
        # TODO
        # Args: username
        # return: an ordered friendlist of user whose name is username
        pass 

    def showFriendRequest(self, username):
        # TODO
        # Args: username
        # return: an unordered list of friend requests of user with name username
        pass

    def acceptFriendRequest(self, username1, username2):
        # TODO
        # Args: username1, username2
        # Accept friend request of username1 for username2. Adding them in their friendlist
        pass






