#!/usr/bin/env python3

from aiohttp import web
import aiohttp_cors
import asyncio


class WebserverListener:

    _button_toggle_event = None
    _button_on_event = None
    _button_off_event = None

    _status = 2

    async def button_toggle(request):
        global _status
        if _button_toggle_event is not None:
            _button_toggle_event.set()
            if _status == 1:
                _status = 0
            elif _status == 0:
                _status = 1
            else:
                _status = 2
            
        # Return a JSON response
        return web.json_response({"status": "success"})

    async def button_on(request):
        global _status
        if _button_on_event is not None:
            _button_on_event.set()
            _status = 0
        # Return a JSON response
        return web.json_response({"status": "success"})

    async def button_off(request):
        global _status
        if _button_off_event is not None:
            _button_off_event.set()
            _status = 1
        # Return a JSON response
        return web.json_response({"status": "success"})
    
    
    async def button_status(request):
        global _status
        # if _button_off_event is not None:
        #     _button_off_event.set()
        return web.json_response(_status)
        if _status == 0:
            return web.json_response({"status": "ON"})
        elif _status == 1:
            return web.json_response({"status": "OFF"})
        else:
            return web.json_response({"status": "Undetermined"})

        # Return a JSON response
        # return web.json_response(_status)

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
        cors.add(app.router.add_post('/button-pressed', WebserverListener.button_toggle), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        cors.add(app.router.add_post('/button-pressed-on', WebserverListener.button_on), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        cors.add(app.router.add_post('/button-pressed-off', WebserverListener.button_off), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        cors.add(app.router.add_post('/button-status', WebserverListener.button_status), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        await web._run_app(app, host='0.0.0.0', port=3000)


# Run the server on all IPs (0.0.0.0) and port 3000
if __name__ == '__main__':
    asyncio.run(WebserverListener.start_server())
