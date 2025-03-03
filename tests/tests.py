import unittest
from enigma.enigma import Enigma, rotor_from_name, Plugboard, PlugLead

ENIGMA_TEST_CASES = [
    {
        'rotors': ['I', 'II', 'III'],
        'reflector': 'B',
        'ring_settings': [1, 1, 1],
        'initial_positions': ['A', 'A', 'Z'],
        'input_char': 'A',
        'expected_output': 'U'
    },
    {
        'rotors': ['I', 'II', 'III'],
        'reflector': 'B',
        'ring_settings': [1, 1, 1],
        'initial_positions': ['A', 'A', 'A'],
        'input_char': 'A',
        'expected_output': 'B'
    },
    {
        'rotors': ['I', 'II', 'III'],
        'reflector': 'B',
        'ring_settings': [1, 1, 1],
        'initial_positions': ['Q', 'E', 'V'],
        'input_char': 'A',
        'expected_output': 'L'
    },
    {
        'rotors': ['IV', 'V', 'Beta'],
        'reflector': 'B',
        'ring_settings': [14, 9, 24],
        'initial_positions': ['A', 'A', 'A'],
        'input_char': 'H',
        'expected_output': 'Y'
    },
    {
        'rotors': ['I', 'II', 'III', 'IV'],
        'reflector': 'C',
        'ring_settings': [7, 11, 15, 19],
        'initial_positions': ['Q', 'E', 'V', 'Z'],
        'input_char': 'Z',
        'expected_output': 'V'
    }
]


class TestEnigma(unittest.TestCase):
    def setUp(self):
        """
        Set up a fresh Enigma machine before each test
        """
        self.machine = Enigma()

    def test_single_rotor(self):
        rotor = rotor_from_name("I")

        assert (rotor.encode_right_to_left("A") == "E")
        assert (rotor.encode_left_to_right("A") == "U")

    def test_plugboard(self):
        plugboard = Plugboard()

        plugboard.add(PlugLead("SZ"))
        plugboard.add(PlugLead("GT"))
        plugboard.add(PlugLead("DV"))
        plugboard.add(PlugLead("KU"))

        assert (plugboard.encode("K") == "U")
        assert (plugboard.encode("A") == "A")

    def test_enigma_initialization(self):
        """Test that the Enigma machine initializes with correct default settings"""
        self.assertIsNotNone(self.machine.rotors)
        self.assertIsNotNone(self.machine.reflector)
        self.assertEqual(len(self.machine.rotors), 3)  # Standard Enigma had 3 rotors

    def test_enigma_encoding(self):
        """Test basic encoding functionality"""
        encoded = self.machine.encode('HELLO')
        self.assertIsInstance(encoded, str)
        self.assertNotEqual(encoded, 'HELLO')  # Encoded text should be different from input
        self.assertEqual(len(encoded), len('HELLO'))

    def test_enigma_decoding(self):
        """Test that encoding and then decoding returns original message"""
        original = 'TESTMESSAGE'
        encoded = self.machine.encode(original)
        # Reset machine to initial position
        self.machine.reset()
        decoded = self.machine.encode(encoded)  # In Enigma, encoding is same as decoding
        self.assertEqual(decoded, original)

    def test_invalid_input(self):
        """Test handling of invalid input"""
        with self.assertRaises(ValueError):
            self.machine.encode('123')  # Should raise error for non-alphabetic characters

    def test_rotor_rotation(self):
        """Test that rotors rotate correctly after each character"""
        initial_positions = self.machine.get_rotor_positions()
        self.machine.encode('A')
        new_positions = self.machine.get_rotor_positions()
        self.assertNotEqual(initial_positions, new_positions)  # At least one rotor should have moved

    def test_uppercase_input(self):
        """Test that the machine handles uppercase input correctly"""
        encoded = self.machine.encode('UPPER')
        self.assertTrue(encoded.isupper())
        self.assertEqual(len(encoded), 5)

    def test_machine_reset(self):
        """Test that machine reset returns to initial state"""
        # Encode something to change the state
        self.machine.encode_left_to_right('TEST')
        initial_positions = self.machine.get_rotor_positions()

        # Reset and check positions
        self.machine.reset()
        reset_positions = self.machine.get_rotor_positions()

        self.assertNotEqual(initial_positions, reset_positions)

    def test_long_message(self):
        """Test encoding of a longer message"""
        long_message = 'THISISALONGERMESSAGETOTEST'
        encoded = self.machine.encode_left_to_right(long_message)
        self.assertEqual(len(encoded), len(long_message))
        self.assertNotEqual(encoded, long_message)

    def test_repeated_character(self):
        """Test that same character encodes differently based on position"""
        # In Enigma, same letter should encode differently each time
        result = self.machine.encode_left_to_right('AAA')
        self.assertNotEqual(result[0], result[1])
        self.assertNotEqual(result[1], result[2])


def test_specific_enigma_configurations(self):
    """Test specific historical or known Enigma configurations"""
    for test_case in ENIGMA_TEST_CASES:
        with self.subTest(msg=f"Testing configuration: {test_case}"):
            # Create a new machine for each test case
            machine = Enigma(
                rotor_sequence=test_case['rotors'],
                reflector=test_case['reflector'],
                ring_setting=test_case['ring_settings'],
                initial_positions=test_case['initial_positions']
            )

            # Encode the input character
            result = machine.encode_left_to_right(test_case['input_char'])

            # Assert the result matches expected output
            self.assertEqual(
                result,
                test_case['expected_output'],
                f"Failed with configuration:\n"
                f"Rotors: {test_case['rotors']}\n"
                f"Reflector: {test_case['reflector']}\n"
                f"Ring settings: {test_case['ring_settings']}\n"
                f"Initial positions: {test_case['initial_positions']}\n"
                f"Input: {test_case['input_char']}\n"
                f"Expected: {test_case['expected_output']}\n"
                f"Got: {result}"
            )

def test_rotor_rotation_sequences():
    """Test various rotor rotation sequences including edge cases"""

    # Test case 1: Normal three-rotor sequence
    enigma = Enigma(rotor_sequence=["III", "II", "I"], reflector="B",
                    ring_setting=[1, 1, 1], initial_positions="AAA")
    # Rotate 26 times and verify each rotor position

    # Test case 2: Double-stepping sequence
    enigma = Enigma(rotor_sequence=["III", "II", "I"], reflector="B",
                    ring_setting=[1, 1, 1], initial_positions="ADV")
    # Should go ADV -> AEW -> BFX
    enigma.encode("A")  # First step
    assert [r.position for r in enigma.rotors[:-1]] == [4, 5, 23]  # AEW
    enigma.encode("A")  # Second step
    assert [r.position for r in enigma.rotors[:-1]] == [2, 6, 24]  # BFX

    # Test case 3: Beta in rightmost position
    enigma = Enigma(rotor_sequence=["III", "II", "Beta"], reflector="B",
                    ring_setting=[1, 1, 1], initial_positions="AAA")
    initial_positions = [r.position for r in enigma.rotors[:-1]]
    enigma.encode("A")
    # Positions should not change
    assert [r.position for r in enigma.rotors[:-1]] == initial_positions

    # Test case 4: Notch positions with ring settings
    enigma = Enigma(rotor_sequence=["III", "II", "I"], reflector="B",
                    ring_setting=[15, 23, 4], initial_positions="ABC")
    # Verify notch behavior with offset ring settings


if __name__ == '__main__':
    unittest.main()
