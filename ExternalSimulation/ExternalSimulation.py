from threading import Lock, Thread

# Abstract external simulation class
class ExternalSimulationProvider:
    """
    Abstract class for interfacing with an external simulation.
    
    Basically implements a basic subject-observer pattern for subsystems to subscribe to, and a thread for receiving updates from the simulation.

    A state mutex is used to ensure updates to the state dictionary are atomic.
    Any reads to the state dictionary should only need to check if the mutex is locked, wait for it to be unlocked, and then read the state dictionary.

    Attributes:
    name: Name of the simulation provider
    available_data: List of data types provided by the simulation
    data: Dictionary containing the state of the simulation
    state_mutex: Mutex for ensuring atomic updates to the state dictionary
    observers: List of observers of the simulation state
    thread: Thread for running the simulation client

    Methods:
    attach: Attach a observer to the provider
    notify: Notify all observers of a state change
    start: Start the simulation client thread
    update: Update the simulation state
    check_support: Check if the simulation provider supports a specific data type

    """
    def __init__(self, name, state_dictionary):
        # Initialize mutex, state dictionary, and observers
        self.name = name
        self.available_data = state_dictionary.keys()
        self.state = state_dictionary
        self.raw_data = {}
        self.state_mutex = Lock()
        self.observers = []

        # Create a thread for the external simulation client
        self.thread = Thread(target=self.update)
        pass

    def attach(self, observer):
        """Attach an observer to the provider
        """
        self.observers.append(observer)

    def notify(self):
        """Notify all observers of a state change
        """
        for observer in self.observers:
            observer.update()

    def start(self):
        """Start the simulation client update thread
        """
        self.thread.start()

    def update(self):
        # Should be implemented by any derived classes
        raise NotImplementedError
    
    def check_support(self, data_type):
        """Check if the simulation provider supports a specific data type
        """
        return data_type in self.available_data

    def get_data(self, data_type):
        """Get the current state data from the simulation
        """
        # Check if the mutex is locked
        while self.state_mutex.locked():
            pass
        
        return self.state[data_type]

class ExternalSimulationObserver:
    """Abstract class for observing an external simulation provider
    """
    def __init__(self, provider):
        self.provider = provider
        self.provider.attach(self)

    def update(self):
        # Should be implemented by any derived classes
        raise NotImplementedError