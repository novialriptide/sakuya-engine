import pygame
from .errors import NoActiveScene
from .math import Vector

class Client:
    def __init__(
        self,
        window_name: str,
        window_size: Vector,
        window_icon: pygame.Surface = None
    ) -> None:
        """
        The game's main client

        Parameters:
            window_name: the window's name
            window_size: the window size
        """
        self.is_running = True
        self._window_name = window_name
        self.window_size = window_size
        self.window_icon = window_icon
        self.running_scenes = {}
        self.scene_manager = None

        self.screen = pygame.display.set_mode(
            (self.window_size.x, self.window_size.y)
        )
        pygame.display.set_caption(self._window_name)

        if self.window_icon is None:
            pass # add sakuya as a default icon

        if self.window_icon is not None:
            pygame.display.set_icon(self.window_icon)

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

    def add_scene(self, scene_name: str, **kwargs) -> None:
        """
        Adds scene to running scene 

        Parameters:
            scene_name: str to be added
        """
        scene = self.scene_manager.get_scene(scene_name)
        scene.on_awake(**kwargs)
        self.running_scenes[scene.name] = {"scene": scene, "kwargs": kwargs}

    def remove_scene(self, scene_name: str, **kwargs) -> None:
        """
        Removes scene

        Parameters:
            scene_name: str to be removed
        """
        scene = self.scene_manager.get_scene(scene_name)
        scene.on_delete(**kwargs)
        del self.running_scenes[scene.name]

    def replace_scene(
        self,
        old_scene_name: str,
        new_scene_name: str, 
        **kwargs
    ) -> None:
        """
        Removes and adds a scene

        Parameters:
            scene_name: str to be added
        """
        old_scene = self.scene_manager.get_scene(old_scene_name)
        new_scene = self.scene_manager.get_scene(new_scene_name)
        self.remove_scene(old_scene)
        self.add_scene(new_scene, **kwargs)