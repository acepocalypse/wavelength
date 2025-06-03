import { useGame } from '../contexts/GameContext';
import Dial from '../components/Dial';
import ScoreBoard from '../components/ScoreBoard';
import SpectrumCard from '../components/SpectrumCard';

export default function GameScreen() {
  const { state, dispatch } = useGame();

  return (
    <div className="flex flex-col items-center gap-6 min-h-screen py-8">
      <ScoreBoard />
      <SpectrumCard />
      <Dial />

      {state.phase === 'PSYCHIC_SEES' && (
        <button
          className="btn-primary px-4 py-2 bg-indigo-600 text-white rounded"
          onClick={() => dispatch({ type: 'NEXT_TURN' })}
        >
          Start Round
        </button>
      )}
      {state.phase === 'TEAM_DISCUSS' && (
        <button
          className="btn-primary px-4 py-2 bg-emerald-600 text-white rounded"
          onClick={() => dispatch({ type: 'LOCK_GUESS' })}
        >
          Lock Guess
        </button>
      )}
      {state.phase === 'REVEAL' && (
        <button
          className="btn-primary px-4 py-2 bg-orange-600 text-white rounded"
          onClick={() => dispatch({ type: 'NEXT_TURN' })}
        >
          Next Turn
        </button>
      )}
    </div>
  );
}
