import pygame
pygame.font.init()

"""
v1.0
This source code is taken straight
from GameDen Engine for Novial's Gravity.
Therefore, parameters should be the same.
"""

def text(text: str, size: int, sys_font: str, color: str):
    formatting = pygame.font.SysFont(sys_font,int(size))
    text_surface = formatting.render(text,True,color)
    return text_surface

def text2(text: str, size: int, font: str, color: str):
    formatting = pygame.font.Font(font,int(size))
    text_surface = formatting.render(text,True,color)
    return text_surface