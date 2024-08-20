# Simconfig Module

## Overview

This is a helper library that can read the `simulated_config.ini`
configuration files.

## Usage

### Obtaining root config

The following Python snippet is how the configuration
dictionary can be obtained from the configuration file
in the root.

```python
from simconfig import get_simulated_config
from definitions import TEST_PATH, Subsystems

config_dictionary = get_simulated_config(TEST_PATH, Subsystems.ADCS)

config_dictionary
# {"port": "61200"}
```
