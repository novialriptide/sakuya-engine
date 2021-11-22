class Error(Exception):
    pass

class NegativeSpeedError(Error):
    def __init__(self):
        self.message = "Speed cannot be negative"

class ObjectNotInWorld(Error):
    def __init__(self):
        self.message = "Object is not in the world"

class NoActiveScene(Error):
    def __init__(self):
        self.message = "No scene is active"