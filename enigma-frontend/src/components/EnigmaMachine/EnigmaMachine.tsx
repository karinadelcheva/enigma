import React, { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Grid } from '@mui/material';
import { Rotor } from '../Rotor/Rotor.tsx'; // Make sure this import path is correct

export const EnigmaMachine: React.FC = () => {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [rotorPositions, setRotorPositions] = useState([0, 0, 0]); // Initial positions for 3 rotors

    const handleRotorChange = (index: number, value: number) => {
        const newPositions = [...rotorPositions];
        newPositions[index] = value;
        setRotorPositions(newPositions);
    };

    const handleEncrypt = () => {
        // For now, keeping the simple reverse to verify everything renders
        // We'll implement the actual encryption logic later
        setOutput(input.split('').reverse().join(''));
    };

    return (
        <Container maxWidth="md" style={{ minHeight: '100vh', paddingTop: '2rem' }}>
            <Paper className="enigma-machine">
                <Typography variant="h4">Enigma Machine</Typography>

                <Grid container spacing={3} className="rotors-container">
                    {rotorPositions.map((position, index) => (
                        <Grid item xs={4} key={index}>
                            <Rotor
                                position={position}
                                index={index}
                                onChange={(value) => handleRotorChange(index, parseInt(value))}
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