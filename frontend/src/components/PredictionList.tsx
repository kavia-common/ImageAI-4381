import React from 'react';
import type { ClassificationPrediction } from '../api/types';

type Props = {
  predictions: ClassificationPrediction[];
};

export default function PredictionList({ predictions }: Props) {
  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {predictions.map((p) => (
        <li
          key={p.label}
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            padding: '8px 12px',
            border: '1px solid #eee',
            borderRadius: 8,
            marginBottom: 8
          }}
        >
          <span>{p.label}</span>
          <span style={{ fontVariantNumeric: 'tabular-nums' }}>
            {(p.probability * 100).toFixed(2)}%
          </span>
        </li>
      ))}
    </ul>
  );
}
