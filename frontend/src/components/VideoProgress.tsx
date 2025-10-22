import React from 'react';

type Props = {
  progress: number;
  status: string;
  jobId?: string;
};

export default function VideoProgress({ progress, status, jobId }: Props) {
  return (
    <div style={{ marginTop: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
        <strong>Status:</strong>
        <span>{status}</span>
      </div>
      <div style={{ height: 12, background: '#eee', borderRadius: 8, overflow: 'hidden' }}>
        <div
          style={{
            width: `${Math.min(Math.max(progress, 0), 100)}%`,
            background: '#0d6efd',
            height: '100%'
          }}
        />
      </div>
      {typeof jobId === 'string' && (
        <small style={{ display: 'block', marginTop: 8, color: '#555' }}>Job ID: {jobId}</small>
      )}
    </div>
  );
}
