import pygame
import SakuyaEngine as engine


class Player(engine.Entity):
    def on_awake(self, scene) -> None:
        self.speed = 0.75
        self.can_walk = True

        idle_img = pygame.Surface((8, 8))
        idle_img.fill((255, 255, 255))
        idle = engine.Animation("idle", [idle_img])
        self.anim_add(idle)
        self.anim_set("idle")


import pygame
import sys

KEYBOARD = {
    "up1": pygame.K_w,
    "left1": pygame.K_a,
    "down1": pygame.K_s,
    "right1": pygame.K_d,
    "up2": pygame.K_w,
    "left2": pygame.K_a,
    "down2": pygame.K_s,
    "right2": pygame.K_d,
    "A": pygame.K_z,
    "B": pygame.K_x,
    "X": None,
    "Y": None,
    "select": pygame.K_q,
    "start": pygame.K_ESCAPE,
}


class PlayerController(engine.BaseController):
    def __init__(self) -> None:
        super().__init__()


class Test(engine.Scene):
    def on_awake(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.collision_rects = [pygame.Rect(30, 30, 50, 50)]

        # Player Setup
        self.player = Player()
        self.player.position = screen_size / 3
        self.add_entity(self.player)
        self.controller = PlayerController()

    def input(self) -> None:
        controller = self.controller
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.player.can_walk:
                    if event.key == KEYBOARD["left1"]:
                        controller.is_moving_left = True

                    if event.key == KEYBOARD["right1"]:
                        controller.is_moving_right = True

                    if event.key == KEYBOARD["up1"]:
                        controller.is_moving_up = True

                    if event.key == KEYBOARD["down1"]:
                        controller.is_moving_down = True

            if event.type == pygame.KEYUP:
                if self.player.can_walk:
                    if event.key == KEYBOARD["left1"]:
                        controller.is_moving_left = False

                    if event.key == KEYBOARD["right1"]:
                        controller.is_moving_right = False

                    if event.key == KEYBOARD["up1"]:
                        controller.is_moving_up = False

                    if event.key == KEYBOARD["down1"]:
                        controller.is_moving_down = False

    def update(self):
        self.screen.fill((0, 0, 0))

        self.player.velocity = self.player.speed * self.controller.movement

        for c in self.collision_rects:
            pygame.draw.rect(self.screen, (255, 0, 0), c)

        # Draw Entities
        for e in self.entities:
            self.screen.blit(e.sprite, e.position + self.camera.position)

        print(self.player.position)
        self.input()
        self.advance_frame()
