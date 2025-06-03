import { useGame } from '../contexts/GameContext';

export default function SpectrumCard() {
  const { state } = useGame();
  const [left, right] = state.spectrum;
  return (
    <div className="flex w-full max-w-md justify-between items-center text-2xl font-semibold">
      <span>{left}</span>
      <span>{right}</span>
    </div>
  );
}
