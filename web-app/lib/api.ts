import { TranscribeResponse } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://transcribe-h3f8nq.fly.dev';

export async function transcribeURL(url: string, language: string = 'en'): Promise<TranscribeResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes timeout

  try {
    const response = await fetch(`${API_URL}/transcribe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url, lang: language }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Failed to transcribe' }));
      throw new Error(error.detail?.message || error.error || 'Transcription failed');
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout - the video may be too long. Please try a shorter video.');
      }
      throw error;
    }
    throw new Error('Transcription failed');
  }
}

export async function transcribeAudio(
  audioBlob: Blob,
  language: string = 'en'
): Promise<TranscribeResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes timeout

  try {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    formData.append('lang', language);

    const response = await fetch(`${API_URL}/transcribe_file`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Failed to transcribe' }));
      throw new Error(error.detail?.message || error.error || 'Transcription failed');
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout - the audio may be too long. Please try a shorter recording.');
      }
      throw error;
    }
    throw new Error('Transcription failed');
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
