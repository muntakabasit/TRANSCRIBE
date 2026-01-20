# DAWT-Transcribe Web App

Free web-based audio transcription app. No App Store required!

## Quick Start

```bash
cd web-app
npm install
npm run dev
```

Open http://localhost:3000

## Features

- 🎙️ **Record Audio** - Browser-based recording
- 🔗 **Transcribe URLs** - YouTube, audio files, etc.
- 🌍 **12+ Languages** - English, Pidgin, African languages, and more
- 📱 **PWA Ready** - Install to home screen like a native app
- 🎨 **Modern UI** - Clean, responsive design
- 🚀 **Free Forever** - No subscriptions or limits

## Deploy to Vercel (Free)

1. Push this folder to GitHub
2. Go to https://vercel.com/new
3. Import your repository
4. Deploy! (automatic)

Your app will be live at `https://your-app.vercel.app`

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=https://transcribe-h3f8nq.fly.dev
```

## Remaining Components to Create

The following components still need to be created. Copy the code below:

### components/LanguageSelector.tsx

```typescript
'use client';

import { SUPPORTED_LANGUAGES } from '@/lib/types';

interface Props {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export default function LanguageSelector({ value, onChange, disabled }: Props) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
      className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {SUPPORTED_LANGUAGES.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.name}
        </option>
      ))}
    </select>
  );
}
```

### components/URLTranscribe.tsx

```typescript
'use client';

import { useState } from 'react';
import { transcribeURL } from '@/lib/api';
import { Transcript, SUPPORTED_LANGUAGES } from '@/lib/types';
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
```

### components/TranscriptDisplay.tsx

```typescript
'use client';

import { Transcript } from '@/lib/types';
import { useState } from 'react';

interface Props {
  transcript: Transcript;
}

export default function TranscriptDisplay({ transcript }: Props) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(transcript.fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadText = () => {
    const blob = new Blob([transcript.fullText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transcript-${new Date().toISOString()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 md:p-8 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Transcript
        </h2>
        <div className="flex gap-2">
          <button
            onClick={copyToClipboard}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            title="Copy to clipboard"
          >
            {copied ? (
              <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            )}
          </button>
          <button
            onClick={downloadText}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            title="Download as text"
          >
            <svg className="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>
        </div>
      </div>

      <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-400">
        <span className="flex items-center gap-1">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
          </svg>
          {transcript.language.toUpperCase()}
        </span>
        {transcript.duration && (
          <span className="flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {Math.floor(transcript.duration)}s
          </span>
        )}
      </div>

      <div className="prose dark:prose-invert max-w-none">
        <p className="text-gray-900 dark:text-white whitespace-pre-wrap">
          {transcript.fullText}
        </p>
      </div>

      {transcript.segments.length > 0 && (
        <details className="mt-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400">
            View timestamps ({transcript.segments.length} segments)
          </summary>
          <div className="mt-4 space-y-2 max-h-96 overflow-y-auto">
            {transcript.segments.map((segment, i) => (
              <div key={i} className="flex gap-3 text-sm">
                <span className="text-gray-500 dark:text-gray-400 font-mono min-w-[80px]">
                  {Math.floor(segment.start)}s - {Math.floor(segment.end)}s
                </span>
                <span className="text-gray-700 dark:text-gray-300">{segment.text}</span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
```

## Install Dependencies

```bash
npm install
```

## Run Development Server

```bash
npm run dev
```

## Build for Production

```bash
npm run build
npm start
```

## Deploy

Push to GitHub and deploy on Vercel for free!

## Tech Stack

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Fly.io Backend API

## License

MIT
