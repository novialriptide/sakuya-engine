class Error(Exception):
    pass

class NotImplementedError(Error):
    def __init__(self):
        self.message = "This feature is not available."

class NegativeSpeedError(Error):
    def __init__(self):
        self.message = "Speed cannot be negative."

class EntityNotInScene(Error):
    def __init__(self):
        self.message = "Entity is not in scene."

class NoActiveSceneError(Error):
    def __init__(self):
        self.message = "No scene is active."

class NotEnoughArgumentsError(Error):
    def __init__(self):
        self.message = "Not enough arguments."