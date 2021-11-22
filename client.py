import pygame
from ProjectRespawn.Sakuya.errors import NoActiveScene
from .scene import Scene
from .math import Vector

class Client:
    def __init__(
        self,
        window_name: str,
        window_size: Vector,
    ) -> None:
        self.is_running = True
        self._window_name = window_name
        self.window_size = window_size
        self.running_scenes = {}

        self.screen = pygame.display.set_mode(
            (self.window_size.x, self.window_size.y)
        )
        pygame.display.set_caption(self._window_name)

    @property
    def window_name(self) -> str:
        return self._window_name

    @window_name.setter
    def window_name(self, value: str) -> None:
        self._window_name = value
        pygame.display.set_caption(self._window_name)

    def main(self) -> None:
        """
        Main game loop
        """
        while(self.is_running):
            if self.running_scenes == []:
                raise NoActiveScene

            for s in self.running_scenes:
                s = self.running_scenes[s]["scene"]
                if s.is_paused:
                    s.update()
            
            pygame.display.flip()

    def add_scene(self, scene: Scene, **kwargs) -> None:
        """
        Adds scene to running scene 

        Parameters:
            scene: Scene to be added
        """
        scene.on_awake(kwargs)
        self.running_scenes[scene.name] = {"scene": scene(), "kwargs": kwargs}

    def remove_scene(self, scene: Scene, **kwargs) -> None:
        """
        Removes scene

        Parameters:
            scene: Scene to be removed
        """
        scene.on_delete(kwargs)
        del self.running_scenes[scene.name]

    def replace_scene(
        self,
        old_scene: Scene,
        new_scene: Scene, 
        **kwargs
    ) -> None:
        """
        Removes and adds a scene

        Parameters:
            scene: Scene to be added
        """
        self.remove_scene(old_scene)
        self.add_scene(new_scene, kwargs)