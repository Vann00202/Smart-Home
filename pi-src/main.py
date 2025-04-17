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


    try:
        await web_task
        await server_task
    except asyncio.CancelledError:
        print("Cancelled")


if __name__ == "__main__":

    # asyncserver.start_server()
    # webserver.app.run(host='0.0.0.0', port=3000)
    asyncio.run(main())

    sys.exit(0)
