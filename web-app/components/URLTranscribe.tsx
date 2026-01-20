'use client';

import { useState } from 'react';
import { transcribeURL } from '@/lib/api';
import { Transcript } from '@/lib/types';
import LanguageSelector from './LanguageSelector';

interface Props {
  onTranscript: (transcript: Transcript) => void;
  isTranscribing: boolean;
  setIsTranscribing: (value: boolean) => void;
}

export default function URLTranscribe({ onTranscript, isTranscribing, setIsTranscribing }: Props) {
  const [url, setUrl] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsTranscribing(true);
    setError(null);

    try {
      const response = await transcribeURL(url, selectedLanguage);

      if (response.success && response.full_text) {
        const transcript: Transcript = {
          fullText: response.full_text,
          segments: response.segments || [],
          language: response.language || selectedLanguage,
          duration: response.duration,
          sourceType: 'url',
          sourceURL: url,
          date: new Date().toISOString(),
        };

        onTranscript(transcript);
        setUrl('');
      } else {
        setError(response.error || 'Transcription failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Transcription failed');
    } finally {
      setIsTranscribing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-[13px] font-medium tracking-wide text-dawt-text-secondary mb-2">
          LANGUAGE
        </label>
        <LanguageSelector
          value={selectedLanguage}
          onChange={setSelectedLanguage}
          disabled={isTranscribing}
        />
      </div>

      <div>
        <label className="block text-[13px] font-medium tracking-wide text-dawt-text-secondary mb-2">
          VIDEO OR AUDIO URL
        </label>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="YouTube, TikTok, Instagram..."
          disabled={isTranscribing}
          className="w-full px-4 py-3 rounded-lg border border-dawt-divider bg-dawt-card text-dawt-text-primary placeholder-dawt-text-secondary placeholder-opacity-50 focus:outline-none focus:border-dawt-accent disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <p className="mt-2 text-[11px] text-dawt-text-secondary">
          Supports YouTube, TikTok, Instagram, and more
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={!url.trim() || isTranscribing}
        className="w-full h-14 rounded-lg text-[14px] font-semibold tracking-wider text-white bg-dawt-accent hover:bg-opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isTranscribing ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            TRANSCRIBING...
          </span>
        ) : (
          'TRANSCRIBE URL'
        )}
      </button>
    </form>
  );
}
