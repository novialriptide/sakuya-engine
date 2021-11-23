from .math import Vector

class BaseController:
    """
    Base class of a controller for a Player or Artificial Intelligence
    """
    def __init__(self, speed: int) -> None:
        """
        Used to control player movements

        Parameters:
            speed: Player movement speed
        """
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_moving_down = False
        self.is_moving_up = False
        self.speed = speed

    @property
    def movement(self):
        _movement = Vector(0, 0)
        if self.is_moving_right:
            _movement.x = self.speed
        if self.is_moving_left:
            _movement.x = -self.speed
        if self.is_moving_down:
            _movement.y = self.speed
        if self.is_moving_up:
            _movement.y = -self.speed

        return _movement

    def stop_movement(self):
        """
        Stops the controller's movement
        """
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_moving_down = False
        self.is_moving_up = False