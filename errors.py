class Error(Exception):
    pass

class NotImplementedError(Error):
    def __init__(self):
        self.message = "This feature is not available"

class NegativeSpeedError(Error):
    def __init__(self):
        self.message = "Speed cannot be negative"

class ObjectNotInWorldError(Error):
    def __init__(self):
        self.message = "Object is not in the world"

class NoActiveSceneError(Error):
    def __init__(self):
        self.message = "No scene is active"