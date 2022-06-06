"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from copy import copy
from typing import TypeVar, Callable, Union

import pygame
import logging
import pathlib
import os
import time
import traceback

from .clock import Clock
from .errors import NoActiveSceneError
from .events import EventSystem
from .scene import SceneManager

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)

__all__ = ["Client"]


def _get_time() -> str:
    month = time.strftime("%m")
    day = time.strftime("%d")
    year = time.strftime("%Y")
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    return f"{month}-{day}-{year} {hour}-{minute}-{second}"


class Client:
    def __init__(
        self,
        window_name: str,
        window_size: pygame_vector2,
        window_icon: pygame.Surface = None,
        resizeable_window: bool = True,
        scale_upon_startup: float = 1,
        debug_caption: bool = True,
        keep_aspect_ratio: bool = True,
        mouse_image: pygame.Surface = None,
        sound_channels: int = 64,
        log_dir: Union[str, None] = None,
    ) -> None:
        """The game's main client.

        Warning: An event system is already built in to this object, but
        do not use it for any events related to a scene. Only use it
        for notifications, client-sided messages, etc.

        Parameters:
            window_name: the window's name
            window_size: the window size
        """

        if log_dir is not None:
            self.local_dir_path = pathlib.Path.home() / log_dir
            self.local_log_path = self.local_dir_path / f"{_get_time()}.log"
            if not os.path.exists(str(self.local_dir_path)):
                os.makedirs(self.local_dir_path)

            os.chmod(self.local_dir_path, 0o777)
            logging.basicConfig(
                filename=self.local_log_path,
                format="%(asctime)s %(levelname)s: %(message)s",
                datefmt="%m/%d/%Y %I:%M:%S %p",
                level=logging.DEBUG,
            )

        logging.info("Initializing SakuyaEngine client")
        self.debug_caption = debug_caption
        self.is_running = True  # bool
        self.clock = Clock()
        self.event_system = EventSystem(self.clock)
        self._window_name = window_name  # str
        self._screen_pos = pygame.Vector2(0, 0)
        self.original_window_size = window_size  # pygame.Vector2
        self.window_icon = window_icon
        self.original_aspect_ratio = window_size.x / window_size.y  # float
        self.keep_aspect_ratio = keep_aspect_ratio
        self.mouse_image = mouse_image

        self.running_scenes = {}
        self.deleted_scenes_queue = []
        self.scene_manager = SceneManager(self)

        self.sounds = {}

        self.pg_clock = pygame.time.Clock()
        self.max_fps = 0
        self.delta_time = 0
        self.raw_delta_time = 0
        self.delta_time_modifier = 1

        self.pg_flag = 0
        if resizeable_window:
            self.pg_flag = pygame.RESIZABLE

        logging.info("Creating client pg_surface")
        self.screen = pygame.Surface(window_size)  # lgtm [py/call/wrong-arguments]
        logging.info("Scaling window_size")
        self.window_size = window_size * scale_upon_startup

        self.set_caption(self._window_name)

        if self.mouse_image is not None:
            logging.info(
                "Default mouse icon is disabled, overriding with custom mouse image"
            )
            pygame.mouse.set_cursor(
                (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)
            )

        if self.window_icon is None:
            pass  # add sakuya as a default icon

        if self.window_icon is not None:
            # if you run the program from source, the icon
            # won't show up until you compile the program.
            logging.info("Setting custom windows icon")
            pygame.display.set_icon(self.window_icon)

        self.events = []

        logging.info("Initializing pygame mixer")
        pygame.mixer.init()

        logging.info(f"Setting number of channels to {sound_channels}")
        pygame.mixer.set_num_channels(sound_channels)

        logging.info("Successfully initialized SakuyaEngine client")

    @property
    def window_name(self) -> str:
        return self._window_name

    @window_name.setter
    def window_name(self, value: str) -> None:
        logging.info("Setting window_name")
        self._window_name = value
        self.set_caption(self._window_name)

    @property
    def window_size(self) -> pygame.Vector2:
        return pygame.Vector2(self.window.get_size())

    @window_size.setter
    def window_size(self, value) -> None:
        logging.info("Setting window_size")
        self.window = pygame.display.set_mode((value.x, value.y), self.pg_flag)

    @property
    def screen_size(self) -> pygame.Vector2:
        return pygame.Vector2(
            self.window_size.y
            * self.original_window_size.x
            / self.original_window_size.y,
            self.window_size.y,
        )

    @property
    def _screen(self) -> pygame.Surface:
        return pygame.transform.scale(self.screen, self.screen_size)

    @property
    def scale(self) -> pygame.Vector2:
        return pygame.Vector2(
            (self.window_size.x - self._screen_pos.x * 2) / self.original_window_size.x,
            (self.window_size.y - self._screen_pos.y * 2) / self.original_window_size.y,
        )

    @property
    def mouse_pos(self) -> pygame.Vector2:
        scale = self.scale
        mouse_pos = pygame.mouse.get_pos()
        scaled_pos = pygame.Vector2(
            (mouse_pos[0] - self._screen_pos.x) / scale.x,
            (mouse_pos[1] - self._screen_pos.y) / scale.y,
        )
        return scaled_pos

    @property
    def current_fps(self) -> float:
        return self.pg_clock.get_fps()

    @property
    def get_num_channels(self) -> int:
        logging.info("Getting number of sound channels")
        return pygame.mixer.get_num_channels()

    def set_caption(self, val: str) -> None:
        pygame.display.set_caption(val)

    def main(self) -> None:
        """
        Main game loop
        """
        video_resize_event = None

        while self.is_running:
            try:
                # Delta time
                self.raw_delta_time = self.pg_clock.tick(self.max_fps) / 1000 * 60
                self.clock.speed = self.delta_time_modifier
                self.delta_time = self.raw_delta_time * self.delta_time_modifier

                if self.running_scenes == []:
                    raise NoActiveSceneError

                self.events = pygame.event.get()
                for event in self.events:
                    if event.type == pygame.VIDEORESIZE:
                        if video_resize_event == event:
                            continue

                        video_resize_event = event

                        if self.keep_aspect_ratio:
                            logging.info(f"Resizing window to correct aspect ratio")
                            new_height = (
                                event.w
                                * self.original_window_size.y
                                / self.original_window_size.x
                            )
                            self.window = pygame.display.set_mode(
                                (event.w, new_height), self.pg_flag
                            )
                        window_rect = self.window.get_rect()
                        screen_rect = self._screen.get_rect()
                        self._screen_pos = pygame.Vector2(
                            window_rect.centerx - screen_rect.centerx,
                            window_rect.centery - screen_rect.centery,
                        )

                # Update all scenes
                for s in copy(self.running_scenes):
                    s = self.running_scenes[s]["scene"]
                    if not s.paused:
                        s.update()
                        s.clock.speed = self.delta_time_modifier
                        self.screen.fill((191, 64, 191))
                        self.screen.blit(s.screen, s.screen_pos)

                # Delete scenes in queue
                for s in self.deleted_scenes_queue[:]:
                    try:
                        self.deleted_scenes_queue.remove(s)
                        del self.running_scenes[s]
                    except KeyError:
                        print(f'Tried deleting scene that does not exist: "{s}"')

                if self.mouse_image is not None and self.mouse_pos:
                    self.screen.blit(self.mouse_image, self.mouse_pos)

                self.window.blit(self._screen, self._screen_pos)

                self.event_system.update()
                pygame.display.update()

                if self.debug_caption:
                    fps = round(self.pg_clock.get_fps(), 2)
                    bullets = 0
                    entities = 0
                    effects = 0
                    scene_time = 0
                    client_time = round(self.clock.get_time(), 2)
                    for s in self.running_scenes:
                        s = self.running_scenes[s]["scene"]
                        bullets += len(s.bullets)
                        entities += len(s.entities)
                        effects += len(s.effects)
                        scene_time = round(s.clock.get_time(), 2)
                    scene = ", ".join(self.running_scenes)
                    self.set_caption(
                        f"fps: {fps}, entities: {entities + bullets}, effects: {effects}, scene_time: {scene_time}, client_time: {client_time}, scene: {scene}"
                    )
            except SystemExit:
                logging.info("Closing game")
                break
            except Exception as e:
                print(traceback.format_exc())
                import tkinter
                from tkinter import messagebox

                crash_msg = "Fatal error in main loop"
                logging.critical(crash_msg, exc_info=True)

                root = tkinter.Tk()
                root.withdraw()
                messagebox.showinfo("SakuyaEngine", crash_msg)

                break

    def add_scene(self, scene_name: str, **kwargs) -> None:
        """Adds scene to running scene

        Parameters:
            scene_name: str to be added

        """
        logging.info(f'Adding scene "{scene_name}" with kwargs: {kwargs}')
        scene = copy(self.scene_manager.get_scene(scene_name))(self)
        scene.on_awake(**kwargs)
        self.running_scenes[scene.name] = {"scene": scene, "kwargs": kwargs}

    def remove_scene(self, scene_name: str, **kwargs) -> None:
        """Removes scene

        Parameters:
            scene_name: str to be removed

        """
        try:
            logging.info(f'Removing scene "{scene_name}" with kwargs: {kwargs}')
            scene = self.running_scenes[scene_name]["scene"]
            scene.on_delete(**kwargs)
            self.deleted_scenes_queue.append(scene.name)
        except KeyError:
            logging.error(
                f'Tried removing a non-active scene "{scene_name}". Ignoring...'
            )

    def replace_scene(self, old_scene_name: str, new_scene_name: str, **kwargs) -> None:
        """Removes and adds a scene

        Parameters:
            scene_name: str to be added

        """
        try:
            logging.info(
                f'Replacing a non-active scene "{old_scene_name}" with "{new_scene_name}"'
            )
            self.remove_scene(old_scene_name)
            self.add_scene(new_scene_name, **kwargs)
        except KeyError:
            logging.error(
                f'Tried replacing a non-active scene "{old_scene_name}" with "{new_scene_name}". Ignoring...'
            )
