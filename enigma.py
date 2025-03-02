import string
import logging

mappings = {
    "Beta": "LEYJVCNIXWPBQMDRTAKZGFUHOS",
    "Gamma": "FSOKANUERHMBTIYCWLQPZXVGJD",
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V": "VZBRGITYUPSDNHLXAWMJQOFECK"
}

reflectors = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}


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
        self.position = position


class Rotor:
    def __init__(self, mapping, location=0, ring_setting=0, notch=Notch(0)):
        self.mapping = mapping
        self.location = location
        self.ring_setting = ring_setting
        self.notch = notch

        self.next_rotor = None
        self.prev_rotor = None

    def connect(self, next_rotor=None, prev_rotor=None):
        self.next_rotor = next_rotor
        self.prev_rotor = prev_rotor

    def encode_right_to_left(self, character):
        # Signal enters pin side (right) and exits contact side (left)
        # 1. Find which pin the signal enters on
        pin_pos = string.ascii_uppercase.index(character)

        # 2. Follow internal wiring to contact
        contact_char = self.mapping[pin_pos]

        # 3. Pass to next rotor if exists
        if self.next_rotor:
            return self.next_rotor.encode_right_to_left(contact_char)
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
        self.notch.position = (self.notch.position + 1) % len(self.mapping)
        if self.is_at_notch() and self.next_rotor:
            self.next_rotor.rotate()

    def is_at_notch(self):
        return self.notch.position == len(self.mapping) - 1

    def encode(self, character):
        if self.notch.position == self.mapping.index(character):
            return self.encode_right_to_left(character)
        else:
            return self.encode_left_to_right(character)


def rotor_from_name(name, location=0, ring_setting=0, notch=Notch(0)):
    return Rotor(mappings[name], location, ring_setting, notch)


class Enigma:
    def __init__(self, rotor_sequence, ring_setting, reflector):
        self.rotors = []
        self.init_rotors(rotor_sequence, ring_setting)
        self.connect_rotors()

        self.reflector = reflector
        self.plugboard = Plugboard()

    def init_rotors(self, rotor_sequence, ring_setting):
        for rotor, index in enumerate(rotor_sequence):
            self.rotors.append(rotor_from_name(rotor, index, ring_setting[index]))
        logging.info(f"Rotors set to {rotor_sequence}.")

    def connect_rotors(self):
        """Connect rotors in a doubly linked list structure"""
        for i in range(len(self.rotors)):
            next_rotor = self.rotors[i + 1] if i < len(self.rotors) - 1 else None
            prev_rotor = self.rotors[i - 1] if i > 0 else None
            self.rotors[i].connect(next_rotor, prev_rotor)

if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    pass
