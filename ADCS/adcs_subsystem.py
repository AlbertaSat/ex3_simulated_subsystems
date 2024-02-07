
import sys
sys.path.append("../")

class ADCSSubsystem:
    """
    This class represents the simulated ADCS subsystem.
    """
    def __init__(self, builder_dict):
        """
        Base constructor. Uses a dictionary with the default values.
        """
        self.state = builder_dict   # This is placeholder.


def command_line_handler(argv):
    """
    Control flow for what to return depending on the commandline arg.

    **Change here if you need to change the port and address values**

    Returns:
        (PORT, HOST)
    """
    default_host = "127.0.0.1"
    default_port = 1802

    return (argv[1] if len(argv) > 1 else default_port), default_host


if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)

    print(f"Starting ADCS subsystem on port {port}")
