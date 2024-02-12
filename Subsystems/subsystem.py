"""
This parent class respresents all common attributes and methods for all subsystems.

- All subsystems must have an ON/OFF state. 

- All subsystems must be able to handle a message from the OBC, and send messages to the OBC, 
with the execption of the DFGM, which just repeatedly sends messages to the OBC. 

Copyright 2024 [Devin Headrick]. Licensed under the Apache License, Version 2.0
"""

from enum import Enum, auto

class SubsystemStatus(Enum):
    ON = auto()
    OFF = auto()

class Subsystem:
    def __init__(self, communication):
        self.status = SubsystemStatus.OFF
        self.communication = communication

    def turn_on(self):
        self.status = SubsystemStatus.ON

    def turn_off(self):
        self.status = SubsystemStatus.OFF

    def handle_message(self, message):
        # To be implemented by subclasses
        pass

    def dispatch_message(self, message):
        # To be implemented by subclasses
        pass


# pylint: disable=duplicate-code
# no error
__author__ = "Devin Headrick"
__copyright__ = """
    Copyright (C) 2023, [Devin Headrick]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
