const DEFAULT_API_BASE = 'http://localhost:8000';

export function getApiBaseUrl(): string {
  const url = import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE;
  return String(url).replace(/\/+$/, '');
}

export function getWsBaseUrl(): string {
  const http = getApiBaseUrl();
  if (http.startsWith('https://')) return 'wss://' + http.slice('https://'.length);
  if (http.startsWith('http://')) return 'ws://' + http.slice('http://'.length);
  // fallback assume host
  return 'ws://' + http;
}
