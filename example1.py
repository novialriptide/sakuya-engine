import Sakuya
import pygame
import sys

from Sakuya.vector import vector

WINDOW_SIZE = (500, 500)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("example")
clock = pygame.time.Clock()
delta_time = 0

world = Sakuya.world()
entity1 = Sakuya.entity(Sakuya.vector(3, 2), 5)
entity1.on_destroy(5)
entity1.velocity = vector(2, 2)
entity1.acceleration = vector(1, 1)
world.objects.append(entity1)

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(entity1.position.x, entity1.position.y, 5, 5))

    print(entity1.on_destroy)

    pygame.display.update()
    world.advance_frame(delta_time)
    delta_time = 1 / clock.tick(60)