import User
import pickle
import threading


class Database:
    def __init__(self):
        self.userDict = {}              # Key: username --- Val: <User>
                                        # ex: userDict['tienanh'] = User tienanh

        self.userFriend = {}            # Key: username -- Val: list contains all names of friends of username
                                        # ex: userFriend['tienanh'] = ['khoi', 'huy']

        self.userFriendRequest = {}     # Key: username -- Val: list contains all names of friend-requests of username
                                        # ex: userFriendRequest['tienanh'] = ['khoi1', 'huy1']
        self.lock = threading.Lock()
        #self.load()

    def save(self):
        # TODO
        # save data to file
        with open("Data/userDict.pkl", "wb") as f1:
            pickle.dump(self.userDict, f1, pickle.HIGHEST_PROTOCOL)
        with open("Data/userFriend.pkl", "wb") as f2:
            pickle.dump(self.userFriend, f2, pickle.HIGHEST_PROTOCOL)
        with open("Data/userFriendRequest.pkl", "wb") as f3:
            pickle.dump(self.userFriendRequest, f3, pickle.HIGHEST_PROTOCOL)

    def load(self):
        # TODO
        # retreive data from file
        with open('Data/userDict.pkl', 'rb') as f1:
            self.userDict = pickle.load(f1)
        with open('Data/userFriend.pkl', 'rb') as f2:
            self.userFriend = pickle.load(f2)
        with open('Data/userFriendRequest.pkl', 'rb') as f3:
            self.userFriendRequest = pickle.load(f3)

    def isRegistered(self, username):
        if username in self.userDict:
            return True
        else:
            return False

    def getStatus (self, username):
        if not self.isRegistered(username):
            return None
        return self.userDict[username].status

    def addUser(self, username, password):
        # Add new user
        if self.isRegistered(username):
            return False
        self.lock.acquire()
        self.userDict[username] = User.User(username, password)
        self.userFriend[username] = []
        self.userFriendRequest[username] = []
        self.lock.release()
        return True

    def addFriend(self, username1, username2):
        # TODO
        # Args: username1:sender, username2: receiver
        # Add username1 into friendRequest of username2
        if (not self.isRegistered(username1)) or (not self.isRegistered(username2)):  # check registration
            return False
        listFriend = self.userFriend[username2]
        listRequest = self.userFriendRequest[username2]
        if username1 in listFriend or username1 in listRequest or username1 == username2:
            return False
        else:
            self.lock.acquire()
            listRequest.append(username1)
            self.lock.release()
            print(self.userFriendRequest[username2])
            return True

    def showFriend(self, username):
        # TODO
        # Args: username
        # return: a ordered dict {friendName: status}, online first
        if not self.isRegistered(username):
            return None
        friendList = self.userFriend[username]
        friendDict = {}
        for friend in friendList:
            friendDict[friend] = self.getStatus(friend)
        #friendDict = {k: v for k, v in sorted(friendDict.items(), key=lambda item: item[1], reverse=True)}
        return friendDict

    def showFriendRequest(self, username):
        # TODO
        # Args: username
        # return: an unordered list of friend requests of user with name username
        if not self.isRegistered(username):
            return None
        else:
            return self.userFriendRequest[username]

    def acceptFriendRequest(self, username2, username1):
        # TODO
        # Args: username1, username2
        # Accept friend request of username1 for username2. Adding them in their friendlist
        if (not self.isRegistered(username1)) or (not self.isRegistered(username2)):
            return False
        listFriend1 = self.userFriend[username1]
        listFriend2 = self.userFriend[username2]
        listRequest2 = self.userFriendRequest[username2]
        if (username1 in listFriend2) or (username1 not in listRequest2) or (username1 == username2):
            return False
        else:
            self.lock.acquire()
            listFriend1.append(username2)
            listFriend2.append(username1)
            listRequest2.remove(username1)
            self.lock.release()
            return True

    def rejectFriendRequest(self, username2, username1):
        # TODO
        # Args: username1, username2
        # Reject friend request of username1 for username2.
        if (not self.isRegistered(username1)) or (not self.isRegistered(username2)):
            return False
        listFriend1 = self.userFriend[username1]
        listFriend2 = self.userFriend[username2]
        listRequest2 = self.userFriendRequest[username2]
        if username1 in listFriend2 or username1 not in listRequest2 or username1 == username2:
            return False
        else:
            self.lock.acquire()
            listRequest2.remove(username1)
            self.lock.release()
            return True

    def Login(self, username, password):
        if not self.isRegistered(username):
            return False
        
        if self.userDict[username].password != password:
            return Fasle

        return True

    def online(self, username):
        if not self.isRegistered(username):
            return False
        
        else:
            self.userDict[username].status = True
            return True

    def offline(self, username):
        if not self.isRegistered(username):
            return False

        else:
            self.userDict[username].status = False
            return True
