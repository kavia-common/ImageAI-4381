import React from 'react';
import UploadArea from '../components/UploadArea';
import PredictionList from '../components/PredictionList';
import { classifyImage } from '../api/client';
import type { ClassificationPrediction } from '../api/types';

export default function ImageClassification() {
  const [preds, setPreds] = React.useState<ClassificationPrediction[] | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function onFileSelected(file: File) {
    setError(null);
    setLoading(true);
    setPreds(null);
    try {
      const res = await classifyImage(file);
      setPreds(res.predictions || []);
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? 'Classification failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Image Classification</h2>
      <UploadArea onFileSelected={onFileSelected} accept="image/*" />
      {loading && <p>Running classification...</p>}
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {preds && preds.length > 0 && (
        <>
          <h3>Top Predictions</h3>
          <PredictionList predictions={preds} />
        </>
      )}
    </section>
  );
}
