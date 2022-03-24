"""
SakuyaEngine // GameDen // GameDen Rewrite (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import Tuple
import pygame

ALPHABET_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_CHARS = "1234567890"
SPECIAL_CHARS = ",./;'[]\\-=<>?:\"{}|!@#$%^&*()"

CHAR_COLOR = (228, 0, 255)


class Font:
    """Handles pixel font without artifacts"""

    def __init__(
        self,
        alphabet_path: str = None,
        numbers_path: str = None,
        special_path: str = None,
    ) -> None:
        """Initialize Font object.

        Warning: The height for each image should all be the same.

        """
        self.database = {}
        self.alphabet_path = alphabet_path
        self.numbers_path = numbers_path
        self.special_path = special_path

        if self.alphabet_path is not None:
            self._alphabet_surface = pygame.image.load(self.alphabet_path)
            self._iterate_font_surf(self._alphabet_surface, ALPHABET_CHARS)

        if self.numbers_path is not None:
            self._numbers_surface = pygame.image.load(self.numbers_path)
            self._iterate_font_surf(self._numbers_surface, NUMBER_CHARS)

        if self.special_path is not None:
            self._special_surface = pygame.image.load(self.special_path)
            self._iterate_font_surf(self._special_surface, SPECIAL_CHARS)

    def _iterate_font_surf(self, surface: pygame.Surface, chars: str) -> None:
        start = 0
        width = 0
        alphabet_height = surface.get_height()
        char = 0
        chars = list(chars)
        for pixel in range(surface.get_width()):
            if surface.get_at((pixel, 0)) == CHAR_COLOR:
                width += 1
            elif surface.get_at((pixel, 0)) != CHAR_COLOR:
                self.database[chars[char]] = surface.subsurface(
                    (start, 1, width, alphabet_height - 1)
                ).convert_alpha()
                start += width + 1
                width = 0
                char += 1

            if char == len(chars):
                break

    def text(
        self,
        text,
        dist: int = 1,
        space_dist: int = 2,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> pygame.Surface:
        width = 0
        height = []
        for char in list(text):
            if char == " ":
                width += space_dist
                continue

            height.append(self.database[char].get_height())
            width += self.database[char].get_width() + dist
        width -= dist

        self.database[" "] = pygame.Surface(
            (space_dist, max(height)), pygame.SRCALPHA, 32
        )
        surf = pygame.Surface((width, max(height)), pygame.SRCALPHA, 32)

        current_width = 0
        for char in list(text):
            surf.blit(self.database[char], (current_width, 0))
            if char == " ":
                char_dist = 0
            elif char != " ":
                char_dist = dist

            current_width += self.database[char].get_width() + char_dist

        pixel_array = pygame.PixelArray(surf)  # lgtm [py/call/wrong-arguments]
        pixel_array.replace((0, 0, 0), color)

        return surf
