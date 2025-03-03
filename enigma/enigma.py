import string
from typing import Any

"""
Enigma Machine Implementation

I'm happy to present my implementation of the Enigma machine. 
Working on this project was truly enjoyable, and I appreciate the opportunity.
For this implementation, I chose an object-oriented programming approach to create 
more dynamic interactions between classes. A feature I am happy with developing was implementing a 
doubly linked list property for the Rotors to enhance the rotation mechanism.
Given more time, I would have further leveraged the doubly linked list structure 
to improve both encoding and decoding processes. I believe this would have 
significantly enhanced the machine's functionality and elegance. 
I also wanted to decode the sample codes provided but couldn't complete that within the timeframe.
One aspect I particularly wanted to develop was better visualization of the machine's operation.

Future enhancements I would implement include:
- Randomly generated rotor mappings
- Support for an unlimited number of rotors
- Generation of machines based on historical models and manufacturing years

Please note, I have intentionally left all the classes and constants in a single file, as I've never submitted 
code before in this way and thought it might be most safe.

"""

mappings = {
    "Beta": "LEYJVCNIXWPBQMDRTAKZGFUHOS",
    "Gamma": "FSOKANUERHMBTIYCWLQPZXVGJD",
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V": "VZBRGITYUPSDNHLXAWMJQOFECK",
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

reflectors = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

notch_map = {
    "I": "Q",
    "II": "E",
    "III": "V",
    "IV": "J",
    "V": "Z"
}

ALPHABET_SIZE = 26


class PlugLead:
    """
    Representation of a PlugLead in an Enigma machine simulation.

    The PlugLead is used to represent a connection between two letters and exists within a
    plugboard.

    :ivar map_dict: A dictionary representing the mapping of two connected
        characters.
    :type map_dict: dict
    """

    def __init__(self, mapping):
        if len(mapping.split()) > 2:
            raise ValueError("Plug mapping should only contain 2 characters")
        self.map_dict = {x: y for x, y in zip(mapping, reversed(mapping))}

    def encode(self, character):
        return self.map_dict.get(character, character)


class Plugboard:
    """
    Represents a plugboard component in an Enigma machine.

    It allows the dynamic addition of plug leads and provides character encoding
    functionality by routing each character through all plug leads.

    :ivar plugs: List of plug leads added to the plugboard.
    :type plugs: list[PlugLead]
    """
    def __init__(self, plug_combinations=None):
        self.plugs = []
        if plug_combinations:
            for plug_combination in plug_combinations:
                self.add(PlugLead(plug_combination))

    def add(self, plug):
        self.plugs.append(plug)

    def encode(self, character):
        for plug in self.plugs:
            character = plug.encode(character)
        return character


class Notch:
    """
    Represents a specific notch indicating a turning position
    within a rotor and is associated with a letter.

    :ivar position_letter: The letter representing the position in the alphabet.
    :type position_letter: str
    :ivar position: The numeric index (0-based) of the position_letter in the alphabet.
    :type position: int
    """
    def __init__(self, position_letter: str = "A"):
        self.position_letter = position_letter
        self.position = string.ascii_uppercase.index(position_letter)


class Rotor:
    """
    Represents a rotor in an Enigma machine.

    The rotor's primary purpose is to encode and decode characters as part of the
    Enigma encryption process. It transforms characters through a specific mapping,
    rotates to change its transformation rules, and interacts with neighboring rotors
    to manipulate the encryption further. Some rotors contain notches that trigger
    the rotation of the next rotor when crossing specific positions.

    Reflectors within the Enigma machine are also of class Rotor.
    """
    def __init__(self, name, location=0, ring_setting=1, initial_position="A"):
        self.name = name
        self.location = location
        self.ring_setting = ring_setting
        self.notch = Notch(notch_map[name]) if name in notch_map else None
        self.position: int = string.ascii_uppercase.index(initial_position)
        self.initial_position = string.ascii_uppercase.index(initial_position)

        self.next_rotor = None
        self.prev_rotor = None

    @property
    def mapping(self):
        return  mappings[self.name]

    @property
    def has_notch(self):
        return self.notch is not None

    @property
    def is_at_notch(self):
        return self.notch.position == self.position

    @property
    def get_relative_position(self):
        return self.position % ALPHABET_SIZE

    @property
    def should_trigger_next_rotor(self):
        # Check if this rotor was at its notch position before rotating
        # Only rotors I-V have notches
        return  self.name not in ['Beta', 'Gamma'] and self.has_notch and self.is_at_notch

    def connect(self, next_rotor=None, prev_rotor=None):
        self.next_rotor = next_rotor
        self.prev_rotor = prev_rotor

    def encode_right_to_left(self, character):
        pin_pos = string.ascii_uppercase.index(character)

        pin_pos = (pin_pos + self.position - (self.ring_setting - 1)) % ALPHABET_SIZE
        contact_char = self.mapping[pin_pos]

        contact_pos = string.ascii_uppercase.index(contact_char)
        contact_pos = (contact_pos + (self.ring_setting - 1)) % ALPHABET_SIZE

        contact_pos = (contact_pos - self.position) % ALPHABET_SIZE
        return string.ascii_uppercase[contact_pos]

    def encode_left_to_right(self, character):
        contact_pos = string.ascii_uppercase.index(character)
        contact_pos = (contact_pos + self.position - (self.ring_setting - 1)) % ALPHABET_SIZE

        char_in_alphabet = string.ascii_uppercase[contact_pos]
        pin_pos = self.mapping.index(char_in_alphabet)

        pin_pos = (pin_pos + (self.ring_setting - 1)) % ALPHABET_SIZE
        pin_pos = (pin_pos - self.position) % ALPHABET_SIZE

        return string.ascii_uppercase[pin_pos]

    def rotate(self):
        """
        Rotates current within the machine depending on its position, type and notch.
        Don't rotate if this is a reflector (reflectors don't have notches)
        """
        # TODO: implement this check using a property of the rotor
        if not self.has_notch and self.name not in ['Beta', 'Gamma']:
            return

        # Store position before rotation for notch checking
        self.initial_position = self.position
        if self.should_trigger_next_rotor and self.next_rotor:
            self.next_rotor.rotate()
        # Perform rotation
        self.position = (self.position + 1) % ALPHABET_SIZE


    def encode(self, character):
        if self.notch.position == self.mapping.index(character):
            return self.encode_right_to_left(character)
        else:
            return self.encode_left_to_right(character)


def rotor_from_name(name, location: int = 0, ring_setting: int = 1, initial_position: string = "A"):
    return Rotor(name, location, ring_setting, initial_position)


class Enigma:
    """
    The Enigma class simulates the functionality of the Enigma machine, a cipher device used in the early to mid-20th
    century. This class allows for encoding and decoding messages through a series of rotors, reflectors, and plugboard
    connections. The implementation handles various configurations, including rotor sequences, reflector types,
    ring settings, initial positions, and plugboard combinations. Encoding and decoding follow the exact same
    bidirectional logic, true to the behavior of the original Enigma machine.

    This class manages rotor initialization, connectivity, and transformations during encoding.
    It supports rotation mechanics, including double-stepping logic. The `encode_character` method handles
    a single character transformation, while `encode` and `decode` apply transformations over an entire message.

    :ivar rotors: List of Rotor objects representing the rotors in the Enigma machine.
    :type rotors: list
    :ivar positions: String representation of the current positions of the rotors.
    :type positions: str
    :ivar reflector: String identifier for the reflector used in the Enigma machine (e.g., "B", "C").
    :type reflector: str
    :ivar plugboard: Plugboard instance representing the plugboard connections.
    :type plugboard: Plugboard
    """
    def __init__(
            self,
            rotor_sequence: list,
            reflector: str,
            ring_setting: list = None,
            initial_positions: string = "AAA",
            plug_combinations: list = None,
    ):
        if ring_setting is None:
            ring_setting = [1, 1, 1]

        self.rotors = []
        self.positions = "".join(reversed(initial_positions))
        self.reflector = reflector
        self.init_rotors(rotor_sequence, list(reversed(ring_setting)))
        self.connect_rotors()

        self.plugboard = Plugboard(plug_combinations)

    @property
    def input_ring(self) -> Rotor:
        return self.rotors[0]

    @property
    def reflector_ring(self) -> Rotor:
        return self.rotors[-1]

    @property
    def rotor_positions(self) -> tuple[Any, ...]:
        return tuple(rotor.position for rotor in self.rotors)

    def reset(self):
        for rotor in self.rotors:
            rotor.position = rotor.initial_position

    def init_rotors(self, rotor_sequence, ring_setting):
        for index, rotor_name in enumerate(reversed(rotor_sequence)):
            self.rotors.append(rotor_from_name(rotor_name, index, ring_setting[index], self.positions[index]))
        self.rotors.append(rotor_from_name(self.reflector))  # reflector goes at the end


    def connect_rotors(self):
        for position, rotor in enumerate(self.rotors):
            if position == 0:
                prev_rotor = None
            else:
                prev_rotor = self.rotors[position - 1]
            if position == len(self.rotors) - 1:
                next_rotor = None
            else:
                next_rotor = self.rotors[position + 1]
            rotor.connect(next_rotor=next_rotor, prev_rotor=prev_rotor)  # Use named parameters to be explicit

    def encode_character(self, character: str):
        """
        Encodes a single character using the Enigma machine simulation. The encoding process includes
        passing the character through a plugboard, forward and backward rotor passes, and a final plugboard
        encoding. The Enigma machine rotors are also rotated before the encoding process.

        :param character: The character to be encoded. Must be a single uppercase letter.
        :returns: The encoded character after processing through the Enigma machine.
        :rtype: str
        """
        character = character.upper()
        self.validate_character(character)

        # Initial plugboard encoding
        character = self.plugboard.encode(character)

        # Rotate before encoding
        self.rotate()

        # Forward pass through rotors
        for rotor in self.rotors:
            character = rotor.encode_right_to_left(character)

        # Backward pass through rotors (excluding reflector)
        for rotor in reversed(self.rotors[:-1]):
            character = rotor.encode_left_to_right(character)


        # Final plugboard encoding
        return self.plugboard.encode(character)

    def decode_character(self, character: str):
        """
        Just points to encode_character. The two methods are equivalent.
        """
        return self.encode_character(character)

    def encode(self, message: str):
        """
        Encodes a given message by converting each character to its respective encoded value.

        :param message: The message string that needs to be encoded.
        :type message: str
        :return: A string representing the encoded message.
        :rtype: str
        """
        encoded_message = ""
        for c in message:
            encoded_message += str(self.encode_character(c.upper()))

        return encoded_message

    def decode(self, message, reset_rotors: bool = False):
        """
        Just points to Enigma.encode
        """
        return self.encode(message)

    def validate_character(self, character):
        if not character.isalpha() or not character.isupper():
            raise ValueError(f"Invalid character: {character}. Must be an uppercase English letter.")

    def rotate(self):
        """Rotate the rotors according to the Enigma machine rules.
            Uses the doubly-linked list structure where input_ring is the rightmost (fastest) rotor."""

        # Check middle rotor (input_ring.prev_rotor) for double-stepping
        if self.input_ring.name not in ['Beta', 'Gamma']:
            middle_rotor = self.input_ring.prev_rotor
            if middle_rotor and middle_rotor.has_notch and middle_rotor.is_at_notch:
                # Double-stepping: middle rotor will step again when rightmost rotor steps
                middle_rotor.rotate()

        # Always rotate the input ring (rightmost/ fastest rotor)
        # This will trigger cascading rotation through notches
        # Note: the Rotor.rotate() method contains a check if the rotor type is a rotating rotor (I-V)
        self.input_ring.rotate()


if __name__ == "__main__":
   pass