import pygame
import sys
from SakuyaEngine.client import Client
from SakuyaEngine.scene import SceneManager
from SakuyaEngine.scene import Scene

client = Client(
    f"SakuyaEngine Client Test Template",
    pygame.Vector2(256 * 1.5, 224 * 1.5),
    debug_caption=False,
)
scene_manager = SceneManager(client)
client.max_fps = 60


class TestScene(Scene):
    def on_awake(self):
        pass

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        self.screen.fill((0, 0, 0))


scene_manager.register_scene(TestScene)

client.add_scene("TestScene")

client.main()
