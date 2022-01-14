"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List

import pygame

from .camera import Camera
from .client import Client
from .entity import Entity
from .errors import EntityNotInScene
from .events import EventSystem
from .clock import Clock


class ScrollBackgroundSprite:
    def __init__(
        self, sprite: pygame.Surface, scroll: pygame.Vector2, infinite: bool = False
    ) -> None:
        self.sprite = sprite
        self.scroll = scroll
        self.infinite = infinite
        self.position = pygame.Vector2(0, 0)


class Scene:
    def __init__(self, client: Client, **kwargs) -> None:
        """The base class for a scene

        This class must be inherited by another class in order to work properly.

        Parameters:
            client: game client
        """
        self.paused = False
        self.client = client
        self.entities = []
        self.bullets = []
        self.particle_systems = []
        self.effects = []
        self.scroll_bgs = []
        self.collision_rects = []
        self.kwargs = kwargs
        self.clock = Clock()
        self.camera = Camera(clock=self.clock)
        self.event_system = EventSystem(self.clock)

        self.screen_pos = pygame.Vector2(0, 0)
        self.screen = self.client.screen.copy()
        self.screen.fill((0, 0, 0))

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def on_awake(self, **kwargs) -> None:
        """Will be called upon startup.

        Must be overrided

        Parameters:
            kwargs: Kwargs to pass onto the event.

        """
        pass

    def on_delete(self, **kwargs) -> None:
        """Will be called upon destruction.

        Must be overrided

        Parameters:
            kwargs: Kwargs to pass onto the event.

        """
        pass

    def update(self, delta_time, **kwargs) -> None:
        """Will be called upon every frame. Calling advance_frame() is recommended.

        Must be overrided.

        Parameters:
            kwargs: Kwargs to pass onto the event.

        """
        pass

    def find_entities_by_name(self, name: str) -> List[Entity]:
        """Finds all registered entities in this scene

        Parameters:
            name: Name of the entity

        """
        entities = []
        for o in self.entities:
            if o.name == name:
                entities.append(o)

        return entities

    def test_collisions_rect(
        self, entity: Entity, ignore_tag: str = None
    ) -> List[Entity]:
        """Returns a list of entities that collides with an entity using pygame.Rect(s).

        Parameters:
            entity: The entity to compare with.
            ignore_tag: Tag to ignore.

        """
        entities = self.entities[:]
        entities.extend(self.bullets[:])
        try:
            entities.remove(entity)
        except:
            raise EntityNotInScene

        collided = []
        for e in entities:
            if (
                entity.custom_hitbox.colliderect(e.custom_hitbox)
                and ignore_tag not in e.tags
            ):
                collided.append(e)

        return collided

    def test_collisions_point(
        self, entity: Entity, ignore_tag: str = None
    ) -> List[Entity]:
        """Returns a list of entities that collides with
        an entity using points. The entity's hitbox will
        still be a pygame.Rect.

        Parameters:
            entity: The entity to compare with.
            ignore_tag: Tag to ignore.

        """
        entities = self.entities[:]
        entities.extend(self.bullets[:])
        try:
            entities.remove(entity)
        except:
            raise EntityNotInScene

        collided = []
        for e in entities:
            if (
                entity.custom_hitbox.collidepoint(e.position + e.center_offset)
                and ignore_tag not in e.tags
            ):
                collided.append(e)

        return collided

    def draw_scroll_bg(self) -> None:
        for bg in self.scroll_bgs:
            bg_rect = bg.sprite.get_rect()
            self.screen.blit(bg.sprite, bg.position)
            if bg.position.x - 1 < bg_rect.width:
                self.screen.blit(
                    bg.sprite, (bg.position.x - bg_rect.width, bg.position.y)
                )
            if bg.position.x >= bg_rect.width:
                self.screen.blit(
                    bg.sprite, (bg.position.x + bg_rect.width, bg.position.y)
                )
            if bg.position.y < bg_rect.height:
                self.screen.blit(
                    bg.sprite, (bg.position.x, bg.position.y - bg_rect.height)
                )
            if bg.position.y >= bg_rect.height:
                self.screen.blit(
                    bg.sprite, (bg.position.x, bg.position.y + bg_rect.height)
                )

    def advance_frame(
        self, delta_time: float, collision_rects: List[pygame.Rect] = []
    ) -> None:
        """Updates the entities inside the world, such as
        physics & animation

        Should be added to the end of the main loop

        Parameters:
            delta_time: The game's delta time

        """
        self.camera.update(delta_time)

        for p in self.particle_systems:
            p.update(delta_time)

        for bg in self.scroll_bgs:
            bg_rect = bg.sprite.get_rect()
            bg.position += bg.scroll * delta_time
            if bg.position.x >= bg_rect.width:
                bg.position.x = 0
            if bg.position.y >= bg_rect.height:
                bg.position.y = 0
            if bg.position.x < 0:
                bg.position.x = bg_rect.width
            if bg.position.y < 0:
                bg.position.y = bg_rect.height

        for entity in self.entities[:]:
            entity.update(delta_time, collision_rects=collision_rects)
            if entity._destroy_queue:
                self.entities.remove(entity)

            # Update Bullet Spawners
            for bs in entity.bullet_spawners:
                bs.position = entity.position + entity.center_offset
                if entity.update_bullet_spawners:
                    if (
                        entity.disable_bulletspawner_while_movement
                        and entity.target_position is not None
                        or entity.destroy_position is not None
                    ):
                        continue
                    new_bullets = bs.update(delta_time)
                    self.bullets.extend(new_bullets)

        for bullet in self.bullets[:]:
            bullet.update(delta_time)
            if bullet._destroy_queue:
                self.bullets.remove(bullet)

        for ef in self.effects[:]:
            ef.update(delta_time)
            if ef._destroy_queue:
                self.effects.remove(ef)


class SubScene(Scene):
    def exit(self) -> None:
        self.exit_scene.paused = False
        self.exit_scene.clock.resume()
        self.client.remove_scene(self.name)


class SceneManager:
    def __init__(self, client: Client) -> None:
        """The scene manager which is used to register scenes

        Parameters:
            client: game client

        """
        client.scene_manager = self
        self.client = client
        self.registered_scenes = {}

    def register_scene(self, scene: Scene) -> bool:
        """Registers a scene into the scene manager

        Parameters:
            scene: scene to be registered

        """
        instance = scene
        self.registered_scenes[scene.__name__] = instance

    def get_scene(self, scene_name: str) -> Scene:
        return self.registered_scenes[scene_name]
