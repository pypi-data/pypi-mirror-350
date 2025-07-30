[![Build, test and publish](https://github.com/happydev-ca/spypoint-api/actions/workflows/publish.yml/badge.svg)](https://github.com/happydev-ca/spypoint-api/actions/workflows/publish.yml)

# spypoint-api

Library to communicate with Spypoint REST API.

## Usage

```python
import aiohttp
import asyncio
import os

from spypointapi import SpypointApi


async def run():
    async with aiohttp.ClientSession() as session:
        api = SpypointApi(os.environ['EMAIL'], os.environ['PASSWORD'], session)

        cameras = await api.async_get_cameras()
        for camera in cameras:
            print(camera)


asyncio.run(run())
```

### Build and test locally

```shell
make install
make test
make build
```

### Release version

```shell
make release bump=patch|minor|major
```