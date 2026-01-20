export interface Segment {
  start: number;
  end: number;
  text: string;
}

export interface Transcript {
  fullText: string;
  segments: Segment[];
  language: string;
  duration?: number;
  sourceType: 'recording' | 'url' | 'file';
  sourceURL?: string;
  date: string;
}

export interface TranscribeResponse {
  success: boolean;
  full_text?: string;
  segments?: Array<{
    start: number;
    end: number;
    text: string;
  }>;
  language?: string;
  duration?: number;
  error?: string;
}

export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'pidgin', name: 'Pidgin' },
  { code: 'twi', name: 'Twi' },
  { code: 'igbo', name: 'Igbo' },
  { code: 'yoruba', name: 'Yoruba' },
  { code: 'hausa', name: 'Hausa' },
  { code: 'swahili', name: 'Swahili' },
  { code: 'amharic', name: 'Amharic' },
  { code: 'french', name: 'French' },
  { code: 'portuguese', name: 'Portuguese' },
  { code: 'ewe', name: 'Ewe' },
  { code: 'dagbani', name: 'Dagbani' },
] as const;
