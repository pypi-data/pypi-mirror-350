import subprocess

from evdev import InputEvent, UInput
from evdev import ecodes as e

from ..config import AnalogInput, Config, KeyInput, MouseTarget
from ..reactor.analog import CursorThread, ScrollThread
from ..util import (
    CommandTarget,
    CursorDirectionTarget,
    Direction,
    KeyboardTarget,
    ScrollDirectionTarget,
)


class Reactor:
    def __init__(self, conf: Config):
        self.conf = conf
        self.keyboard_ui = UInput()
        self.mouse_ui = UInput(
            {
                e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],
                e.EV_REL: [e.REL_X, e.REL_Y, e.REL_WHEEL_HI_RES, e.REL_HWHEEL_HI_RES],
            }
        )

        if self.conf.mapper.translate(AnalogInput.LEFT) == MouseTarget.CURSOR:
            cursor_idle_range = self.conf.options["left_analog_idle_range"]
        elif self.conf.mapper.translate(AnalogInput.RIGHT) == MouseTarget.CURSOR:
            cursor_idle_range = self.conf.options["right_analog_idle_range"]
        else:
            cursor_idle_range = 1.0

        if self.conf.mapper.translate(AnalogInput.LEFT) == MouseTarget.SCROLL:
            scroll_idle_range = self.conf.options["left_analog_idle_range"]
        elif self.conf.mapper.translate(AnalogInput.RIGHT) == MouseTarget.SCROLL:
            scroll_idle_range = self.conf.options["right_analog_idle_range"]
        else:
            scroll_idle_range = 1.0

        self.cursor_thread = CursorThread(
            self.mouse_ui,
            speed=self.conf.options["cursor_speed"],
            idle_range=cursor_idle_range,
        )
        self.scroll_thread = ScrollThread(
            self.mouse_ui,
            speed=self.conf.options["scroll_speed"],
            idle_range=scroll_idle_range,
            revert_x=self.conf.options["revert_scroll_x"],
            revert_y=self.conf.options["revert_scroll_y"],
        )

    def push(self, event: InputEvent):
        key_input = KeyInput.from_event(event)
        analog_input = AnalogInput.from_event(event)

        if key_input is not None:
            target = self.conf.mapper.translate(key_input)
            if isinstance(target, KeyboardTarget):
                self.keyboard_ui.write(e.EV_KEY, target.ecodes, 1)
                self.keyboard_ui.write(e.EV_KEY, target.ecodes, 0)
                self.keyboard_ui.syn()
            elif isinstance(target, CommandTarget):
                subprocess.Popen(target.command, stdout=subprocess.DEVNULL, shell=True)
            elif isinstance(target, CursorDirectionTarget):
                if target.direction == Direction.UP:
                    self.mouse_ui.write(e.EV_REL, e.REL_Y, -target.pixel)
                elif target.direction == Direction.DOWN:
                    self.mouse_ui.write(e.EV_REL, e.REL_Y, target.pixel)
                elif target.direction == Direction.LEFT:
                    self.mouse_ui.write(e.EV_REL, e.REL_X, -target.pixel)
                elif target.direction == Direction.RIGHT:
                    self.mouse_ui.write(e.EV_REL, e.REL_X, target.pixel)
                self.mouse_ui.syn()
            elif isinstance(target, ScrollDirectionTarget):
                if target.direction == Direction.UP:
                    self.mouse_ui.write(e.EV_REL, e.REL_WHEEL_HI_RES, target.speed)
                elif target.direction == Direction.DOWN:
                    self.mouse_ui.write(e.EV_REL, e.REL_WHEEL_HI_RES, -target.speed)
                elif target.direction == Direction.LEFT:
                    self.mouse_ui.write(e.EV_REL, e.REL_HWHEEL_HI_RES, -target.speed)
                elif target.direction == Direction.RIGHT:
                    self.mouse_ui.write(e.EV_REL, e.REL_HWHEEL_HI_RES, target.speed)
                self.mouse_ui.syn()

        elif analog_input is not None:
            target = self.conf.mapper.translate(analog_input)
            if target == MouseTarget.CURSOR:
                self.cursor_thread.push(event)
            elif target == MouseTarget.SCROLL:
                self.scroll_thread.push(event)
