import React, { createContext, useContext, useReducer } from 'react';

const spectra = [
  ['Hot', 'Cold'],
  ['Expensive', 'Cheap'],
  ['Fiction', 'Non‑Fiction'],
  ['Salty', 'Sweet'],
  ['Old', 'New'],
];

const initialState = {
  round: 1,
  currentTeam: 0,          // 0 = blue, 1 = orange
  scores: [0, 0],
  phase: 'PSYCHIC_SEES',
  spectrum: spectra[0],
  targetAngle: Math.floor(Math.random() * 181),
  guessAngle: 90,
  wedge: { bull: 8, inner: 14, outer: 22 },
};

function reducer(state, action) {
  switch (action.type) {
    case 'SET_GUESS':
      return { ...state, guessAngle: action.payload };
    case 'LOCK_GUESS':
      return { ...state, phase: 'REVEAL' };
    case 'NEXT_TURN': {
      const nextSpectrum = spectra[Math.floor(Math.random() * spectra.length)];
      return {
        ...state,
        round: state.round + 1,
        currentTeam: (state.currentTeam + 1) % 2,
        spectrum: nextSpectrum,
        targetAngle: Math.floor(Math.random() * 181),
        guessAngle: 90,
        phase: 'PSYCHIC_SEES',
      };
    }
    default:
      return state;
  }
}

const GameContext = createContext();
export const useGame = () => useContext(GameContext);

export function GameProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <GameContext.Provider value={{ state, dispatch }}>
      {children}
    </GameContext.Provider>
  );
}
