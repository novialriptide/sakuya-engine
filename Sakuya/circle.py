from Sakuya.math import *
import pygame
import math

class Circle:
    def __init__(self, position: Vector, radius: int):
        self.position = position
        self.radius = radius

    def collidepoint(self, point: Vector):
        dist_x = point.x - self.position.x
        dist_y = point.y - self.position.y
        distance = math.sqrt(math.pow(dist_x, 2) + math.pow(dist_y, 2))
        
        return distance <= self.radius


    def colliderect(self, rect: pygame.Rect):
        pass

    def collidecircle(self, circle):
        dist_x = self.position.x - circle.position.x
        dist_y = self.position.y - circle.position.y
        distance = math.sqrt(math.pow(dist_x, 2) + math.pow(dist_y, 2))

        return distance <= self.radius + circle.radius