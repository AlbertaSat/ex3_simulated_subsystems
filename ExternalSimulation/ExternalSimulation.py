from threading import Lock, Thread

# Abstract external simulation class
class ExternalSimulationProvider:
    """
    Abstract class for interfacing with an external simulation.
    
    Basically implements a basic subject-observer pattern for subsystems to subscribe to, and a thread for receiving updates from the simulation.

    A state mutex is used to ensure updates to the state dictionary are atomic.
    Any reads to the state dictionary should only need to check if the mutex is locked, wait for it to be unlocked, and then read the state dictionary.

    Attributes:
    data: Dictionary containing the state of the simulation
    state_mutex: Mutex for 'controlling' access to the state dictionary
    observers: List of observers of the simulation state
    thread: Thread for running the simulation client

    Methods:
    attach: Attach a observer to the provider
    notify: Notify all observers of a state change
    start: Start the simulation client thread
    update: Update the simulation state

    """
    def __init__(self):
        # Initialize mutex, state dictionary, and observers
        self.data = {}
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
        # To be implemented by subclasses
        pass

class ExternalSimulationObserver:
    """Abstract class for observing an external simulation provider
    """
    def __init__(self, provider):
        self.provider = provider
        self.provider.attach(self)

    def update(self):
        # To be implemented by subclasses
        pass