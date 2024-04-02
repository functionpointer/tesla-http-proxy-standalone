#! /usr/bin/env python3

import ssl
import aiohttp
from pathlib import Path
import asyncio

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(Path("./certs/tls-cert.pem"))


async def main():
  async with aiohttp.ClientSession() as session:
    async with session.get("https://localhost:4448", ssl_context=ssl_context) as resp:
      print(resp.status)
      print(await resp.text())

asyncio.run(main())
