#!/usr/bin/env python3

from aiohttp import web
import aiohttp_cors
import asyncio


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
        data = f"data: {datetime.now()}\n\n"
        await response.write(data.encode('utf-8'))
        await asyncio.sleep(1)

    return response

app1 = web.Application()
app1.router.add_get('/sse', sse_handler)
web.run_app(app1)





button_event = asyncio.Event()


async def button_pressed(request):
    if button_pressed_event is not None:
        button_pressed_event.set()
    # Return a JSON response
    return web.json_response({"status": "success"})


async def start_server(toggle_event: asyncio.Event):
    button_pressed_event = toggle_event
    button_pressed_event.clear()

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
    cors.add(app.router.add_post('/button-pressed-on', button_pressed), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    cors.add(app.router.add_post('/button-pressed-off', button_pressed), {
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