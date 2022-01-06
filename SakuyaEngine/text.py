"""
SakuyaEngine // GameDen // GameDen Rewrite (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import pygame
import pygame.freetype

from typing import Tuple

pygame.freetype.init()

def text(
    text: str,
    size: int,
    sys_font: str,
    color: Tuple[int, int, int],
    antialias: bool = False
) -> pygame.Surface:
    """Creates a pygame Surface object that 
    uses a font from the operating system.

    Parameters:
        text: The text that will be displayed.
        size: The surface's size.
        sys_font: The font name.
        color: The color in RGB format.

    Returns:
        A pygame Surface with text.

    """
    formatting = pygame.freetype.SysFont(sys_font)
    text_surface = formatting.render(text, fgcolor=color, size = size)
    return text_surface[0]

def text2(
    text: str,
    size: int,
    font: str,
    color: Tuple[int, int, int],
    antialias: bool = False
) -> pygame.Surface:
    """Creates a pygame Surface object that 
    uses a font from local files.

    Parameters:
        text: The text that will be displayed.
        size: The surface's size.
        font: The font name.
        color: The color in RGB format.

    Returns:
        A pygame Surface with text.

    """
    formatting = pygame.freetype.Font(font)
    text_surface = formatting.render(text, fgcolor=color, size = size)
    return text_surface[0]

alphabetchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
specialchars = ",./;'[]\\-=<>?:\"{}|!@#$%^&*()"
def text3(
    text: str,
    size: int,
    font: str,
    color: Tuple[int, int, int]
) -> pygame.Surface:
    transparent_background_color = (255, 43, 243)
    separate_color = (255, 43, 243)
    raise NotImplementedError()