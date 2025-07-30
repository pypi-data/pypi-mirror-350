# Joymote

Use Joy-Con or Pro Controller as remote control of Linux machine.

> Currently, only support Pro Controller. We are working on supporting Joy-Con.

## Requirements

- [Python](https://www.python.org)
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

  - Make sure you have the permission to access `/dev/uinput`.

## Installation

### Using pip

```bash
pip install joymote
```

### From source

```bash
git clone https://github.com/kkoyung/joymote.git joymote
cd joymote
# check out different version by tags
pip install .
```

## Usage

1. Copy the example configuration file to `~/.config/joymote/config.toml`.

    ```bash
    wget -o ~/.config/joymote/config.toml https://raw.githubusercontent.com/kkoyung/joymote/refs/heads/main/config.toml
    ```

2. Connect to the controller via Bluetooth, just like usual Bluetooth devices. Tips: Press and hold down the tiny button between ZL and ZR buttons, for at least one second to enter pairing mode.
3. Run `joymote`.

    ```bash
    joymote
    ```

4. By default, joymote does nothing. Check out `config.toml` and change it to configure joymote's behaviours.

## Development

1. Clone the repository.

    ```bash
    git clone https://github.com/kkoyung/joymote.git joymote
    cd joymote
    ```

2. Run the code.

    ```bash
    uv run joymote
    # or
    python -m venv .venv
    source .venv/bin/activate
    python install .
    python -m joymote
    ```

## Pairing two Joy-Con as one device

Use [joycond](https://github.com/DanielOgorchock/joycond), which is a userspace daemon, to combine Joy-Cons into a single device.

- Install and start. For example, if you are on Arch Linux, you can run

  ```bash
  yay -S joycond-git
  sudo systemctl enable --now joycond
  ```

- Then, follow [this instruction](https://github.com/DanielOgorchock/joycond?tab=readme-ov-file#usage) to pair the controller.

## Disclaimer

Nintendo®, Nintendo Switch®, Joy-Con®, and Pro Controller® are registered trademarks of Nintendo of America Inc. This project is an independent work and is not affiliated with, endorsed by, or sponsored by Nintendo. All trademarks are the property of their respective owners.
