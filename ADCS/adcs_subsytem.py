"""Empty Doc String to conform to Pylint"""
import sys
import socket

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1801


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting ADCS subsystem on port {PORT}")

    # Create a socket and bind it to the port. Listen indefinitely for client connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Tell OS to reuse socket addr if not previously closed
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((DEFAULT_HOST, int(PORT)))
        s.listen()

        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected with {addr}")
                    #handler = EPSCommandHandler(conn)
                    #handler.handle_command()

            except BrokenPipeError as e:
                print(f"Client connection closed: {e}")
