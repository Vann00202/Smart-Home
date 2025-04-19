#!/usr/bin/env python3

from aiohttp import web
import aiohttp_cors
import asyncio


button_event = asyncio.Event()


async def button_pressed(request):
    button_event.set()
    # Return a JSON response
    return web.json_response({"status": "success"})


async def start_server():
    button_event.clear()

    app = web.Application()
    cors = aiohttp_cors.setup(app)

    # Setup CORS for the route
    cors.add(app.router.add_post('/button-pressed', button_pressed), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    await web._run_app(app, host='0.0.0.0', port=3000)


# Run the server on all IPs (0.0.0.0) and port 3000
if __name__ == '__main__':
    asyncio.run(start_server())
