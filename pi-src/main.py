#!/usr/bin/env python3

import sys
import asyncio
import subprocess
import multiprocessing as mp

# Local Modules
from asyncserver import asyncserver
from webserver import webserver
from transcribe import transcribe


# TODO: Handle exceptions when a device disconnects
# sudo_v_cmd = ['sudo', '-v']
# command = ['sudo', 'create_ap', '--no-virt', '-g', asyncserver.HOST_IP, 'wlp0s20f0u6', 'wlp170s0', 'wiredliving', 'livingwired']


async def monitor_event(event: asyncio.Event, func: callable, *args):
    while True:
        await event.wait()
        # response = await func()
        response = await func(*args)
        event.clear()
        print("Resetting Event")


async def handle_new_connections(q: asyncio.Queue):
    while True:
        # Will probably need to add a try catch here
        addr = await q.get()
        event_task = asyncio.create_task(monitor_event(webserver.button_event, asyncserver.toggle, addr))


async def main():
    # subprocess.run(sudo_v_cmd)
    # process = subprocess.Popen(command)
    # print("Process started with PID:", process.pid)
    # await asyncio.sleep(5)

    server_task = asyncio.create_task(asyncserver.start_server())
    web_task = asyncio.create_task(webserver.start_server())

    connection_handler_task = asyncio.create_task(handle_new_connections(asyncserver.new_clients))

    mp.set_start_method("spawn")
    audio_queue = mp.Queue()
    output_queue = mp.Queue()

    record_proc = mp.Process(target=transcribe.record, args=(audio_queue,))
    transcribe_proc = mp.Process(target=transcribe.transcribe, args=(audio_queue, output_queue,))

    record_proc.start()
    transcribe_proc.start()

    while True:
        if not output_queue.empty():
            result = output_queue.get()
            if result == "SET_ON":
                webserver.button_event.set()
            elif result == "SET_OFF":
                webserver.button_event.set()

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
