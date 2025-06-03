import { useGame } from '../contexts/GameContext';

export default function ScoreBoard() {
  const { state } = useGame();
  const colors = ['bg-blue-500', 'bg-orange-500'];
  return (
    <div className="flex gap-4 text-xl font-bold">
      {state.scores.map((s, i) => (
        <div key={i} className={`px-4 py-2 text-white rounded ${colors[i]}`}>
          Team {i + 1}: {s}
        </div>
      ))}
    </div>
  );
}
