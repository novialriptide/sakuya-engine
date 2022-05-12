from math import degrees
import pygame
import sys
import SakuyaEngine as engine

client = engine.Client(
    f"SakuyaEngine Client Test Lighting",
    pygame.Vector2(256 * 1.5, 224 * 1.5),
    debug_caption=True,
)
scene_manager = engine.SceneManager(client)

bg = pygame.image.load("resources\sakuya_background.jpg")
bg = pygame.transform.scale(bg, pygame.Vector2(bg.get_size()) / 2)


class TestScene(engine.Scene):
    def on_awake(self):
        self.lightroom = engine.LightRoom(self)
        self.collisions = [[pygame.Vector2(75, 35), pygame.Vector2(75, 75)]]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 255))
        self.screen.blit(bg, pygame.Vector2(bg.get_size()) / -2 + screen_size / 2)

        self.lightroom.draw_point_light(screen_size / 2, 35, collisions=self.collisions)

        dir = degrees(engine.get_angle(self.client.mouse_pos, screen_size / 2)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 2, 150, dir, 65, collisions=self.collisions
        )
        dir = degrees(engine.get_angle(self.client.mouse_pos, screen_size / 3)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 3, 150, dir, 45, collisions=self.collisions
        )
        self.screen.blit(self.lightroom.surface, (0, 0))

        for c in self.collisions:
            pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])


scene_manager.register_scene(TestScene)

client.add_scene("TestScene")

client.main()
