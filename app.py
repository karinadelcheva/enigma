from flask import Flask, request, jsonify
from flask_cors import CORS
from enigma.enigma import Enigma

app = Flask(__name__)
CORS(app)

enigma_machine = None


@app.route('/init', methods=['POST'])
def initialize_enigma():
    global enigma_machine
    data = request.json
    rotor_names = data.get('rotors', ['I', 'II', 'III'])
    reflector = data.get('reflector', 'B')
    positions = data.get('positions', 'AAA')
    plugboard_pairs = data.get('plugboard', [])

    enigma_machine = Enigma(rotor_names, reflector)
    enigma_machine.rotor_positions(positions)

    for pair in plugboard_pairs:
        enigma_machine.plugboard.add(pair)

    return jsonify({"status": "initialized"})


@app.route('/encode', methods=['POST'])
def encode_character():
    global enigma_machine
    data = request.json
    char = data['character'].upper()

    if not enigma_machine:
        return jsonify({"error": "Enigma machine not initialized"}), 400

    result = enigma_machine.encode_character(char)

    # Get the current state of the machine
    rotor_positions = [rotor.position_letter for rotor in enigma_machine.rotors]

    return jsonify({
        "input": char,
        "output": result,
        "rotorPositions": rotor_positions
    })


if __name__ == '__main__':
    app.run(debug=True)