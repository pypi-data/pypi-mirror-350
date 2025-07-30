"""This module contains the main loop for updating sprites and running their events."""

import math as _math

from .mouse_loop import mouse_state
from ..callback import callback_manager, CallbackType
from ..callback.callback_helpers import run_callback, run_async_callback
from ..globals import globals_list
from ..io.screen import convert_pos, PYGAME_DISPLAY
from ..io.mouse import mouse
from ..objects.line import Line
from ..objects.sprite import point_touching_sprite


async def _update_sprites(do_events: bool = True):  # pylint: disable=too-many-branches
    # pylint: disable=too-many-nested-blocks
    globals_list.sprites_group.update()

    for sprite in globals_list.sprites_group.sprites():
        ######################################################
        # update sprites with results of physics simulation
        ######################################################
        if sprite.physics and sprite.physics.can_move:
            body = sprite.physics._pymunk_body
            angle = _math.degrees(body.angle)
            if isinstance(sprite, Line):
                sprite._x = body.position.x - (sprite.length / 2) * _math.cos(angle)
                sprite._y = body.position.y - (sprite.length / 2) * _math.sin(angle)
                sprite._x1 = body.position.x + (sprite.length / 2) * _math.cos(angle)
                sprite._y1 = body.position.y + (sprite.length / 2) * _math.sin(angle)
                # sprite._length, sprite._angle = sprite._calc_length_angle()
            else:
                if (
                    str(body.position.x) != "nan"
                ):  # this condition can happen when changing sprite.physics.can_move
                    sprite._x = body.position.x
                if str(body.position.y) != "nan":
                    sprite._y = body.position.y

            sprite.angle = (
                angle  # needs to be .angle, not ._angle so surface gets recalculated
            )
            sprite.physics._x_speed, sprite.physics._y_speed = body.velocity

        sprite._is_clicked = False
        if sprite.is_hidden:
            continue

        if not do_events and not sprite.physics:
            continue

        #################################
        # All @sprite.when_touching events
        #################################
        if sprite._touching_callback[0]:
            await run_async_callback(sprite._touching_callback[0], [], [])
        if sprite._touching_callback[1]:
            await run_async_callback(sprite._touching_callback[1], [], [])

        #################################
        # @sprite.when_clicked events
        #################################
        if mouse.is_clicked:
            if (
                point_touching_sprite(convert_pos(mouse.x, mouse.y), sprite)
                and mouse_state.click_happened_this_frame
            ):
                # only run sprite clicks on the frame the mouse was clicked
                sprite._is_clicked = True
                if callback_manager.get_callback(
                    CallbackType.WHEN_CLICKED_SPRITE, id(sprite)
                ):
                    for callback in callback_manager.get_callback(
                        CallbackType.WHEN_CLICKED_SPRITE, id(sprite)
                    ):
                        if not callback.is_running:
                            run_callback(
                                callback,
                                [],
                                [],
                            )

    globals_list.sprites_group.update()
    globals_list.sprites_group.draw(PYGAME_DISPLAY)
