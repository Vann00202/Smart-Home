#!/usr/bin/env python3

import sys
import asyncio
import signal

# Local Modules
from asyncserver import asyncserver
from webserver import webserver


async def main():

    server_task = asyncio.create_task(asyncserver.start_server())
    web_task = asyncio.create_task(webserver.start_server())

    # Start multiprocessing for voice recoginition here
    await webserver.button_event.wait()
    print("Button was pressed")

    try:
        await web_task
        await server_task
    except asyncio.CancelledError:
        print("Cancelled")


if __name__ == "__main__":

    asyncio.run(main())

    sys.exit(0)
