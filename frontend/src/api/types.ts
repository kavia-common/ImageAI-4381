export type HealthResponse = {
  status: string;
  detail?: string;
};

export type ClassificationPrediction = {
  label: string;
  probability: number;
};

export type ClassificationResponse = {
  predictions: ClassificationPrediction[];
};

export type DetectionBox = {
  label: string;
  confidence: number;
  box: [number, number, number, number]; // x1,y1,x2,y2 or similar
};

export type DetectionResponse = {
  detections: DetectionBox[];
  image_url?: string;
};

export type VideoStartResponse = {
  job_id: string;
  message?: string;
};

export type VideoProgressMessage = {
  type: 'progress' | 'complete' | 'error';
  progress?: number; // 0..100
  frame?: number;
  total_frames?: number;
  image_url?: string; // preview image url if provided
  message?: string;
};

export type ApiError = {
  message: string;
  status?: number;
  detail?: unknown;
};
