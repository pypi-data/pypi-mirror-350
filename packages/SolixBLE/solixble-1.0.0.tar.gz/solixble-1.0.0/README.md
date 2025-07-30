# SolixBLE

[![PyPI Status](https://img.shields.io/pypi/v/SolixBLE.svg)](https://pypi.python.org/pypi/SolixBLE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python module for monitoring Anker Solix power stations over Bluetooth.
 - 👌 Free software: MIT license
 - 🍝 Sauce: https://github.com/flip-dots/SolixBLE
 - 📦 PIP: https://pypi.org/project/SolixBLE/


This Python module enables you to monitor Anker Solix devices directly
from your computer, without the need for any cloud services or Anker app.
It leverages the Bleak library to interact with Bluetooth Anker Solix power stations.
No pairing is required in order to receive telemetry data.


## Features

- 🔋 Battery percentage
- ⚡ Total Power In/Out
- 🔌 AC Power In/Out
- 🚗 DC Power In/Out
- ⏰ AC/DC Timer value
- ⏲️ Time remaining to full/empty
- ☀️ Solar Power In
- 📱 USB Port Status
- 💡 Light bar status
- 🔂 Simple structure
- ✔️ More emojis than strictly necessary


## Supported Devices

- C300X
- Maybe more? IDK


## Requirements

- 🐍 Python 3.11+
- 📶 Bleak 0.19.0+
- 📶 bleak-retry-connector


## Supported Operating Systems

- 🐧 Linux (BlueZ)
  - Ubuntu Desktop
  - Arch (HomeAssistant OS)
- 🏢 Windows
  - Windows 10 
- 💾 Mac OSX
  - Maybe?


## Installation


### PIP

```
pip install SolixBLE
```


### Manual

SolixBLE consists of a single file (SolixBLE.py) which you can simply put in the
same directory as your program. If you are using manual installation make sure
the dependencies are installed as well.

```
pip install bleak bleak-retry-connector
```
