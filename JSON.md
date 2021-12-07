# Animation
Referred to as `anim_data` in other JSON files.

`Animation` can be added by referring to their parameters via the json file.

# Entity
Referred to as `entity_data` in other JSON files.

You can also add the `Entity` parameters via a json file as well.

For `event_animations`, refer to the animation's `name (string)`.
```json
{
    "animations": [anim_data, ...],
    "bullet_movesets": [
        {
            "spawn_chance": null,
            "bullet": bullet_data
            "bullet_spawner": bullet_spawner_data
        }
    ],
    "event_sounds": {
        "on_shoot": [...],
        "on_death": [...],
        "ambient": [...],
        ...
    }
}
```

# Bullet Spawner
Referred to as `bullet_spawner_data` in other JSON files.

`BulletSpawner` can be added by referring to their parameters via the json file.

# Bullet
Referred to as `bullet_data` in other JSON files.

`Bullet` can be added by referring to their parameters via the json file.

# Particle System
Referred to as `particle_system_data` in other JSON files.

`Particles` can be added by referring to their parameters via the json file.