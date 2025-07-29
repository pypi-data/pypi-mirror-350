async function getMetricData(
  prometheusUrl: string,
  metricName: string,
  start: number,
  end: number,
  step: number
): Promise<any> {
  const url = new URL(`${prometheusUrl}/api/v1/query_range`);
  url.searchParams.set('query', metricName);
  url.searchParams.set('start', start.toString());
  url.searchParams.set('end', end.toString());
  url.searchParams.set('step', step.toString());

  const resp = await fetch(url.toString());
  return await resp.json();
}

async function getScaphMetrics(prometheusUrl: string): Promise<string[]> {
  const resp = await fetch(`${prometheusUrl}/api/v1/label/__name__/values`);
  const data = await resp.json();
  return data.data.filter((name: string) => name.startsWith('scaph_'));
}

export default async function getScaphData() {
  try {
    const prometheusUrl = 'http://mc-a4.lab.uvalight.net/prometheus/';
    const metrics: string[] = [];
    await getScaphMetrics(prometheusUrl).then(response =>
      metrics.push(...response)
    );
    console.log('### Metrics response ### \n ', metrics);

    const end = Math.floor(Date.now() / 1000);
    const start = end - 3600; // last hour
    const step = 15;

    const results: Map<string, [number, string][]> = new Map();

    for (const metricName of metrics) {
      const metricData = await getMetricData(
        prometheusUrl,
        metricName,
        start,
        end,
        step
      );
      const data = metricData.data.result[0].values; // For some reason the response is within a [].
      results.set(metricName, data);
    }

    return results;
  } catch (error) {
    console.error('Error fetching Scaph metrics:', error);
    return new Map<string, [number, string][]>();
  }
}
