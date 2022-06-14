import pygame
import logging

from .clock import Clock

__all__ = ["Sound"]


class Sound:
    def __init__(self, source: str, cooldown: int = 0, volume: float = 1) -> None:
        self.source = source
        self._pg_source = pygame.mixer.Sound(self.source)
        self.cooldown = cooldown
        self._cooldown_clock = Clock(pause_upon_start=True)
        self._playing = False
        self._volume = volume
        self._pg_source.set_volume(self._volume)
        self._volume_modifier = 1

    @property
    def volume_modifier(self) -> float:
        return self._volume_modifier

    @volume_modifier.setter
    def volume_modifier(self, value: float) -> None:
        self._volume_modifier = value
        self._pg_source.set_volume(self._volume * self._volume_modifier)

    def play(self, repeat: bool = False) -> None:
        if repeat and self.cooldown == 0:
            logging.info(f'Playing sound "{self.source}" on repeat')
            self._pg_source.play(loops=-1)

        elif repeat and self.cooldown > 0:
            self._cooldown_clock.resume()
            if self.cooldown < self._cooldown_clock.get_time():
                logging.warning(
                    f'Tried playing sound "{self.source}" on repeat with a cooldown'
                )
                self._cooldown_clock.reset()
            if self._cooldown_clock.get_time() == 0:
                logging.info(f'Playing sound "{self.source}" on repeat with a cooldown')
                self._pg_source.play()

        if not repeat:
            logging.info(f'Playing sound "{self.source}"')
            self._pg_source.play()

    def stop(self) -> None:
        self._pg_source.stop()
        self._cooldown_clock.reset()
        self._cooldown_clock.pause()
