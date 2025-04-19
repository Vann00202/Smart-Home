#!/usr/bin/env python3

import sys
import asyncio

# Local Modules
from asyncserver import asyncserver
from webserver import webserver


async def monitor_event(event: asyncio.Event, func: callable):
    while True:
        await event.wait()
        print("Button")
        # Something on the arduino side is causing it to not respond a second time
        await func
        event.clear()
        print("Resetting Event")


async def main():

    server_task = asyncio.create_task(asyncserver.start_server())
    web_task = asyncio.create_task(webserver.start_server())

    await asyncio.sleep(3)
    result = asyncserver.get_connected()
    addr = result[0]

    event_task = asyncio.create_task(monitor_event(webserver.button_event, asyncserver.set_on(addr)))

    # Start multiprocessing for voice recoginition here

    try:
        await web_task
        await server_task
    except asyncio.CancelledError:
        print("Cancelled")


if __name__ == "__main__":

    asyncio.run(main())

    sys.exit(0)
