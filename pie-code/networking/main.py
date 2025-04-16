#!/usr/bin/env python3

import sys
import asyncio

HOST_IP = "192.168.12.1"
PORT = 18000
MESSAGE_TYPES = {
    "GET_STATE": "GET_STATE\n",
    "SET_ON": "SET_ON\n",
    "SET_OFF": "SET_OFF\n"
}

clients = {}


# Private methods -----------------------------------------

async def _handle_connection(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    # request_queue = asyncio.Queue()
    # clients[addr] = (writer, request_queue)
    clients[addr] = (writer, reader)

    try:
        while True:
            # Maybe we send a keep alive signal periodically
            await asyncio.sleep(1)
            # request = await request_queue.get()

            # print(f"Sending request to client: {request}")
            # writer.write(request.encode())
            # await writer.drain()  # Wait for the data to be sent

            # Wait for the client to respond
            # data = await reader.read(100)
            # response = data.decode()
            # print(f"Received response from client: {response}")

    except asyncio.CancelledError:
        print(f"Connection from {addr} was cancelled.")
    finally:
        # Remove client from active connections on disconnect
        if addr in clients:
            del clients[addr]
        writer.close()
        await writer.wait_closed()
        print(f"Connection from {addr} closed")


# Sends data and returns the response
async def _send_request(addr, request):
    if addr in clients:
        writer, reader = clients[addr]
        print(f"Sending request to client: {request}")
        writer.write(request.encode())
        await writer.drain()  # Wait for the data to be sent

        # Wait for the client to respond
        data = await reader.read(100)
        response = data.decode()
        print(f"Received response from client: {response}")

        return response
    else:
        print(f"{addr} not connected")
        return None


# Public methods -----------------------------------------

async def send_update(addr):
    return await _send_request(addr, MESSAGE_TYPES["GET_STATE"])


async def start_server():
    server = await asyncio.start_server(_handle_connection, HOST_IP, PORT)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    try:
        await server.serve_forever()
    except asyncio.CancelledError:
        server.close()
        await server.wait_closed()
        # raise


async def main():
    server_task = asyncio.create_task(start_server())

    await asyncio.sleep(5)
    if len(clients) > 0:
        print("Sending Update to client...")
        await send_update(list(clients.keys())[0])

    await server_task


# Entry point
if __name__ == "__main__":

    asyncio.run(main())
