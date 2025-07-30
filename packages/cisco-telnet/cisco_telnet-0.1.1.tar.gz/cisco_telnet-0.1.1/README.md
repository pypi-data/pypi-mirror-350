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
        password="your_password",
        enable_pass="your_enable_password"  # Optional, if required
    )

asyncio.run(main())
```

## Example integration

You can also use this module as part of a larger automation script, for example:

```python
from cisco_telnet import apply_telnet_config
import asyncio

commands = [
    "hostname TestRouter",
    "interface Loopback0",
    "ip address 10.1.1.1 255.255.255.255"
]

asyncio.run(apply_telnet_config(commands, "10.0.0.1", "admin", "password"))
```
**Parameter explanation:**

- `username="admin"` — username for Telnet login to the Cisco device.
- `password="your_password"` — password for Telnet login.
- `enable_pass="your_enable_password"` — enable mode password (optional, if required).

## License

MIT License