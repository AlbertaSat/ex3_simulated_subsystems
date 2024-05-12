#!/usr/bin/env python3
import socket
import click
import threading
import sys
import time


@click.command()  # Making this file a command line tool.
@click.option(
    "--host", default="127.0.0.1", help="The address of the host. Defaults to 127.0.0.1"
)
@click.option(
    "--port", default=42123, help="The port that the server will be hosted on"
)
def echo_server(host, port):
    """The main function that starts the echoing server"""
    s = socket.create_server((host, port))
    animate_loading()
    print(f"Started echo server at {host}, with port {port}")

    while True:
        conn, address = s.accept()
        print(f"Connected to {address}")
        new_thread = threading.Thread(target=handle_client, args=(conn, address))
        new_thread.start()


def animate_loading():
    chars = [".", "..", "..."]
    for char in chars:
        sys.stdout.write("\r" + "loading" + char)
        time.sleep(0.5)
        sys.stdout.flush()
    print("")


def handle_client(conn, addr: str):
    """This function makes the echo server handle a client"""
    while True:
        recv_data = conn.recv(4096)
        if recv_data:
            print(f"{recv_data}")
            if conn.sendall(recv_data) == None:
                continue
        else:
            print(f"Lost connection to {addr}, closing socket.")
            conn.close()
            break


if __name__ == "__main__":
    """Just trying to run a tcp server on localhost that will echo back all messages that it receives"""
    echo_server()
