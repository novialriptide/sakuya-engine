"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List

from .events import EventSystem, WaitEvent
from .scene import Scene
from .entity import Entity
from .errors import NotEnoughArgumentsError

import pygame
import json

class WaveManager:
    def __init__(self):
        pass
    
    def spawn(
        self,
        event_system: EventSystem,
        enemy_path: List[pygame.Vector2],
        entity_id: int,
        lifetime: int = 10000
    ) -> Entity:
        e = self.entities[entity_id].copy()

        def move_despawn_func(entity: Entity, despawn_pos: pygame.Vector2):
            # Event that will wait until it's time for it to despawn and execute the despawn movement.
            entity.target_position = despawn_pos - e.center_offset
            entity.destroy_position = despawn_pos - e.center_offset

        e.position = enemy_path[0] - e.center_offset
        e.target_position = enemy_path[1] - e.center_offset

        if lifetime != 0:
            wait_moveback_enemy = WaitEvent("wait_moveback_enemy", lifetime, move_despawn_func, args=[e, enemy_path[2]])
            event_system._methods.append(wait_moveback_enemy)

        return e
    
    def update(self) -> None:
        pass

def _create_spawn_event_stage(
    wave_manager: WaveManager,
    scene: Scene,
    event_system: EventSystem,
    enemy_path: List[pygame.Vector2],
    entity_id: int,
    wait_time: int,
    lifetime: int = 10000
) -> WaitEvent:
    def spawn_func(_event_system, _enemy_path, _entity_id, _lifetime):
        entity = wave_manager.spawn(_event_system, _enemy_path, _entity_id, _lifetime)
        scene.entities.append(entity)
    spawn_event = WaitEvent("spawn_enemy", wait_time, spawn_func, args=[
        event_system, enemy_path, entity_id, lifetime
    ])
    return spawn_event

def load_stage_json(
    path: str,
    wave_manager: WaveManager,
    scene: Scene
) -> None:
    file = open(path, "r")
    data = json.load(file)
    wait_time = 0
    
    for w in data["waves"].keys():
        for p in data["waves"][w]:
            enemy_path = data["paths"][p]["paths"]
            enemies = data["waves"][w][p]["enemies"]
            
            for entity_id in enemies:
                spawn_event = _create_spawn_event_stage(
                    wave_manager, scene, scene.event_system, enemy_path,
                    entity_id, wait_time
                )
                scene.event_system._methods.append(spawn_event)
        
        wait_time += int(w)