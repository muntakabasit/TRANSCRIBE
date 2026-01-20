import { TranscribeResponse } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://transcribe-h3f8nq.fly.dev';

export async function transcribeURL(url: string, language: string = 'en'): Promise<TranscribeResponse> {
  const response = await fetch(`${API_URL}/transcribe`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url, lang: language }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Failed to transcribe' }));
    throw new Error(error.error || 'Transcription failed');
  }

  return response.json();
}

export async function transcribeAudio(
  audioBlob: Blob,
  language: string = 'en'
): Promise<TranscribeResponse> {
  const formData = new FormData();
  formData.append('file', audioBlob, 'recording.webm');
  formData.append('lang', language);

  const response = await fetch(`${API_URL}/transcribe-file`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Failed to transcribe' }));
    throw new Error(error.error || 'Transcription failed');
  }

  return response.json();
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
