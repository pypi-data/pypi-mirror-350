#!/usr/bin/python

import argparse
import logging
import os
import pathlib

from joymote import config, engine, version


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Use Joy-Con or Pro Controller as remote control of Linux machine.",
        add_help=False,
    )
    parser.add_argument(
        "-h", "--help", help="Show this help message and exit.", action="help"
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Print version information.",
        action="version",
        version=version.get_version(),
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Path to config file. Default: $XDG_CONFIG_HOME/.config/joymote/config.toml",
        nargs=1,
        default=None,
        type=pathlib.Path,
    )
    args = parser.parse_args()

    # Set up logger
    logger = logging.getLogger(__name__)

    # Load configuration
    if args.config is None:
        home_directory = os.getenv("HOME", "/root")
        xdg_config_home = os.getenv("XDG_CONFIG_HOME", home_directory + "/.config")
        config_path = xdg_config_home + "/joymote/config.toml"
    else:
        config_path = args.config[0]
    conf = config.Config(config_path)

    # Start main body
    devices = engine.scan_devices()
    if len(devices) == 0:
        logger.warning("Not detected device")
        exit()
    for device in devices:
        engine.start_capture(device, conf)


if __name__ == "__main__":
    main()
