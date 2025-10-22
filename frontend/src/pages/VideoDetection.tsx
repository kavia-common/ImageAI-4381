import React from 'react';
import UploadArea from '../components/UploadArea';
import VideoProgress from '../components/VideoProgress';
import { openVideoWs, startVideoDetection } from '../api/client';
import type { VideoProgressMessage } from '../api/types';

export default function VideoDetection() {
  const [jobId, setJobId] = React.useState<string | null>(null);
  const [progress, setProgress] = React.useState<number>(0);
  const [status, setStatus] = React.useState<string>('Idle');
  const [error, setError] = React.useState<string | null>(null);
  const wsRef = React.useRef<WebSocket | null>(null);

  async function onFileSelected(file: File) {
    cleanupWs();
    setJobId(null);
    setProgress(0);
    setStatus('Uploading...');
    setError(null);

    try {
      const res = await startVideoDetection(file);
      setJobId(res.job_id);
      setStatus('Processing...');
      const ws = openVideoWs(res.job_id);
      wsRef.current = ws;
      ws.onopen = () => {
        setStatus('Connected, receiving updates...');
      };
      ws.onmessage = (event) => {
        try {
          const msg: VideoProgressMessage = JSON.parse(event.data);
          if (msg.type === 'progress' && typeof msg.progress === 'number') {
            setProgress(msg.progress);
            setStatus(`Processing... ${msg.progress}%`);
          } else if (msg.type === 'complete') {
            setProgress(100);
            setStatus('Complete');
            ws.close();
          } else if (msg.type === 'error') {
            setError(msg.message ?? 'Job error');
            setStatus('Error');
            ws.close();
          }
        } catch (e) {
          console.error('Failed to parse WS message', e);
        }
      };
      ws.onerror = () => {
        setError('WebSocket error');
      };
      ws.onclose = () => {
        // keep status if complete, else indicate disconnected
        if (progress < 100 && !error) {
          setStatus('Disconnected');
        }
      };
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? 'Failed to start video detection');
      setStatus('Error');
    }
  }

  function cleanupWs() {
    if (wsRef.current) {
      try {
        wsRef.current.close();
      } catch {}
      wsRef.current = null;
    }
  }

  React.useEffect(() => {
    return () => cleanupWs();
  }, []);

  return (
    <section>
      <h2>Video Detection</h2>
      <UploadArea onFileSelected={onFileSelected} accept="video/*" />
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      <VideoProgress progress={progress} status={status} jobId={jobId ?? undefined} />
    </section>
  );
}
