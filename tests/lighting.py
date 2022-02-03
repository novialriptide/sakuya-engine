from math import degrees
import pygame
import sys
from SakuyaEngine.client import Client
from SakuyaEngine.scene import SceneManager
from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle

client = Client(
    f"SakuyaEngine Client Test Lighting",
    pygame.Vector2(256 * 1.5, 224 * 1.5),
    debug_caption=True,
)
scene_manager = SceneManager(client)

bg = pygame.image.load("resources\sakuya_background.jpg")
bg = pygame.transform.scale(bg, pygame.Vector2(bg.get_size()) / 2)


class TestScene(Scene):
    def on_awake(self):
        self.lightroom = LightRoom(self)
        self.collisions = [[pygame.Vector2(50, 20), pygame.Vector2(50, 50)]]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 255))
        self.screen.blit(bg, pygame.Vector2(bg.get_size()) / -2 + screen_size / 2)

        self.lightroom.draw_point_light(screen_size / 2, 35, collisions=self.collisions)

        dir = degrees(get_angle(self.client.mouse_pos, screen_size / 2)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 2, 150, dir, 65, collisions=self.collisions
        )
        dir = degrees(get_angle(self.client.mouse_pos, screen_size / 3)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 3, 150, dir, 45, collisions=self.collisions
        )
        self.screen.blit(self.lightroom.surface, (0, 0))

        for c in self.collisions:
            pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])


scene_manager.register_scene(TestScene)

client.add_scene("TestScene")

client.main()
