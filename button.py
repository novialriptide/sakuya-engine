import pygame
import sys
from math import *

class Button:
    def __init__(self, rect: pygame.Rect, methods=[], key=None):
        self.rect = rect
        self.key = key
        self.methods = methods

    @property
    def is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def is_pressing_key(self):
        return pygame.key.get_pressed()[self.key] == 1

    @property
    def is_pressing_mouse(self):
        return pygame.mouse.get_pressed()[0] and self.is_hovering

    def execute(self):
        for f in self.methods: f()

    def update(self):
        if self.is_pressing_mouse or self.is_pressing_key:
            self.execute()