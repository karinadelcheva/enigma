import React from 'react';
import { TextField, Paper, Typography } from '@mui/material';
import './Rotor.css';

interface RotorProps {
    position: number;
    index: number;
    onChange: (value: string) => void;
}

export const Rotor: React.FC<RotorProps> = ({ position, index, onChange }) => {
    return (
        <Paper className="rotor">
            <Typography variant="subtitle1">Rotor {index + 1}</Typography>
            <TextField
                value={position}
                onChange={(e) => onChange(e.target.value.toUpperCase())}
                inputProps={{
                    maxLength: 1,
                    style: { textAlign: 'center' }
                }}
            />
        </Paper>
    );
};