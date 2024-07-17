import socket
import sys
import threading
import time

def write_to_server(client, lock):
    while True:
        message = bytes(input(), "utf-8")
        try:
            with lock:
                client.sendall(message)
                print(f"Sent {message}")
        except Exception as e:
            print(f"Error sending data: {e}")
            client.close()
            break

BUFF_SIZE = 128

def main():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments:")
        print("Usage: python3 generic_client.py <port>")
        return 1

    host = socket.gethostname()
    port = int(sys.argv[1])

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"Connected to {host}:{port}")
    except OSError as e:
        print(f"Could not connect to hostname: {host} port: {port} - {e}")
        return -1

    client_lock = threading.Lock()
    write_thread = threading.Thread(target=write_to_server, args=(client, client_lock))
    write_thread.start()

    while True:
        try:
                msg = client.recv(BUFF_SIZE)
                if len(msg) > 0:
                    print(f"Received: {msg.decode('utf-8')}")
        except BlockingIOError:
            continue
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

if __name__ == "__main__":
    main()
