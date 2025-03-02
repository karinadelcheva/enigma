# Enigma Machine Implementation

This project implements a simulation of the World War II Enigma encryption machine in Python. The implementation includes all core components of the historical Enigma machine.

## Components

The implementation consists of several key classes:

### PlugLead
- Represents a single plug connection in the Enigma machine's plugboard
- Handles the swapping of character pairs

### Plugboard
- Manages multiple plug connections
- Allows adding new plug leads
- Encodes characters according to the plug connections

### Rotor
- Implements the Enigma machine's rotor mechanism
- Supports bidirectional encoding (right-to-left and left-to-right)
- Handles rotor rotation and notch positions
- Configurable ring settings

### Notch
- Represents the notch position on a rotor
- Used for controlling rotor stepping

### Enigma
- Main class that combines all components
- Manages the rotor setup and connections
- Handles the complete encryption/decryption process

## Usage

The implementation can be imported into Python code using:

```python
from enigma import *
```

The code is designed to be used as a module, with the main functionality implemented in separate Python files rather than directly in Jupyter notebook cells.

## Features

- Full implementation of historical Enigma machine mechanics
- Configurable rotor settings and positions
- Plugboard support for character substitution
- Bidirectional signal flow through rotors
- Reflector implementation
- Rotor stepping mechanism with notch positions

## Requirements

- Python 3.x
- No additional dependencies required

## Implementation Details

The code implements the mechanical workings of the Enigma machine, including:
- Character mapping through rotors
- Rotor rotation mechanisms
- Plugboard character substitution
- Reflector functionality
- Full signal path simulation (forward and return paths)# enigma
