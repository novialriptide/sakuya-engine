import pygame
import sys
from SakuyaEngine.client import Client
from SakuyaEngine.scene import SceneManager
from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom

client = Client(
    f"SakuyaEngine Client Test Lighting",
    pygame.Vector2(256 * 1.5, 224 * 1.5),
    debug_caption=True,
)
scene_manager = SceneManager(client)


class TestScene(Scene):
    def on_awake(self):
        self.lightroom = LightRoom(self)
        self.lightroom.add_point_light(pygame.Vector2(50, 50), 25)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.lightroom.screen, (0, 0))


scene_manager.register_scene(TestScene)

client.add_scene("TestScene")

client.main()