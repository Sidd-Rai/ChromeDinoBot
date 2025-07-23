# Chrome Dino Bot

Automate playing the Chrome Dino game using computer vision and keyboard automation.

## Features

- Detects obstacles in the Dino game using screen region scanning.
- Automatically jumps over obstacles.
- Adjustable scan region via a GUI selector.
- Supports dynamic scan box shifting as game speed increases.
- Start bot with a spacebar cue (`BotCuedStart.py`) or immediately (`Bot.py`).

## Files

- [`Bot.py`](Bot.py): Bot starts as soon as you run the script .
- [`BotCuedStart.py`](BotCuedStart.py): Bot waits for spacebar before starting, so that it can start simultaneously with the dino game.
- [`ScanRegionSelector.py`](ScanRegionSelector.py): GUI tool to select and save scan region.
- [`scanBoxCoordinates.json`](scanBoxCoordinates.json): Stores scan region coordinates.
- `.gitignore`: Ignores `venv` folder.

## Requirements

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/)
- [numpy](https://pypi.org/project/numpy/)
- [pyautogui](https://pypi.org/project/pyautogui/)
- [pynput](https://pypi.org/project/pynput/) (for `BotCuedStart.py`)

Install dependencies:
```sh
pip install Pillow numpy pyautogui pynput
