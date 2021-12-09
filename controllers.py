"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from .math import Vector

class BaseController:
    """Base class of a controller for a Player or Artificial Intelligence"""
    def __init__(self) -> None:
        """Used to control player movements

        Parameters:
            speed: Player movement speed
        """
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_moving_down = False
        self.is_moving_up = False

    @property
    def movement(self) -> Vector:
        _movement = Vector(0, 0)
        if self.is_moving_right:
            _movement.x = 1
        if self.is_moving_left:
            _movement.x = -1
        if self.is_moving_down:
            _movement.y = 1
        if self.is_moving_up:
            _movement.y = -1

        return _movement

    def stop_movement(self) -> None:
        """Stops the controller's movement"""
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_moving_down = False
        self.is_moving_up = False