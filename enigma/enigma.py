import string
import logging
from typing import Any

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
    def __init__(self, mapping):
        if len(mapping.split()) > 2:
            raise ValueError("Plug mapping should only contain 2 characters")
        self.map_dict = {x: y for x, y in zip(mapping, reversed(mapping))}

    def encode(self, character):
        return self.map_dict.get(character, character)


class Plugboard:
    def __init__(self):
        self.plugs = []

    def add(self, plug):
        self.plugs.append(plug)

    def encode(self, character):
        for plug in self.plugs:
            character = plug.encode(character)
        return character


class Notch:
    def __init__(self, position):
        self.position = string.ascii_uppercase.index(position)


class Rotor:
    def __init__(self, name, location=0, ring_setting=0, initial_position="A"):
        self.mapping = mappings[name]
        self.name = name
        self.location = location
        self.ring_setting = ring_setting
        self.notch = Notch(notch_map[name]) if name in notch_map else None
        self.position: int = string.ascii_uppercase.index(initial_position)
        self.initial_position = initial_position
        print('initial position', self.position)
        print('ring_setting', self.ring_setting)
        # print('notch', self.notch.position)
        print('self.mapping', self.mapping)

        self.next_rotor = None
        self.prev_rotor = None

    def connect(self, next_rotor=None, prev_rotor=None):
        self.next_rotor = next_rotor
        self.prev_rotor = prev_rotor

    def encode_right_to_left(self, character):
        # Signal enters pin side (right) and exits contact side (left)
        # 1. Find which pin the signal enters on
        pin_pos = string.ascii_uppercase.index(character)
        print('inside rotor ', self.name, 'character ', character)
        print('character position ', pin_pos)

        # 2. Apply position offset
        pin_pos = (pin_pos + self.position) % 25
        print('after position offset', pin_pos)

        # 3. Apply ring setting offset (opposite direction of position)
        pin_pos = (pin_pos - self.ring_setting) % 25
        print('after ring setting offset ', pin_pos)
        # 2. Follow internal wiring to contact
        contact_char = self.mapping[pin_pos]
        print('contact_char', contact_char)
        # # 3. Pass to next rotor if exists
        # if self.next_rotor:
        #     return self.next_rotor.encode_right_to_left(contact_char)
        return contact_char

    def encode_left_to_right(self, character):
        # Signal enters contact side (left) and exits pin side (right)
        # 1. Find which contact the signal enters on
        contact_pos = self.mapping.index(character)

        # 2. Follow internal wiring backwards to pin
        pin_char = string.ascii_uppercase[contact_pos]

        # 3. Pass to previous rotor if exists
        if self.prev_rotor:
            return self.prev_rotor.encode_left_to_right(pin_char)
        return pin_char

    def rotate(self):
        self.position += 1

        if self.has_notch and self.is_at_notch and self.next_rotor:
            self.next_rotor.rotate()

    @property
    def has_notch(self):
        return self.notch is not None

    @property
    def is_at_notch(self):
        return self.notch.position == self.position

    @property
    def get_relative_position(self):
        return self.position % ALPHABET_SIZE

    def encode(self, character):
        if self.notch.position == self.mapping.index(character):
            return self.encode_right_to_left(character)
        else:
            return self.encode_left_to_right(character)



def rotor_from_name(name, location: int = 0, ring_setting: int = 0, initial_position: string = "A"):
    return Rotor(name, location, ring_setting, initial_position)


class Enigma:
    def __init__(
            self,
            rotor_sequence: list,
            reflector: str,
            ring_setting: list = None,
            initial_positions: string = "AAA"
    ):
        if ring_setting is None:
            ring_setting = [1, 1, 1]

        self.rotors = []
        self.positions = initial_positions
        self.reflector = reflector
        self.init_rotors(rotor_sequence, ring_setting)
        self.connect_rotors()

        self.plugboard = Plugboard()

    @property
    def input_ring(self) -> Rotor:
        return self.rotors[0]

    def reset(self):
        for rotor in self.rotors:
            rotor.position = string.ascii_uppercase.index(rotor.initial_position)

    def init_rotors(self, rotor_sequence, ring_setting):
        for index, rotor_name in enumerate(reversed(rotor_sequence)):
            print('initializing rotor: ', rotor_name, index, ring_setting[index], self.positions[index])
            self.rotors.append(rotor_from_name(rotor_name, index, ring_setting[index], self.positions[index]))
        self.rotors.append(rotor_from_name(self.reflector))  # reflector goes at the end

        logging.info(f"Rotors set to {rotor_sequence}. Reflector set to {self.reflector}.")

    @property
    def rotor_positions(self) -> tuple[Any, ...]:
        """
        Get the current positions of all three rotors.

        Returns:
            tuple[int, int, int]: Current positions of the left, middle, and right rotors
        """
        return tuple(rotor.position for rotor in self.rotors)

    def get_rotor_positions(self):
        return self.rotor_positions

    def connect_rotors(self):
        """Connect each rotor to its neighboring rotors in the sequence,
        implementing a doubly-linked list structure."""
        total_rotors = len(self.rotors)

        for position, rotor in enumerate(self.rotors):
            rotor.left_rotor = self.rotors[position + 1] if position < total_rotors - 1 else None
            rotor.right_rotor = self.rotors[position - 1] if position > 0 else None

    def encode_character(self, character: str):
        """Encode a character using our Enigma machine.
        """
        character = character.upper()
        Enigma.__validate_character(character)
        character = self.plugboard.encode(character)
        self.__rotate()

        # pass characters
        for rotor in self.rotors:
            character = rotor.encode_right_to_left(character)

        for rotor in reversed(self.rotors[0:-1]):
            character = rotor.encode_left_to_right(character)

        # calculate offset between last rotor on right and static ring
        inx = self.input_ring.mapping.index(character)
        first_rotor_offset = self.rotors[0].get_relative_position % ALPHABET_SIZE
        character = self.input_ring.mapping[(inx - first_rotor_offset) % ALPHABET_SIZE]

        # swap the character again if connected in the plugboard by lead.
        return self.plugboard.encode(character)

    def decode_character(self, character: str):
        """Just points to encode_character. The two methods are equivalent in a DLL structure.
        """
        return self.encode_character(character)

    def encode(self, message: str):
        encoded_message = ""
        for c in message:
            encoded_message += str(self.encode_character(c.upper()))

        return encoded_message

    def decode(self, message, reset_rotors: bool = False):
        """Just points to encode
        """
        return self.encode(message)

    @classmethod
    def __validate_character(cls, character):
        if not character.isalpha() or not character.isupper():
            raise ValueError(f"Invalid character: {character}. Must be an uppercase English letter.")

    def __rotate(self):
        self.input_ring.rotate()


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    pass
