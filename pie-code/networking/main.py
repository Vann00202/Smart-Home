#!/usr/bin/env python3

import sys
import socket

# TODO: Find a way to gracefully exit and free up port


HOST_IP = "192.168.12.1"
PORT = 18000
MESSAGE_TYPES = ["GET_STATE", "SET_ON", "SET_OFF"]

running = True

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST_IP, PORT))
        s.listen()
        conn, addr = s.accept()  # This should be threaded in a while loop for multiple connections
        while running:
            print(f"Recieved connection from {addr}")
            msg = str(conn.recv(1024), "utf-8")
            if msg in MESSAGE_TYPES:
                print(f"Message Type: {msg}")
                conn.sendall(msg.encode())

    sys.exit(0)
