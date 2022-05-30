from typing import Union
import pygame

from .clock import Clock

__all__ = ["Sound"]

class Sound:
    def __init__(self, source: str, time: Union[int, None] = None) -> None:
        self.source = source
        self.time = time
        self._pg_source = pygame.mixer.Sound(self.source)
        self._cooldown_clock = Clock(pause_upon_start=True)
        self._cooldown = 0
        self._playing = False
        self._play_times = 0

    def play(self, play_times: int = 1) -> None:
        """Plays the sound.

        Parameters:
            play_times (int): The amount of times the sound will be played.
            -1 for infinite.

        """
        self._play_times += play_times

    def update(self) -> None:
        if self._cooldown < self._cooldown_clock.get_time():
            return
        else:
            self._cooldown_clock.reset()

        if self._play_times > 0:
            self._pg_source.play()
            self._play_times -= 1

        elif self._play_times == -1:
            self._pg_source.play()

        else:
            raise Exception("Unexpected play times value.")


class SoundManager:
    def __init__(self, client: "Client") -> None:
        self.client = client
        self._sounds = {}

    def register(self, name, sound: Sound) -> None:
        self._sounds[name] = sound

    def update(self) -> None:
        for s in self.sounds:
            s.update()
