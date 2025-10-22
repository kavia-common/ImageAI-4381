import React from 'react';
import type { DetectionBox } from '../api/types';

type Props = {
  src: string;
  boxes: DetectionBox[];
};

export default function DetectionPreview({ src, boxes }: Props) {
  const imgRef = React.useRef<HTMLImageElement | null>(null);
  const [size, setSize] = React.useState<{ w: number; h: number }>({ w: 0, h: 0 });

  function updateSize() {
    const el = imgRef.current;
    if (el) setSize({ w: el.clientWidth, h: el.clientHeight });
  }

  React.useEffect(() => {
    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  return (
    <div style={{ position: 'relative', display: 'inline-block', maxWidth: '100%' }}>
      <img
        ref={imgRef}
        src={src}
        alt="Detection target"
        style={{ width: '100%', height: 'auto', display: 'block' }}
        onLoad={updateSize}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          pointerEvents: 'none'
        }}
      >
        {boxes.map((b, idx) => {
          const [x1, y1, x2, y2] = b.box;
          const left = `${(x1 / (size.w || 1)) * 100}%`;
          const top = `${(y1 / (size.h || 1)) * 100}%`;
          const width = `${((x2 - x1) / (size.w || 1)) * 100}%`;
          const height = `${((y2 - y1) / (size.h || 1)) * 100}%`;
          return (
            <div
              key={idx}
              style={{
                position: 'absolute',
                left,
                top,
                width,
                height,
                border: '2px solid #00d1b2',
                borderRadius: 4,
                boxShadow: '0 0 0 1px rgba(0,0,0,0.2) inset'
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  bottom: '100%',
                  left: 0,
                  background: 'rgba(0,0,0,0.7)',
                  color: 'white',
                  padding: '2px 6px',
                  borderRadius: 4,
                  fontSize: 12,
                  transform: 'translateY(-4px)'
                }}
              >
                {b.label} {Math.round(b.confidence * 100)}%
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
