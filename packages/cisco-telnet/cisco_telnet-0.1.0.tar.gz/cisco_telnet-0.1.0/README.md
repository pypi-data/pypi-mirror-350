# cisco_telnet

A Python module for applying Telnet configurations to Cisco devices.

## Features

- Connects to Cisco devices via Telnet
- Authenticates with username and password
- Enters enable and configuration modes
- Sends a list of configuration commands
- Prints device responses

## Installation

```sh
pip install cisco_telnet
```

## Usage

```python
import asyncio
from cisco_telnet import apply_telnet_config

commands = [
    "interface FastEthernet0/1",
    "description Connected to Server",
    "no shutdown"
]

async def main():
    await apply_telnet_config(
        commands,
        host="192.168.1.1",
        username="admin",
        password="your_password"
    )

asyncio.run(main())
```

## License

MIT License