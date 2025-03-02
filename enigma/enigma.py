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
    def __init__(self, position_letter: str = "A"):
        self.position_letter = position_letter
        self.position = string.ascii_uppercase.index(position_letter)


class Rotor:
    def __init__(self, name, location=0, ring_setting=1, initial_position="A"):
        self.mapping = mappings[name]
        self.name = name
        self.location = location
        self.ring_setting = ring_setting
        self.notch = Notch(notch_map[name]) if name in notch_map else None
        self.position: int = string.ascii_uppercase.index(initial_position)
        self.initial_position = string.ascii_uppercase.index(initial_position)

        self.next_rotor = None
        self.prev_rotor = None

    def connect(self, next_rotor=None, prev_rotor=None):
        self.next_rotor = next_rotor
        self.prev_rotor = prev_rotor

    def encode_right_to_left(self, character):
        # 1. Convert character to number (0-25)
        pin_pos = string.ascii_uppercase.index(character)

        # 2. Apply position offset
        pin_pos = (pin_pos + self.position) % ALPHABET_SIZE

        # 3. Apply ring setting offset
        pin_pos = (pin_pos - (self.ring_setting - 1)) % ALPHABET_SIZE

        # 4. Use the mapping to encode
        contact_char = self.mapping[pin_pos]

        # 5. Reverse ring setting offset
        contact_pos = string.ascii_uppercase.index(contact_char)
        contact_pos = (contact_pos + (self.ring_setting - 1)) % ALPHABET_SIZE

        # 6. Reverse position offset
        contact_pos = (contact_pos - self.position) % ALPHABET_SIZE

        return string.ascii_uppercase[contact_pos]

    def encode_left_to_right(self, character):
        # 1. Convert character to number (0-25)
        contact_pos = string.ascii_uppercase.index(character)

        # 2. Apply position offset
        contact_pos = (contact_pos + self.position) % ALPHABET_SIZE

        # 3. Apply ring setting offset
        contact_pos = (contact_pos - (self.ring_setting - 1)) % ALPHABET_SIZE

        # 4. Find the position in the mapping
        char_in_alphabet = string.ascii_uppercase[contact_pos]
        pin_pos = self.mapping.index(char_in_alphabet)

        # 5. Reverse ring setting offset
        pin_pos = (pin_pos + (self.ring_setting - 1)) % ALPHABET_SIZE

        # 6. Reverse position offset
        pin_pos = (pin_pos - self.position) % ALPHABET_SIZE

        return string.ascii_uppercase[pin_pos]


    def rotate(self):
        # Don't rotate if this is a reflector (reflectors don't have notches)
        if not self.has_notch or self.name in ['Beta', 'Gamma']:
            return

        # Store position before rotation for notch checking
        self.initial_position = self.position
        if self.has_notch and self.is_at_notch and self.next_rotor:
            self.next_rotor.rotate()
        # Perform rotation
        self.position = (self.position + 1) % ALPHABET_SIZE

    def should_trigger_next_rotor(self):
        # Check if this rotor was at its notch position before rotating
        # Only rotors I-V have notches
        return self.has_notch and self.is_at_notch

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


def rotor_from_name(name, location: int = 0, ring_setting: int = 1, initial_position: string = "A"):
    return Rotor(name, location, ring_setting, initial_position)


