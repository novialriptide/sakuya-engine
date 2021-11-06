from Sakuya.errorhandler.error import *

class ObjectNotInWorld(Error):
    def __init__(self):
        self.message = "Object isn\'t in world"