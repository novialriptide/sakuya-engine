"""
SakuyaEngine // GameDen (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
import pygame

def text(
    text: str,
    size: int,
    sys_font: str,
    color: str
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
    # NOTE: This function is a variant 
    # from GameDen REWRITE for Novial's Gravity
    pygame.font.init()
    formatting = pygame.font.SysFont(sys_font, int(size))
    text_surface = formatting.render(text, True, color)
    return text_surface

def text2(
    text: str,
    size: int,
    font: str,
    color: str
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
    # NOTE: This function is a variant 
    # from GameDen REWRITE for Novial's Gravity
    pygame.font.init()
    formatting = pygame.font.Font(font, int(size))
    text_surface = formatting.render(text, True, color)
    return text_surface