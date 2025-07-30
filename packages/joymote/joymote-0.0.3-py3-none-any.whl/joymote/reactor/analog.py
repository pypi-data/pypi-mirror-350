import logging
import threading
from math import atan, cos, sin
from time import sleep

from evdev import InputEvent, UInput
from evdev import ecodes as e

logger = logging.getLogger(__name__)


class BaseThread(threading.Thread):
    def __init__(self, ui: UInput):
        threading.Thread.__init__(self, daemon=True)

        self.ui = ui
        self.step_time = 0.02
        self.step_factor = 0.001
        self.center_threshold = 3600
        self.stopping_event = threading.Event()
        self.x = 0
        self.y = 0

    def run(self):
        while True:
            self.step()
            sleep(self.step_time)

            if self.stopping_event.is_set():
                break

    def step(self):
        logger.debug("BaseThread make a step: x=%d, y=%d", self.x, self.y)

    def push(self, event: InputEvent):
        if event.type == e.EV_ABS:
            if event.code == e.ABS_X or event.code == e.ABS_RX:
                self.x = event.value
            elif event.code == e.ABS_Y or event.code == e.ABS_RY:
                self.y = event.value
        else:
            logger.error("Pushed non-AbsEvent to BaseThread")
            return

        if self.x**2 + self.y**2 > self.center_threshold**2:
            # Restart the thread if it has stopped
            if not self.is_alive():
                threading.Thread.__init__(self, daemon=True)
                self.stopping_event.clear()
                self.start()
        else:
            # Stop the thread
            self.stopping_event.set()


class CursorThread(BaseThread):
    def __init__(self, ui: UInput, speed: float = 1.0, idle_range: float = 1.0):
        super().__init__(ui)
        self.step_factor *= float(speed)
        self.center_threshold *= float(idle_range)

    def step(self):
        logger.debug("CursorThread make a step: x=%d, y=%d", self.x, self.y)

        if self.x == 0:
            self.x = 1  # set to 1 to avoid division of zero

        rel_x = int(
            (self.x - self.center_threshold * cos(atan(self.y / self.x)))
            * self.step_factor
        )
        rel_y = int(
            (self.y - self.center_threshold * sin(atan(self.y / self.x)))
            * self.step_factor
        )
        self.ui.write(e.EV_REL, e.REL_X, rel_x)
        self.ui.write(e.EV_REL, e.REL_Y, rel_y)
        self.ui.syn()


class ScrollThread(BaseThread):
    def __init__(
        self,
        ui: UInput,
        speed: float = 1.0,
        idle_range: float = 1.0,
        revert_x: bool = False,
        revert_y: bool = False,
    ):
        super().__init__(ui)
        self.step_factor *= float(speed)
        self.center_threshold *= float(idle_range)
        self.revert_x = revert_x
        self.revert_y = revert_y

    def step(self):
        logger.debug("ScrollThread make a step: x=%d, y=%d", self.x, self.y)

        if self.x == 0:
            self.x = 1  # set to 1 to avoid division of zero

        rel_x = int(
            (self.x - self.center_threshold * cos(atan(self.y / self.x)))
            * self.step_factor
        )
        rel_y = int(
            (self.y - self.center_threshold * sin(atan(self.y / self.x)))
            * self.step_factor
        )

        if self.revert_x:
            rel_x = -rel_x
        if self.revert_y:
            rel_y = -rel_y

        self.ui.write(e.EV_REL, e.REL_HWHEEL_HI_RES, rel_x)
        self.ui.write(e.EV_REL, e.REL_WHEEL_HI_RES, -rel_y)
        self.ui.syn()
