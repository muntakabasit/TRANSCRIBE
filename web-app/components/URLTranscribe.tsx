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
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Language
        </label>
        <LanguageSelector
          value={selectedLanguage}
          onChange={setSelectedLanguage}
          disabled={isTranscribing}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          YouTube URL or Audio Link
        </label>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://youtube.com/watch?v=..."
          disabled={isTranscribing}
          className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
        />
      </div>

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={!url.trim() || isTranscribing}
        className="w-full py-3 px-6 rounded-lg font-medium text-white bg-gradient-to-r from-primary-500 to-accent-500 hover:shadow-lg transform transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
      >
        {isTranscribing ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Transcribing...
          </span>
        ) : (
          'Transcribe URL'
        )}
      </button>
    </form>
  );
}
