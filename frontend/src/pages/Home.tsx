import React from 'react';
import { getApiBaseUrl } from '../config';
import { getHealth } from '../api/client';
import type { HealthResponse } from '../api/types';

export default function Home() {
  const [health, setHealth] = React.useState<HealthResponse | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    let mounted = true;
    setLoading(true);
    getHealth()
      .then((h) => mounted && setHealth(h))
      .catch((e) => {
        console.error(e);
        if (mounted) setError(e?.message ?? 'Failed to fetch health');
      })
      .finally(() => mounted && setLoading(false));
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <section>
      <h1>Welcome to ImageAI Demo</h1>
      <p>Use the navigation to try Image Classification, Object Detection, and Video Detection.</p>
      <div style={{ marginTop: 16, padding: 12, border: '1px solid #eee', borderRadius: 8 }}>
        <h3>Backend Health</h3>
        {loading && <p>Checking backend health...</p>}
        {error && <p style={{ color: 'crimson' }}>Error: {error}</p>}
        {health && (
          <pre style={{ background: '#f9f9f9', padding: 12, borderRadius: 6, overflowX: 'auto' }}>
            {JSON.stringify(health, null, 2)}
          </pre>
        )}
        <small>API Base URL: {getApiBaseUrl()}</small>
      </div>
    </section>
  );
}
