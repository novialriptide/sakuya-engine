# SakuyaEngine .wave Documentation
## Commands
```
spawn <entity_key> <spawnpoint_key> <spawn_animation_key> <lifetime>
    Spawn an entity at a spawn point. If lifetime is 0, 
    it will live forever until its health runs out.

    Example:
        spawn 4 2 0 2000
        spawn 0 6 0 0
        spawn 9 0 1 1000

wait <milliseconds>
    Time to wait to resume commands

    Example:
        wait 3000
        wait 1500
```