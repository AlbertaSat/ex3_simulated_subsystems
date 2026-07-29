# Definitions Module

## Overview

This module contains immutable definitions that are shared
throughout the project. Things such as the root path of the
project directory on any file system, and `enum` that
represents the different simulated subsystems.

## Content

### PROJECT_ROOT

This is a `pathlib.Path` object that contains the path to
the root of the project. This value is dynamic, as it 
will update between machines.

### Subsystems

This `enum` contains the fixed grouping of subsystems
supported by this project.
