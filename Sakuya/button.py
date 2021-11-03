import pygame
from math import *

class Button:
    def __init__(self, rect: pygame.Rect, methods=[]):
        self.rect = rect
        self.methods = methods

    @property
    def is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def execute(self):
        for f in self.methods: f()

    def update(self):
        if pygame.mouse.get_pressed()[0] and self.is_hovering:
            self.execute()