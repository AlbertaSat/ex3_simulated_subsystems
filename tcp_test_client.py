import socket
import signal
import sys

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())
        print("Message sent to server")

def signal_handler(signum, frame):
    print(f"Received signal {signum}. Exiting gracefully.")
    sys.exit(0)

if __name__ == "__main__":
    # Communication parameters for the EPS subsystem
    eps_host = "127.0.0.1"
    eps_port = 1801

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create the socket outside the loop
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((eps_host, eps_port))

        while True:
            # Get user input
            user_input = input("Enter a message to send to the EPS subsystem (or press Enter to exit): ")

            # Exit the loop if the user presses Enter
            if not user_input:
                break

            # Send message to the EPS subsystem using the same socket
            client_socket.sendall(user_input.encode())
            print("Message sent to server")
