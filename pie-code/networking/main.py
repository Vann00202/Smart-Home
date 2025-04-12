#!/usr/bin/env python3

import sys
import socket
import signal

# TODO: Find a way to gracefully exit and free up port

HOST_IP = "192.168.12.1"
PORT = 18000
MESSAGE_TYPES = ["GET_STATE", "SET_ON", "SET_OFF"]
MESSAGE_TERMINATION = "\n"

state = {
    "running": False
}


def interrupt_handler(sig, frame):
    print("Keyboard Interrupt Recieved")
    state["running"] = False


def run_server():
    state["running"] = True

    signal.signal(signal.SIGINT, interrupt_handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST_IP, PORT))
        s.listen()
        s.settimeout(1.0)
        while state["running"]:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue

            with conn:
                print(f"Recieved connection from {addr}")
                msg = str(conn.recv(1024), "utf-8")
                if msg in MESSAGE_TYPES:
                    print(f"Recieved Message Type: {msg}")
                    sendmsg = MESSAGE_TYPES[1] + MESSAGE_TERMINATION
                    conn.sendall(sendmsg.encode())

    print("Server shutdown gracefully")


if __name__ == "__main__":

    run_server()

    sys.exit(0)
