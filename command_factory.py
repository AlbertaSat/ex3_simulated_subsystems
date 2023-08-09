"""This module contains a factory class to create command objects based on command type.

Copyright 2023 [Abhishek Naik]. Licensed under the Apache License, Version 2.0
"""


# Factory pattern: Command Factory
class CommandFactory:
    """A factory class to create command objects based on command type."""

    def __init__(self, subsystem):
        self.subsystem = subsystem

    def command_request_data(self, params=None):
        """
        Executes a 'request' type command to get the current value of a parameter.
        Args:
            params (list): Name of the parameter to request from the IRIS subsystem state
        Returns:
            str: A string containing the requested parameter and its associated value
        """
        print("Request command received: " + params[0])
        if params and len(params) == 1 and params[0] in self.subsystem.state:
            return f"{params[0]}:{self.subsystem.state[params[0]]}\n"
        return "ERROR: Invalid request command \n"

    def command_update_parameter(self, params=None):
        """
        Executes an 'update' type command to update a parameter value.
        Args:
            params (list): Name of the parameter to request from the IRIS subsystem state
        Returns:
            str: A string containing the requested parameter and its associated value
        """
        print("Update command received: " + params[0])
        if params and len(params) == 2 and params[0] in self.subsystem.updatable_parameters:
            self.subsystem.state[params[0]] = params[1]
            return f"Updated {params[0]} to {params[1]}\n"
        return "ERROR: update command \n"

    def command_execute(self, params=None):
        """
        Executes an 'execute' type command to call a function.
        Args:
            params (list): Name of the function to call
        Returns:
            str: A string containing the return value from the function call
        """
        print("Execute command received: " + params[0])
        if params and len(params) == 1 and params[0] in self.subsystem.executable_commands:
            return f"Command {params[0]} executed \n"
        return "ERROR: Invalid execute command \n"

    def create_command(self, command_type):
        """Creates a command object based on the command type.
        Args:
            command_type (str): The type of command to be created
        Returns:
            the method that was asked for in 'command_type'
        """
        if command_type == 'request':
            return self.command_request_data
        if command_type == 'update':
            return self.command_update_parameter
        if command_type == 'execute':
            return self.command_execute
        return None
