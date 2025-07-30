# PySilentWave

![PyPI](https://img.shields.io/pypi/v/pysilentwave)
![Publish to PyPI](https://github.com/thesilentwave/pysilentwave/actions/workflows/publish.yml/badge.svg)




API client for TheSilentWave devices.

## Installation

```bash
pip install pysilentwave
```

## Usage

```python
import asyncio
from pysilentwave import SilentWaveClient

async def main():
    client = SilentWaveClient("192.168.1.100")
    status = await client.get_status()
    print(f"Device status: {status}")

asyncio.run(main())
```

## Requirements

- Python 3.9 or higher
- aiohttp 3.8.0 or higher

## License

MIT
