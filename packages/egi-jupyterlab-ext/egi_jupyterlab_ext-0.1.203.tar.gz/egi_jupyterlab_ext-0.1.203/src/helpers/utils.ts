// Downsample: pick every Nth point to reduce chart density
export function downSample<T>(data: T[], maxPoints = 250): T[] {
  if (data.length <= maxPoints) {
    return data;
  }
  const step = Math.ceil(data.length / maxPoints);
  return data.filter((_, idx) => idx % step === 0);
}

export const parseData = (data: [number, string][]) =>
  data.map(([timestamp, value]: [number, string]) => ({
    date: new Date(timestamp * 1000), // Convert to JS Date (ms)
    value: Number(value)
  }));
