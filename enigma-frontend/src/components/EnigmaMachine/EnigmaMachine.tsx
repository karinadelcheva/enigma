import React, { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Grid } from '@mui/material';
import { Rotor } from '../Rotor/Rotor.tsx';

// Define the rotor wirings based on historical Enigma machines
const ROTOR_WIRINGS = [
    'EKMFLGDQVZNTOWYHXUSPAIBRCJ', // Rotor I
    'AJDKSIRUXBLHWTMCQGZNPYFVOE', // Rotor II
    'BDFHJLCPRTXVZNYEIWGAKMUSQO'  // Rotor III
];

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

export const EnigmaMachine: React.FC = () => {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [rotorPositions, setRotorPositions] = useState([0, 0, 0]);

    const handleRotorChange = (index: number, value: number) => {
        const newPositions = [...rotorPositions];
        newPositions[index] = value;
        setRotorPositions(newPositions);
    };

    const rotateRotors = (positions: number[]): number[] => {
        const newPositions = [...positions];
        newPositions[0] = (newPositions[0] + 1) % 26;

        if (newPositions[0] === 0) {
            newPositions[1] = (newPositions[1] + 1) % 26;
            if (newPositions[1] === 0) {
                newPositions[2] = (newPositions[2] + 1) % 26;
            }
        }
        return newPositions;
    };

    const encryptLetter = (letter: string, positions: number[]): string => {
        if (!ALPHABET.includes(letter)) return letter;

        let charIndex = ALPHABET.indexOf(letter);

        // Forward through rotors
        for (let i = 0; i < 3; i++) {
            const offset = positions[i];
            const rotor = ROTOR_WIRINGS[i];
            charIndex = (charIndex + offset) % 26;
            charIndex = ALPHABET.indexOf(rotor[charIndex]);
            charIndex = (charIndex - offset + 26) % 26;
        }

        // Reflector (simple reflection)
        charIndex = 25 - charIndex;

        // Backward through rotors
        for (let i = 2; i >= 0; i--) {
            const offset = positions[i];
            const rotor = ROTOR_WIRINGS[i];
            charIndex = (charIndex + offset) % 26;
            charIndex = rotor.indexOf(ALPHABET[charIndex]);
            charIndex = (charIndex - offset + 26) % 26;
        }

        return ALPHABET[charIndex];
    };

    const handleEncrypt = () => {
        let currentPositions = [...rotorPositions];
        let result = '';

        for (const char of input.toUpperCase()) {
            if (ALPHABET.includes(char)) {
                result += encryptLetter(char, currentPositions);
                currentPositions = rotateRotors(currentPositions);
            } else {
                result += char;
            }
        }

        setOutput(result);
    };

    return (
        <Container maxWidth="md" style={{ minHeight: '100vh', paddingTop: '2rem' }}>
            <Paper className="enigma-machine" style={{ padding: '2rem' }}>
                <Typography variant="h4" gutterBottom>Enigma Machine</Typography>

                <Grid container spacing={3} className="rotors-container" style={{ marginBottom: '2rem' }}>
                    {rotorPositions.map((position, index) => (
                        <Grid item xs={4} key={index}>
                            <Rotor
                                position={position}
                                index={index}
                                onChange={(value) => handleRotorChange(index, value)}
                            />
                        </Grid>
                    ))}
                </Grid>

                <TextField
                    label="Input"
                    value={input}
                    onChange={(e) => setInput(e.target.value.toUpperCase())}
                    multiline
                    rows={4}
                    fullWidth
                    variant="outlined"
                    margin="normal"
                />

                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleEncrypt}
                    fullWidth
                    style={{ margin: '1rem 0' }}
                >
                    Encrypt/Decrypt
                </Button>

                <TextField
                    label="Output"
                    value={output}
                    multiline
                    rows={4}
                    fullWidth
                    variant="outlined"
                    margin="normal"
                    InputProps={{ readOnly: true }}
                />
            </Paper>
        </Container>
    );
};