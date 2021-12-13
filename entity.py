"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from __future__ import annotations
from typing import TypeVar, Callable

import pygame
import math
import json

from typing import List
from copy import copy

from .animation import Animation, load_anim_dict, split_image
from .physics import gravity
from .particles import load_particles_dict
from .controllers import BaseController
from .particles import Particles
from .bar import Bar

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.math.Vector2)

class Entity:
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: int = 1,
        max_health: float = 100,
        position: pygame_vector2 = pygame.math.Vector2(0, 0),
        controller: BaseController = None,
        fire_rate: int = 0,
        has_collision: bool = True,
        has_rigidbody: bool = False,
        enable_terminal_velocity: bool = False,
        obey_gravity: bool = True,
        speed: float = 0,
        custom_hitbox_size: pygame_vector2 = pygame.math.Vector2(0, 0),
        particle_systems: List[Particles] = [],
        bullet_spawners: List[BulletSpawner] = [],
        update_bullet_spawners: bool = True,
        static_sprite: pygame.Surface = None,
        healthbar_update_speed: float = 1000,
        healthbar_position_offset: pygame_vector2 = pygame.math.Vector2(0, 0),
        draw_healthbar: bool = True
    ):
        """Objects that goes with a scene
        """
        self.name = name
        self.tags = tags
        self.scale = pygame.math.Vector2(1, 1) * scale
        
        if controller is not None:
            self.controller = controller()
        if controller is None:
            self.controller = None

        self.has_collision = has_collision
        self.animations = {}
        self.current_anim = None
        self.position = position
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = speed
        self.acceleration = pygame.math.Vector2(0, 0)
        self.obey_gravity = obey_gravity
        self.terminal_velocity = 10.0
        self.enable_terminal_velocity = enable_terminal_velocity

        self.has_collision = has_collision
        self.has_rigidbody = has_rigidbody
        self.custom_hitbox_size = custom_hitbox_size
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._custom_hitbox_rect = pygame.Rect(0, 0, 0, 0)

        self.particle_systems = particle_systems
        self.bullet_spawners = bullet_spawners
        self.update_bullet_spawners = update_bullet_spawners
        
        # destroy
        self._destroy_val = 0
        self._enable_destroy = False
        self._is_destroyed = False

        # shooting
        self.fire_rate = fire_rate
        self.can_shoot = True
        self.next_fire_ticks = pygame.time.get_ticks()

        self.current_health = max_health
        self._max_health = max_health

        self.healthbar = Bar(max_health, healthbar_update_speed)
        self.healthbar_position_offset = healthbar_position_offset
        self.draw_healthbar = draw_healthbar

        self.static_sprite = static_sprite

    @property
    def sprite(self) -> pygame.Surface:
        cur_anim = self.anim_get(self.current_anim)
        if self.static_sprite is not None:
            width, height = self.static_sprite.get_size()
            scaled_sprite = pygame.transform.scale(
                self.static_sprite, (
                    self.scale.x * width, 
                    self.scale.y * height
                )
            )
            return scaled_sprite
        if cur_anim is not None:
            width, height = cur_anim.sprite.get_size()
            scaled_sprite = pygame.transform.scale(
                cur_anim.sprite, (
                    self.scale.x * width, 
                    self.scale.y * height
                )
            )
            return scaled_sprite

    @property
    def rect(self) -> pygame.Rect:
        if self.sprite is not None:
            width, height = self.sprite.get_size()
            self._rect.x = self.position.x
            self._rect.y = self.position.y
            self._rect.width = width
            self._rect.height = height
            return self._rect
        if self.sprite is None:
            return pygame.Rect(self.position.x, self.position.y, 1, 1)

    @property
    def custom_hitbox(self) -> pygame.Rect:
        rect = self.rect
        self._custom_hitbox_rect.x = self.position.x + rect.width/2 - self.custom_hitbox_size.x
        self._custom_hitbox_rect.y = self.position.y + rect.height/2 - self.custom_hitbox_size.y
        self._custom_hitbox_rect.width = self.custom_hitbox_size.x*2
        self._custom_hitbox_rect.height = self.custom_hitbox_size.y*2
        return self._custom_hitbox_rect

    @property
    def center_offset(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.rect.width/2, self.rect.height/2)

    def destroy(self, time: int) -> None:
        """Set the destruction time.

        Parameters:
            time: milliseconds to destruction

        """
        self._enable_destroy = True
        self._destroy_val = time + pygame.time.get_ticks()

    def get_collisions(
        self,
        rects: List[pygame.Rect]
    ) -> List[pygame.Rect]:
        """Get a list of rects that collide with the entity's rect.
        
        It's recommended to use scene.test_collisions() instead.

        Parameters:
            rects: List of pygame rects.

        """
        return pygame.Rect.collidelistall(self.rect, rects)

    def move(
        self,
        movement: pygame_vector2, 
        collision_rects: List[pygame.Rect]
    ) -> bool:
        """Moves the position

        Parameters:
            movement: value to add to position

        Returns:
            If true, the position has been updated

        """
        
        self.position += movement
    
    def shoot(
        self,
        offset: pygame_vector2,
        projectile,
        angle: float,
        speed: float
    ) -> Entity:
        """Shoot an entity.

        Parameters:
            offset: The position offset of where the projectile's initial position.
            projectile: The entity that will be spawned.
            angle: The angle (radian) of the projectile's velocity
            speed: Speed of the projectile.

        """
        if self.can_shoot and pygame.time.get_ticks() >= self.next_fire_ticks:
            self.next_fire_ticks = pygame.time.get_ticks() + self.fire_rate
            projectile = copy(projectile)
            projectile.owner = self
            projectile.velocity = pygame.math.Vector2(speed * math.cos(angle), speed * math.sin(angle))
            projectile.position = self.position + offset - pygame.math.Vector2(projectile.rect.width/2, projectile.rect.height/2)
            return projectile

    def anim_get(self, animation_name: str) -> Animation:
        if animation_name is not None:
            return self.animations[animation_name]
        if animation_name is None:
            return None

    def anim_set(self, animation_name: str) -> bool:
        """Assign an animation to be played

        Parameters:
            animation_name: Animation to be played

        Returns:
            If true, playing the animation was successful

        """
        self.current_anim = animation_name

    def anim_add(self, animation: Animation) -> None:
        """Adds an animation

        Parameters:
            animation: Animation to be added

        """
        self.animations[animation.name] = copy(animation)

    def anim_remove(self, animation_name: str) -> bool:
        """Removes an animation

        Parameters:
            animation_name: Animation to be removed

        Returns:
            If True, removing the animation was successful

        """
        raise NotImplementedError

    def copy(self) -> Entity:
        """Returns a copy of the entity
        
        You should not use Python3's copy.copy() method since
        it will interfere with the same entities animations

        """
        e = copy(self)
        new_anims = {}
        new_particles = []
        new_bullet_spawners = []
        new_healthbar = copy(e.healthbar)
        for a in self.animations.keys():
            new_anims[a] = copy(self.anim_get(a))

        for p in self.particle_systems:
            new_particles.append(copy(p))

        for bs in self.bullet_spawners:
            new_bullet_spawners.append(copy(bs))

        e.animations = new_anims
        e.particle_systems = new_particles
        e.bullet_spawners = new_bullet_spawners
        e.healthbar = new_healthbar

        return e

    def update(self, delta_time: float) -> None:
        """Updates the position, animation, etc

        Parameters:
            delta_time: the game's delta time

        """
        # Destroy
        if self._enable_destroy and self._destroy_val <= pygame.time.get_ticks():
            self._is_destroyed = True

        # Update Particles
        for ps in self.particle_systems:
            ps.position = self.position
            ps.update(delta_time)
        
        # Update Animation
        if self.current_anim is not None:
            self.anim_get(self.current_anim).update(delta_time)

        # Update HealthBar
        self.healthbar.current_health = self.current_health
        self.healthbar.update(delta_time)

        # Apply terminal velocity
        term_vec = self.terminal_velocity * delta_time
        if self.enable_terminal_velocity:
            if self.velocity.x < 0:
                self.velocity.x = max(self.velocity.x, term_vec)
            if self.velocity.x > 0:
                self.velocity.x = min(self.velocity.x, term_vec)
            if self.velocity.y < 0:
                self.velocity.y = max(self.velocity.y, term_vec)
            if self.velocity.y > 0:
                self.velocity.y = min(self.velocity.y, term_vec)

        # Controller movement
        if self.controller is not None:
            self.velocity = self.controller.movement * self.speed

        # Apply gravity?
        g = gravity
        if not self.obey_gravity:
            g = pygame.math.Vector2(0, 0)

        # Apply velocity
        if self.has_rigidbody:
            self.velocity += self.acceleration + g
        
        velocity = self.velocity * delta_time
        self.move(velocity, [])

