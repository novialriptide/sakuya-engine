## version 2.5.0
### New Features
1. Added `Client.delta_time_modifier` to manipulate the game's clockspeed.
2. Added `Client.raw_delta_time` to fetch the client's delta time without modifiers.
3. Added `Entity.static_rect` which is a `pygame.Rect` that won't change size due to rotations.

### New Improvements
1. Working `pygame.SCALED` replacement so that the `Client.screen` will no longer have black bars upon screen resize.
2. `Entity` sprites are now rotatable.
3. Fixed `Entity.move()` collisions

## version 2.4.0
### New Features
1. Added `Entity.target_position` for simpler movement.
2. Added `Entity.destroy_position`.
3. Added `EnlargingCircle` effect.
4. Added `Rain` effect.
5. Added `shadow()` to add a shadow effect.
6. Added `Entity.disable_bulletspawner_while_movement`.
7. Added `Bullet.sound_upon_fire`.
8. Added `Client.debug_caption` to view FPS, active `Scene`s, `Entity` + `Bullet` count, and more.
9. Added `Scene.screen` for easy draw management.
10. Added `Entity.points_upon_death`.

### New Improvements / Bug Fixes / Typing Fixes
1. `BaseController.movement`'s vector is normalized upon return.
2. Improvements to `Camera.shake()`.
3. `._is_destroyed` has been renamed to `._destroy_queue` for all SakuyaEngine objects.
4. Renamed `spotlight()` to `light()`.
5. `Button` rewrite.
6. Complete `Wave` rewrite.
8. Added `pip install .`.
9. Removed the image requirement for `Entity`
10. `Scene` will no longer be loaded upon registration.
11. `Button.is_pressing_key` now works properly.
12. `Bullet.acceleration` is now typed properly.

### Optimizations
1. `Entity.custom_hitbox` has been optimized to be *50%* faster.
2. `Entity.center_offset` has been optimized.
3. `Entity.center_position` has been optimized.