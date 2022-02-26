## version 3.0.0
### New Features
1. Added `LightRoom`.
2. Added `rect_to_lines()`.
3. Added `Entity` events.
4. Added `raycast()`.
5. Reworked `eval_segment_intersection()`.
6. Added `collide_segments()`.
7. Added `draw_pie()`.
8. Removed need for `collision_rects` in `Scene.advance_frame()`.
9. Renamed `tests` folder to `examples`.
10. Removed inaccurate mouse presses in `Button`.
11. Added `Entity.alpha`.
12. Added `Clock.reset()`.
13. Added `Entity.ignore_collisions`

## version 2.5.0
### New Features
1. Added `Client.delta_time_modifier` to manipulate the game's clockspeed.
2. Added `Client.raw_delta_time` to fetch the client's delta time without modifiers.
3. Added `Entity.static_rect` which is a `pygame.Rect` that won't change size due to rotations.
4. Added `Entity.rotation_offset`.
5. Added `Entity.abs_position` and `Entity.abs_center_position`.
6. Added `Particles.obey_gravity`.
7. `RepeatEvent` can now have waiting periods between method calls.
8. Removed `Controller` in `Entity.update()` for a more customizable experience.
9. Default angle has been changed from `360 degrees` to `90 degrees` for `Entity` rotations
10. `Entity` sprites are now rotatable.

### Bug Fixes / Typing Fixes
1. Working `pygame.SCALED` replacement so that the `Client.screen` will no longer have black bars upon screen resize.
2. Fixed `Entity.move()` collisions.
3. Fixed `Button.is_pressing_mouseup()`.

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
11. `BaseController.movement`'s vector is normalized upon return.
12. Improvements to `Camera.shake()`.

### Bug Fixes / Typing Fixes
1. `._is_destroyed` has been renamed to `._destroy_queue` for all SakuyaEngine objects.
2. Renamed `spotlight()` to `light()`.
3. `Button` rewrite.
4. Complete `Wave` rewrite.
5. Added `pip install .`.
6. Removed the image requirement for `Entity`
7. `Scene` will no longer be loaded upon registration.
8. `Button.is_pressing_key` now works properly.
9. `Bullet.acceleration` is now typed properly.

### Optimizations
1. `Entity.custom_hitbox` has been optimized to be *50%* faster.
2. `Entity.center_offset` has been optimized.
3. `Entity.center_position` has been optimized.

## version 2.3.0
### New Features
1. Added `BulletSpawner.is_active`.
2. `BulletSpawner` can now aim at a target.
3. Removed `Bullet.sprite`.
4. `Particles` can be loaded in via `JSON`.
5. `Entity` can now load `Particles` via `JSON`.
6. `Bullet` can now be used without a loaded sprite.
7. `Entity.move()` collisions added.
8. `Entity.center_position` added.
9. `Camera` added.
10. `ScrollBackgroundSprite` added.

### Bug Fixes / Typing Fixes
1. Fixed a bug where the healthbar was not being copied in `Entity.copy()`.
2. `get_angle()` documentation rewrite.
3. `pygame.SCALED` flag added.
4. `Bullet.sprite` now rotates properly.
5. `Scene.is_paused` renamed to `Scene.paused`

### Optimizations
1. `SakuyaEngine.Vector` has been deprecated and has been replaced with `pygame.Vector2` boosting the fps of [Helix](https://github.com/novialriptide/Helix) by 200%.
2. `vector2_move_toward()` has been optimized.
3. `Entity.rect` has been optimized.
4. `Entity.custom_hitbox` has been optimized.
5. `Particles` object creation has been optimized.
6. `Particles.update()` has been optimized.
7. `text()` has been optimized.
8. `text2()` has been optimized.
9. `Entity.sprite` has been optimized to be *5%* faster.
10. `Bullet.sprite` optimizations.