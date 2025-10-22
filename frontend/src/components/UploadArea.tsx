import React from 'react';

type Props = {
  onFileSelected: (file: File) => void;
  accept?: string;
};

export default function UploadArea({ onFileSelected, accept }: Props) {
  const inputRef = React.useRef<HTMLInputElement | null>(null);
  const [dragOver, setDragOver] = React.useState(false);

  function onPickClick() {
    inputRef.current?.click();
  }

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) onFileSelected(file);
    e.currentTarget.value = '';
  }

  function onDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) onFileSelected(file);
  }

  function onDragOver(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(true);
  }

  function onDragLeave(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
  }

  const borderColor = dragOver ? '#0d6efd' : '#ccc';

  return (
    <div>
      <div
        onClick={onPickClick}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        role="button"
        tabIndex={0}
        style={{
          border: `2px dashed ${borderColor}`,
          padding: 24,
          borderRadius: 12,
          textAlign: 'center',
          cursor: 'pointer',
          background: dragOver ? '#f0f7ff' : '#fafafa'
        }}
      >
        <p style={{ margin: 0 }}>
          Drag and drop a file here, or <span style={{ color: '#0d6efd' }}>click to select</span>.
        </p>
        {accept && <small>Accepted: {accept}</small>}
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          onChange={onFileChange}
          style={{ display: 'none' }}
        />
      </div>
    </div>
  );
}
