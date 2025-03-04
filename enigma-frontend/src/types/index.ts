export interface RotorSettings {
  position: string;
  ring_setting?: string;
}

export interface EnigmaConfig {
  rotors: RotorSettings[];
  plugboard?: Record<string, string>;
}

export interface EnigmaResponse {
  result: string;
  rotor_positions?: string[];
}