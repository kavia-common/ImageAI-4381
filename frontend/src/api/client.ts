import axios from 'axios';
import { getApiBaseUrl, getWsBaseUrl } from '../config';
import type {
  HealthResponse,
  ClassificationResponse,
  DetectionResponse,
  VideoStartResponse
} from './types';

// Create axios client configured from env
export const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 60000
});

// PUBLIC_INTERFACE
export async function getHealth(): Promise<HealthResponse> {
  /** Get API health. */
  const { data } = await api.get<HealthResponse>('/api/v1/health');
  return data;
}

// PUBLIC_INTERFACE
export async function classifyImage(file: File): Promise<ClassificationResponse> {
  /** Classify a single image via multipart/form-data POST. */
  const form = new FormData();
  form.append('file', file);
  const { data } = await api.post<ClassificationResponse>('/api/v1/classify', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
}

// PUBLIC_INTERFACE
export async function detectObjects(file: File): Promise<DetectionResponse> {
  /** Run object detection on a single image via multipart/form-data POST. */
  const form = new FormData();
  form.append('file', file);
  const { data } = await api.post<DetectionResponse>('/api/v1/detect', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
}

// PUBLIC_INTERFACE
export async function startVideoDetection(file: File): Promise<VideoStartResponse> {
  /** Start a video detection job. Returns a job_id to subscribe to websocket updates. */
  const form = new FormData();
  form.append('file', file);
  const { data } = await api.post<VideoStartResponse>('/api/v1/video/start', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
}

// PUBLIC_INTERFACE
export function openVideoWs(jobId: string): WebSocket {
  /** Open WebSocket for video job progress updates. */
  const wsUrl = `${getWsBaseUrl()}/ws/video/${jobId}`;
  return new WebSocket(wsUrl);
}
