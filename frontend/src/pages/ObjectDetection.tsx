import React from 'react';
import UploadArea from '../components/UploadArea';
import DetectionPreview from '../components/DetectionPreview';
import { detectObjects } from '../api/client';
import type { DetectionResponse } from '../api/types';

export default function ObjectDetection() {
  const [result, setResult] = React.useState<DetectionResponse | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [imgUrl, setImgUrl] = React.useState<string | null>(null);

  async function onFileSelected(file: File) {
    setError(null);
    setResult(null);
    setImgUrl(URL.createObjectURL(file));
    setLoading(true);
    try {
      const res = await detectObjects(file);
      setResult(res);
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? 'Detection failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Object Detection</h2>
      <UploadArea onFileSelected={onFileSelected} accept="image/*" />
      {loading && <p>Detecting objects...</p>}
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {result && imgUrl && (
        <>
          <h3>Result</h3>
          <DetectionPreview src={imgUrl} boxes={result.detections} />
        </>
      )}
    </section>
  );
}
