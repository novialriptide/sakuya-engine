import pygame

class Button:
    def __init__(self, rect: pygame.Rect, method, args=[], kwargs={}):
        self.rect = rect
        self.method = method

    @property
    def is_hoverng(self):
        pass

    @property
    def is_clicked(self):
        pass