import socket
import pickle

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8352

def serialize_file(filename):
        with open(filename, 'rb') as file:
            file_contents = file.read()
            serialized_data = pickle.dumps(file_contents)
            return serialized_data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((DEFAULT_HOST, DEFAULT_PORT))
    message = serialize_file('packet.txt')
    s.sendall(message)