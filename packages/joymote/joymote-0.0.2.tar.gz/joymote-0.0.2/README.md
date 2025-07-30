# Joymote

Use Joy-Con or Pro Controller as remote control of Linux machine.

> Currently, only support Pro Controller. We are working on supporting Joy-Con.

## Requirements

- [joycond](https://github.com/DanielOgorchock/joycond)
  - Install and start. For example, if you are on Arch Linux, you can run

    ```bash
    yay -S joycond-git
    sudo systemctl enable --now joycond
    ```

  - Then, follow [this instruction](https://github.com/DanielOgorchock/joycond?tab=readme-ov-file#usage) to pair the controller(s).
- [uinput module](https://www.kernel.org/doc/html/v4.12/input/uinput.html)
  - Check whether the `uinput` module is loaded, by running:

    ```bash
    lsmod | grep uinput
    ```

    If it is loaded, you will see a line like `uinput                 20480  0`.
  - You can manually load the module by running:

    ```bash
    sudo modprobe uinput
    ```

  - You can also run the following command to load `uinput` modules automatically on boot.

    ```bash
    sudo bash -c "cat uinput > /etc/modules-load.d/uinput.conf"
    ```

## Installation

## Usage

## Run development build

We use [uv](https://docs.astral.sh/) to manage this project.

1. Clone the repository.

    ```bash
    git clone https://github.com/kkoyung/joymote.git
    ```

2. Run the code.

    ```bash
    uv run joymote
    ```

## Disclaimer

Nintendo®, Nintendo Switch®, Joy-Con®, and Pro Controller® are registered trademarks of Nintendo of America Inc. This project is an independent work and is not affiliated with, endorsed by, or sponsored by Nintendo. All trademarks are the property of their respective owners.
