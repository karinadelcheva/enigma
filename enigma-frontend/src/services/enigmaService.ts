import axios from 'axios';
import { EnigmaConfig, EnigmaResponse } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const enigmaService = {
    encrypt: async (text: string, config: EnigmaConfig): Promise<EnigmaResponse> => {
        try {
            const response = await axios.post(`${API_URL}/encode`, {
                text,
                rotor_settings: config.rotors.map(r => r.position).join(''),
                ring_settings: config.rotors.map(r => r.ring_setting).join(''),
                plugboard: config.plugboard
            });
            return response.data;
        } catch (error) {
            console.error('Encryption error:', error);
            throw error;
        }
    }
};