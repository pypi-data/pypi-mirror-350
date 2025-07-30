# aiopixooapi

An asynchronous Python library for controlling Divoom Pixoo64 LED display devices.

## Installation

```bash
pip install aiopixooapi
```

## Quick Start

```python
import asyncio
from aiopixooapi import Pixoo


async def main():
    # Connect to your Pixoo64 device
    async with Pixoo("192.168.1.100") as pixoo:  # Replace with your device's IP address
        await pixoo.get_all_settings()


if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

http://docin.divoom-gz.com/web/#/5/23

### Sources used

#### Divoom

* https://divoom.com/apps/help-center#hc-pixoo64developeropen-sourcesdkapiopen-source

That gives us:

* http://doc.divoom-gz.com/web/#/12?page_id=89

Where the contact page:

* http://doc.divoom-gz.com/web/#/12?page_id=143

Send us to

* http://docin.divoom-gz.com/web/#/5/23

OLDER REFERENCES

* http://doc.divoom-gz.com/web/#/12
* http://doc.divoom-gz.com/web/#/7
* http://doc.divoom-gz.com/web/#/5

## Running Tests

To install test dependencies (including pytest):

```bash
pip install .[test]
```

To run the tests using pytest, execute:

```bash
pytest
```

Or to run tests in a specific file:

```bash
pytest tests/test_pixoo.py
```

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the LICENSE file for details.
