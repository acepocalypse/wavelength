export function scoreGuess(target, guess, wedge) {
  const diff = Math.abs(target - guess);
  if (diff <= wedge.bull) return 4;
  if (diff <= wedge.inner) return 3;
  if (diff <= wedge.outer) return 2;
  return 0;
}
