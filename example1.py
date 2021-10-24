import Sakuya
import pygame
import sys

from Sakuya.vector import vector

WINDOW_SIZE = vector(500, 500)
TICKS_PER_SEC = 16

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE.x, WINDOW_SIZE.y))
pygame.display.set_caption("example")
clock = pygame.time.Clock()
delta_time = 0
ticks_past = 0

world = Sakuya.world()
entity1 = Sakuya.entity(Sakuya.vector(250, 250), 5)
entity1.velocity = vector(-10, 50)
entity2 = Sakuya.entity(Sakuya.vector(250, 250), 5)
entity2.velocity = vector(10, 50)
entity2.on_destroy(2000)
world.objects.append(entity1)
world.objects.append(entity2)

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0,0,0))
    for o in world.objects:
        o_rect = Sakuya.world_to_pygame_rect(o.hitbox, WINDOW_SIZE.y)
        pygame.draw.rect(screen, (255,255,255), o_rect)

    print(world.current_tick)

    pygame.display.update()
    world.advance_frame(delta_time)
    delta_time = 1 / clock.tick(60)