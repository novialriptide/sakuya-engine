"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
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

class SceneNotActiveError(Error):
    def __init__(self):
        self.message = "Scene is not active"

class NotEnoughArgumentsError(Error):
    def __init__(self):
        self.message = "Not enough arguments."

class LineSegmentLinesError(Error):
    def __init__(self):
        # Coincident means "same line"
        self.message = "Two lines inputted are parallel or coincident"