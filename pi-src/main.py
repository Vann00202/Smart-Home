#!/usr/bin/env python3

import sys
import asyncio
import multiprocessing as mp

# Local Modules
from asyncserver import asyncserver
from webserver import webserver
from transcribe import transcribe


toggle_event = asyncio.Event()
on_event = asyncio.Event()
off_event = asyncio.Event()


async def monitor_event(event: asyncio.Event, func: callable, *args):
    while True:
        await event.wait()
        response = await func(*args)
        event.clear()
        print("Resetting Event")


async def handle_new_connections(q: asyncio.Queue):
    while True:
        # Will probably need to add a try catch here
        addr = await q.get()
        event_task = asyncio.create_task(monitor_event(toggle_event, asyncserver.toggle, addr))
        event_task = asyncio.create_task(monitor_event(on_event, asyncserver.set_on, addr))
        event_task = asyncio.create_task(monitor_event(off_event, asyncserver.set_off, addr))


async def main():

    global toggle_event, on_event, off_event

    server_task = asyncio.create_task(asyncserver.start_server())
    web_task = asyncio.create_task(webserver.WebserverListener.start_server(toggle_event, on_event, off_event))

    connection_handler_task = asyncio.create_task(handle_new_connections(asyncserver.new_clients))

    mp.set_start_method("spawn")
    audio_queue = mp.Queue()
    output_queue = mp.Queue()

    record_proc = mp.Process(target=transcribe.record, args=(audio_queue,))
    transcribe_proc = mp.Process(target=transcribe.transcribe, args=(audio_queue, output_queue,))

    record_proc.start()
    transcribe_proc.start()


    while True:
        await asyncio.sleep(1)
        if not output_queue.empty():
            result = output_queue.get()
            if result == "SET_ON":
                on_event.set()
            elif result == "SET_OFF":
                off_event.set()
            elif result == "TOGGLE":
                toggle_event.set()

    record_proc.join()
    transcribe_proc.join()

    try:
        await web_task
        await server_task
    except asyncio.CancelledError:
        print("Cancelled")


if __name__ == "__main__":

    asyncio.run(main())

    sys.exit(0)
