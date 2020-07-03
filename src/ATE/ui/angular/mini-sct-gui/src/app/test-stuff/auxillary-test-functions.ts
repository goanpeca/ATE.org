export function wait(ms = 1000) {
  return new Promise(resolve => {
    setTimeout(resolve, ms);
  });
}

export async function waitUntil(fn, fnCondition, pollIntervall, timeout) {
  let startTime = performance.now();
  let  timeoutReached = false;
  while (!fnCondition()) {
    await wait(pollIntervall);
    fn();
    if (performance.now() - startTime > timeout) {
      timeoutReached = true;
      break;
    }
  }
  return !timeoutReached;
}
