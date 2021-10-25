import pygame
pygame.font.init()

def text(text: str, size: int, sys_font: str, color: str):
    formatting = pygame.font.SysFont(sys_font,int(size))
    text_surface = formatting.render(text,True,color)
    return text_surface

def text2(text: str, size: int, font: str, color: str):
    formatting = pygame.font.Font(font,int(size))
    text_surface = formatting.render(text,True,color)
    return text_surface