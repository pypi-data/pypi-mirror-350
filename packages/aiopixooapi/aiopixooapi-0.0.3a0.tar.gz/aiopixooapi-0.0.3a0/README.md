
# AioPixooAPI

A Python library for interacting with Divoom Pixoo devices and the Divoom online API.

## Installation

Install the library using pip:

```bash
pip install aiopixooapi
```

## Usage

### Pixoo64 (Device API)

The `Pixoo64` class is used to interact with a Pixoo64 device on your local network.

```python
import asyncio
from aiopixooapi.pixoo64 import Pixoo64

async def main():
    async with Pixoo64("192.168.1.100") as pixoo:
        # Reboot the device
        response = await pixoo.sys_reboot()
        print(response)

        # Get all settings
        settings = await pixoo.get_all_settings()
        print(settings)

asyncio.run(main())
```

### Divoom (Online API)

The `Divoom` class is used to interact with the Divoom online API.

```python
import asyncio
from aiopixooapi.divoom import Divoom

async def main():
    async with Divoom() as divoom:
        # Get dial types
        dial_types = await divoom.get_dial_type()
        print(dial_types)

        # Get dial list for a specific type and page
        dial_list = await divoom.get_dial_list("Social", 1)
        print(dial_list)

asyncio.run(main())
```

## Development
### Setup
To set up the development environment, clone the repository, create a virtual environment and install the required packages

```bash
pip install -e .
pip install -e .[test]
```

### Testing

Run the tests using `pytest`:

```bash
pytest
```

## License

This project is licensed under the MIT License.
