import socket
from threading import Lock
import time
from os import path
import subprocess
import sys

path_to_script = path.dirname(path.abspath(__file__))
path_to_42 = path.join(path_to_script, "..", "..", "42", "42")

state_dictionary = {
    'dfgm': {
        "Bx": 0,
        "By": 0,
        "Bz": 0,
    },
    'daedalus': {
        "temperature": 0,
    }
}


# Interface class for the 42 simulation
class FTInterface:
    def __init__(self, exec_path=path_to_42):
        print(f"Starting 42 simulation at {exec_path}")
        # Launch the 42 simulation
        sys.path.append(exec_path)
        
        # Start the 42 simulation
        self.simulator = subprocess.Popen([exec_path], cwd=exec_path[:-3], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        # Initialize mutex and state dictionary for the FT
        self.data = {}
        self.state_mutex = Lock()
        
        # # Connect to localhost:10001 TCP/IP socket
        print("Connecting to server")
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect(('localhost', 10001))
                break
            except ConnectionRefusedError:
                print("42 Connection refused. Retrying in 1 second")
                time.sleep(1)
        
        # # Create a thread to listen for data from the server
        # self.client_thread = Thread(target=self.thread_function)

    def update_state_atomic(self):
        """ Function to read the state of the 42 simulation
        """
        with self.state_mutex:
            # Socket state data from the simulation starts with `TIME: XXXXXXXXXXX` and ends with `[EOF]`
            
            # Read full message from the simulation
            data = self.s.recv(1024*128).decode("utf-8")
            
            print(f"Received: {data}")
            
            # Structure
            # TIME 0.0000000000000000
            # DictionaryList[0].Name = x[ y[ z]]
            # DictionaryList[1].Name = x[ y[ z]]
            # ...
            # [EOF]
            
            # Split the data into lines
            lines = data.split("\n")
            self.data = {}
            
            # Parse the data into a dictionary
            for line in lines:
                if line == "[EOF]":
                    break
                if "TIME" in line:
                    # Parse the time
                    self.data["TIME"] = line.split(" ")[1]
                else:
                    # Parse the line into a dictionary
                    line_data = line.split(" = ")
                    name = line_data[0].split("[")[0]
                    field = line_data[0].split("]")[1][1:]
                    i = int(line_data[0].split("[")[1].split("]")[0])
                    values = line_data[1].split(" ")
                    
                    # CHeck if the name is in the dictionary
                    if name not in self.data:
                        self.data[name] = [{}]
                    
                    # Check if the index is in the dictionary
                    if len(self.data[name]) <= i:
                        self.data[name].append({})
                    
                    # Add the field to the dictionaru
                    if field not in self.data[name][i]:
                        self.data[name][i][field] = []
                    
                    self.data[name][i][field] = values
  
    def thread_function(self):
        """ Function to listen for data from the server and process it
        """
        while True:
            data = self.s.recv(1024)
            print(f"Received: {data}")

    # def __del__(self):
    #     if self.s is not None:
    #         self.s.close()
    #     if self.simulator is not None:
    #         self.simulator.terminate()

        
        
if __name__ == "__main__":
    ft_interface = FTInterface()
    ft_interface.update_state_atomic()
    while True:
        pass
    # ft_interface.client_thread.start()