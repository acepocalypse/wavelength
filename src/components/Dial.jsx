import { motion, useDragControls } from 'framer-motion';
import { useGame } from '../contexts/GameContext';

export default function Dial() {
  const { state, dispatch } = useGame();
  const { targetAngle, guessAngle, phase } = state;
  const showTarget = phase === 'REVEAL';
  const controls = useDragControls();

  const handleDrag = (_, info) => {
    const rect = info.target.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height;
    const angle = Math.atan2(cy - info.point.y, info.point.x - cx) * 180 / Math.PI;
    const clamped = Math.max(0, Math.min(180, angle));
    dispatch({ type: 'SET_GUESS', payload: clamped });
  };

  return (
    <div className="relative w-dial h-dial">
      <svg viewBox="0 0 200 100" className="w-full h-full">
        <path d="M0 100 A100 100 0 0 1 200 100" fill="#e2e8f0" />
      </svg>

      {showTarget && (
        <div
          className="absolute inset-0 origin-bottom"
          style={{ transform: `rotate(${targetAngle - 90}deg)` }}
        >
          <div className="w-1 h-full bg-green-500 mx-auto opacity-70" />
        </div>
      )}

      <motion.div
        className="absolute left-1/2 bottom-0 origin-bottom"
        drag
        dragControls={controls}
        dragMomentum={false}
        onDrag={handleDrag}
        style={{ rotate: guessAngle - 90 }}
      >
        <div className="w-1 h-28 bg-red-500 rounded-t" />
      </motion.div>
    </div>
  );
}