def load_entity_json(json_path: str, bullet_target: Entity = None) -> Entity:
    from .bullets import load_bulletspawner_dict

    data = json.load(open(json_path))
    return_entity = Entity()

    # Position
    if "position" in data.keys():
        data["position"] = pygame.math.Vector2(data["position"])

    # Custom Hitbox Size
    if "custom_hitbox_size" in data.keys():
        data["custom_hitbox_size"] = pygame.math.Vector2(data["custom_hitbox_size"])

    # Healthbar
    if "healthbar_position_offset" in data.keys():
        data["healthbar_position_offset"] = pygame.math.Vector2(data["healthbar_position_offset"])

    # Animations
    if "animations" in data.keys() and "static_sprite" not in data.keys():
        for a in data["animations"][:]:
            anim = load_anim_dict(a)
            return_entity.anim_add(anim)
        return_entity.anim_set(list(return_entity.animations.keys())[0])
        del data["animations"]

    if "static_sprite" in data.keys():
        sprite = split_image(
            pygame.image.load(data["static_sprite"]["path"]),
            px_width = data["static_sprite"]["width"],
            px_height = data["static_sprite"]["height"]
        )
        data["static_sprite"] = pygame.image.load(sprite[data["static_sprite"]["index"]])

    for key in data:
        if hasattr(return_entity, key):
            setattr(return_entity, key, data[key])

    # Bullet Spawners
    if "bullet_spawners" in data.keys():
        spawners = data["bullet_spawners"][:]
        new_bullet_spawners = []
        for bs in spawners:
            new_bs = load_bulletspawner_dict(bs)
            new_bs.target = bullet_target
            new_bullet_spawners.append(new_bs)

        return_entity.bullet_spawners = new_bullet_spawners

    # Particle Systems
    if "particle_systems" in data.keys():
        particle_systems = data["particle_systems"][:]
        new_particle_systems = []
        for ps in particle_systems:
            new_ps = load_particles_dict(ps)
            new_particle_systems.append(new_ps)
        
        return_entity.particle_systems = new_particle_systems

    return return_entity
