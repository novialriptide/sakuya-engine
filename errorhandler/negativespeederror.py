from Sakuya.errorhandler.error import *

class NegativeSpeedError(Error):
    def __init__(self):
        self.message = "Speed cannot be negative"