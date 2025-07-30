from enum import Enum

from evdev import InputEvent
from evdev import ecodes as e


class KeyInput(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    A = 5
    B = 6
    X = 7
    Y = 8
    L = 9
    R = 10
    ZL = 11
    ZR = 12
    PLUS = 13
    MINUS = 14
    CAPTURE = 15
    HOME = 16
    LEFT_ANALOG_PRESS = 17
    RIGHT_ANALOG_PRESS = 18

    @staticmethod
    def from_string(string: str):
        all_names = [i.name for i in list(KeyInput)]
        if string.upper() in all_names:
            return KeyInput[string.upper()]
        else:
            return None

    @staticmethod
    def from_event(event: InputEvent):
        if event.type == e.EV_KEY:
            if event.code == e.BTN_EAST and event.value == 1:
                return KeyInput.A
            elif event.code == e.BTN_SOUTH and event.value == 1:
                return KeyInput.B
            elif event.code == e.BTN_NORTH and event.value == 1:
                return KeyInput.X
            elif event.code == e.BTN_WEST and event.value == 1:
                return KeyInput.Y
            elif event.code == e.BTN_TL and event.value == 1:
                return KeyInput.L
            elif event.code == e.BTN_TR and event.value == 1:
                return KeyInput.R
            elif event.code == e.BTN_TL2 and event.value == 1:
                return KeyInput.ZL
            elif event.code == e.BTN_TR2 and event.value == 1:
                return KeyInput.ZR
            elif event.code == e.BTN_START and event.value == 1:
                return KeyInput.PLUS
            elif event.code == e.BTN_SELECT and event.value == 1:
                return KeyInput.MINUS
            elif event.code == e.BTN_Z and event.value == 1:
                return KeyInput.CAPTURE
            elif event.code == e.BTN_MODE and event.value == 1:
                return KeyInput.HOME
            elif event.code == e.BTN_THUMBL and event.value == 1:
                return KeyInput.LEFT_ANALOG_PRESS
            elif event.code == e.BTN_THUMBR and event.value == 1:
                return KeyInput.RIGHT_ANALOG_PRESS
            else:
                return None
        elif event.type == e.EV_ABS:
            if event.code == e.ABS_HAT0Y and event.value == -1:
                return KeyInput.UP
            elif event.code == e.ABS_HAT0Y and event.value == 1:
                return KeyInput.DOWN
            elif event.code == e.ABS_HAT0X and event.value == -1:
                return KeyInput.LEFT
            elif event.code == e.ABS_HAT0X and event.value == 1:
                return KeyInput.RIGHT
            else:
                return None
        else:
            return None


class AnalogInput(Enum):
    LEFT = 1
    RIGHT = 2

    @staticmethod
    def from_string(string: str):
        all_names = [i.name for i in list(AnalogInput)]
        if string.upper() in all_names:
            return AnalogInput[string.upper()]
        else:
            return None

    @staticmethod
    def from_event(event: InputEvent):
        if event.type == e.EV_ABS:
            if event.code == e.ABS_X or event.code == e.ABS_Y:
                return AnalogInput.LEFT
            elif event.code == e.ABS_RX or event.code == e.ABS_RY:
                return AnalogInput.RIGHT


type Input = KeyInput | AnalogInput


#######################################################################


class KeyboardTarget:
    def __init__(self, ecodes):
        self.ecodes = ecodes


class MouseTarget(Enum):
    CURSOR = 1
    SCROLL = 2


class CommandTarget:
    def __init__(self, command: str):
        self.command = command


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class CursorDirectionTarget:
    def __init__(self, direction: Direction, pixel: int):
        self.direction = direction
        self.pixel = pixel


class ScrollDirectionTarget:
    def __init__(self, direction: Direction, speed: int):
        self.direction = direction
        self.speed = speed


type Target = (
    KeyboardTarget
    | MouseTarget
    | CommandTarget
    | CursorDirectionTarget
    | ScrollDirectionTarget
)


#######################################################################


class Mapper:
    def __init__(self):
        self.mapping = {}

    def insert(self, input: Input, target: Target):
        self.mapping[input] = target

    def translate(self, input: Input) -> Target | None:
        if input in self.mapping.keys():
            return self.mapping[input]
        else:
            return None
