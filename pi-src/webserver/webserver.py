#!/usr/bin/env python3

from aiohttp import web
import aiohttp_cors
import asyncio


_button_toggle_event = None
_button_on_event = None
_button_off_event = None

status = "Undetermined"


async def sse_handler(request):
    response = web.StreamResponse(
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    )
    await response.prepare(request)

    while True:
        if _button_toggle_event is not None:
            data = f"{status}\n\n"
            await response.write(data.encode('utf-8'))
        await asyncio.sleep(1)


app1 = web.Application()
app1.router.add_get('/sse', sse_handler)
web.run_app(app1)


async def button_toggle(request):
    if _button_toggle_event is not None:
        _button_toggle_event.set()
    # Return a JSON response
    return web.json_response({"status": "success"})


async def button_on(request):
    if _button_on_event is not None:
        _button_on_event.set()
    # Return a JSON response
    return web.json_response({"status": "success"})


async def button_off(request):
    if _button_off_event is not None:
        _button_off_event.set()
    # Return a JSON response
    return web.json_response({"status": "success"})


async def start_server(toggle_event: asyncio.Event, on_event: asyncio.Event, off_event: asyncio.Event):
    global _button_toggle_event, _button_on_event, _button_off_event

    _button_toggle_event = toggle_event
    _button_on_event = on_event
    _button_off_event = off_event

    _button_toggle_event.clear()
    _button_on_event.clear()
    _button_off_event.clear()

    app = web.Application()
    cors = aiohttp_cors.setup(app)

    # Setup CORS for the route
    cors.add(app.router.add_post('/button-pressed', button_toggle), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    cors.add(app.router.add_post('/button-pressed-on', button_on), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    cors.add(app.router.add_post('/button-pressed-off', button_off), {
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
    #!/usr/bin/env python3