class Enigma:
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
        self.init_rotors(rotor_sequence, ring_setting)
        self.connect_rotors()
        print(f"Rotors set to {[[rotor.position, rotor.name] for rotor in self.rotors]}.")
        self.plugboard = Plugboard(plug_combinations)

    @property
    def input_ring(self) -> Rotor:
        return self.rotors[0]

    def reset(self):
        for rotor in self.rotors:
            rotor.position = rotor.initial_position

    def init_rotors(self, rotor_sequence, ring_setting):
        for index, rotor_name in enumerate(reversed(rotor_sequence)):
            self.rotors.append(rotor_from_name(rotor_name, index, ring_setting[index], self.positions[index]))
        self.rotors.append(rotor_from_name(self.reflector))  # reflector goes at the end

    @property
    def rotor_positions(self) -> tuple[Any, ...]:
        return tuple(rotor.position for rotor in self.rotors)

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
        """Encode a character using Enigma machine.
        """
        character = character.upper()
        Enigma.__validate_character(character)

        # Initial plugboard encoding
        character = self.plugboard.encode(character)

        # Rotate before encoding
        self.__rotate()
        print(f"Rotated to {[[rotor.position, rotor.name] for rotor in self.rotors]}.")

        # Forward pass through rotors
        for rotor in self.rotors:
            character = rotor.encode_right_to_left(character)
            print(f"Rotor {rotor.name} Encryption: {character}")

        # Backward pass through rotors (excluding reflector)
        for rotor in reversed(self.rotors[:-1]):
            character = rotor.encode_left_to_right(character)
            print(f"Rotor {rotor.name} Encryption: {character}")

        # Final plugboard encoding
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
        """Rotate the rotors according to the Enigma machine rules.
            Uses the doubly-linked list structure where input_ring is the rightmost (fastest) rotor."""
        # Check middle rotor (input_ring.prev_rotor) for double-stepping
        middle_rotor = self.input_ring.prev_rotor
        if middle_rotor and middle_rotor.has_notch and middle_rotor.is_at_notch:
            # Double-stepping: middle rotor will step again when rightmost rotor steps
            middle_rotor.rotate()

        # Always rotate the input ring (rightmost/fastest rotor)
        # This will trigger cascading rotation through notches
        self.input_ring.rotate()


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    enigma2 = Enigma(rotor_sequence=["I", "II", "III"], reflector="B", ring_setting=[1, 1, 1], initial_positions="AAZ",
                     plug_combinations=["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])
    print(enigma2.encode("HELLOWORLD"))
    enigma2 = Enigma(rotor_sequence=["I", "II", "III"], reflector="B", ring_setting=[1, 1, 1], initial_positions="AAA")

    assert enigma2.encode_character("A") == "B"  # Expected output: B

#
# Keyboard Input: A
# Rotors Position: AAB
# Plugboard Encryption: A
# Wheel 3 Encryption: C
# Wheel 2 Encryption: D
# Wheel 1 Encryption: F
# Reflector Encryption: S
# Wheel 1 Encryption: S
# Wheel 2 Encryption: E
# Wheel 3 Encryption: B
# Plugboard Encryption: B
# Output (Lampboard): B
# -----------------------------
#
# Rotor III Encryption: B
# Rotor II Encryption: A
# Rotor I Encryption: C
# Rotor B Encryption: U
# Rotor I Encryption: R
# Rotor II Encryption: G
# Rotor III Encryption: S


# Keyboard Input: A
# Rotors Position: AAA
# Plugboard Encryption: A
# Wheel 3 Encryption: B
# Wheel 2 Encryption: J
# Wheel 1 Encryption: Z
# Reflector Encryption: T
# Wheel 1 Encryption: L
# Wheel 2 Encryption: K
# Wheel 3 Encryption: U
# Plugboard Encryption: U
# Output (Lampboard): U

#
# Keyboard Input: F
# Rotors Position: AAA
# Plugboard Encryption: F
# Wheel 3 Encryption: L
# Wheel 2 Encryption: H
# Wheel 1 Encryption: Q
# Reflector Encryption: E
# Wheel 1 Encryption: A
# Wheel 2 Encryption: A
# Wheel 3 Encryption: T
# Plugboard Encryption: T
# Output (Lampboard): T
# -----------------------------

# Keyboard Input: F
# Rotors Position: AAB
# Plugboard Encryption: F
# Wheel 3 Encryption: B
# Wheel 2 Encryption: J
# Wheel 1 Encryption: Z
# Reflector Encryption: T
# Wheel 1 Encryption: L
# Wheel 2 Encryption: K
# Wheel 3 Encryption: E
# Plugboard Encryption: E
# Output (Lampboard): E
