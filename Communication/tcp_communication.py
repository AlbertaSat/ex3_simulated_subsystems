from Communication.communication_interface import CommunicationInterface
import socket
import threading
import queue
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TCPCommunication(CommunicationInterface):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind((self.host, self.port))
        self.socket_obj.listen()
        self.connected_client = None
        self.lock = threading.Lock()
        self.incoming_messages = queue.Queue()
        self.outgoing_messages = queue.Queue()

    def start_listening(self):
        threading.Thread(target=self._listen_for_clients, daemon=True).start()
        threading.Thread(target=self._send_messages, daemon=True).start()
        threading.Thread(target=self._receive_messages, daemon=True).start()

    def _listen_for_clients(self):
        while True:
            try:
                conn, addr = self.socket_obj.accept()
                with self.lock:
                    if self.connected_client:
                        logger.info("Disconnecting previous client.")
                        # Clear message queues when client is disconnected
                        self.incoming_messages.queue.clear()
                        self.outgoing_messages.queue.clear()
                        self.connected_client.close()

                    self.connected_client = conn
                    logger.info(f"Connected with {addr}")
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt detected. Closing socket.")
                with self.lock:
                    if self.connected_client:
                        self.connected_client.close()
                break
            except BrokenPipeError as error_msg:
                logger.info(f"Client connection closed: {error_msg}")
                with self.lock:
                    if self.connected_client:
                        # Clear message queues when client is disconnected
                        self.incoming_messages.queue.clear()
                        self.outgoing_messages.queue.clear()
                        self.connected_client.close()
                    self.connected_client = None

    def _send_messages(self):
        while True:
            try:
                with self.lock:
                    if self.connected_client:
                        if not self.outgoing_messages.empty():
                            message = self.outgoing_messages.get()
                            self.connected_client.sendall(message.encode())
                            logger.info(f"Sent message to client: {message}")

            except BrokenPipeError:
                logger.info("Client disconnected abruptly")
                with self.lock:
                    self.connected_client.close()
                    self.connected_client = None

    def _receive_messages(self):
        while True:
            try:
                with self.lock:
                    if self.connected_client:
                        data = self.connected_client.recv(
                            1024).decode().strip()
                        if data:
                            self.incoming_messages.put(data)
                            logger.info(
                                f"Received message from client: {data}")

            except BrokenPipeError:
                logger.info("Client disconnected abruptly")
                with self.lock:
                    self.connected_client.close()
                    self.connected_client = None

    def send_message(self, message):
        with self.lock:
            self.outgoing_messages.put(message)

    def receive_message(self):
        try:
            return self.incoming_messages.get(block=False)
        except queue.Empty:
            return None
