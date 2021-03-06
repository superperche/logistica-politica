#!/usr/bin/env python3

from pyrebase import *
import config

class LogiticaPolitica:
    """
    LogiticaPolitica is a database of people, their twitter handles, their party affiliations and their emotional
    leanings.
    """
    def __init__(self):
        self.config = config.firebaseStuff
        self.firebase = initialize_app(self.config)
        self.db = self.firebase.database()

    # start takes a LogiticaPolitical and starts a db stream to dynamically change and access the database.
    # start: LogiticaPolitica -> None
    # Effects: stream started with db to access and edit.
    def start(self):
        self.stream = self.db.stream(self.streamHandler)

    # streamHandler takes a pyredb and a dictionary called post in order to mutate pyredb with the values of the dict.
    # streamHandler: pyredb DictOf(Str: Num or Str: Str) -> None
    # Effects: mutate pyredb
    def streamHandler(self, post):
        event = post["event"]
        key = post["path"]
        value = post["data"]

        if event == "put":
            print(key, ":", value)

    # addUser takes a pyredb, two strings called handle and uName, and two number dictionaries called moods and parties,
    #   in order to mutate pyredb by adding a new user with the details provided into the db.
    # addUser: pyredb Str Str DictOf(num) DictOf(num) -> None
    # Effects: Mutates pyredb
    def addUser(self, handle, uName, moods, parties):
        dataDict = dict(moods, **parties)
        dataDict["name"] = uName
        self.db.child(handle).set(dataDict)

    # getAll takes a pyredb and returns a dictionary containing values for each correlation between political parties
    #   and emotion for each entry in the database.
    # getAll: pyredb -> Dict
    def getAll(self):
        all_users = self.db.child("/").get()
        masterList = []
        if all_users.each() is not None:
            for user in all_users.each():
                mDict = {}
                mDict["handle"] = user.key()
                mDict["Conservative"] = (user.val())["Conservative"]
                mDict["Green"] = (user.val())["Green"]
                mDict["Liberal"] = (user.val())["Liberal"]
                mDict["Libertarian"] = (user.val())["Libertarian"]
                mDict["fear"] = (user.val())["fear"]
                mDict["joy"] = (user.val())["joy"]
                mDict["surprise"] = (user.val())["surprise"]
                mDict["anger"] = (user.val())["anger"]
                mDict["sadness"] = (user.val())["sadness"]
                mDict["name"] = (user.val())["name"]
                masterList.append(mDict)
            print(masterList)
            return masterList
        else:
            return []

if __name__ == "__main__":
    test = LogiticaPolitica()
    test.start()
    test.getAll()
