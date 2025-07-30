import logging

import evdev

from .config import Config
from .reactor import Reactor

logger = logging.getLogger(__name__)


def scan_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # FIXME: What is "Pro Controller (IMU)"?
    devices = list(filter(lambda device: device.name == "Pro Controller", devices))
    for device in devices:
        logger.info("Detected device: %s, %s", device.path, device.name)

    return devices


def start_capture(device, conf: Config):
    reactor = Reactor(conf)

    logger.info("Start capturing device: %s, %s", device.path, device.name)
    try:
        for event in device.read_loop():
            reactor.push(event)
    except KeyboardInterrupt:
        logger.info("Stop capturing device: %s, %s", device.path, device.name)
        device.close()
