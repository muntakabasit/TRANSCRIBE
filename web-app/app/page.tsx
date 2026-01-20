'use client';

import { useState } from 'react';
import AudioRecorder from '@/components/AudioRecorder';
import URLTranscribe from '@/components/URLTranscribe';
import TranscriptDisplay from '@/components/TranscriptDisplay';
import { Transcript } from '@/lib/types';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'record' | 'url'>('record');
  const [transcript, setTranscript] = useState<Transcript | null>(null);
  const [isTranscribing, setIsTranscribing] = useState(false);

  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 mb-4 shadow-lg">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            DAWT-Transcribe
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Free audio transcription for everyone
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 bg-white dark:bg-gray-800 p-1 rounded-xl shadow-sm">
          <button
            onClick={() => setActiveTab('record')}
            className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all ${
              activeTab === 'record'
                ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              Record
            </div>
          </button>
          <button
            onClick={() => setActiveTab('url')}
            className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all ${
              activeTab === 'url'
                ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
              URL
            </div>
          </button>
        </div>

        {/* Content */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 md:p-8 mb-6">
          {activeTab === 'record' ? (
            <AudioRecorder
              onTranscript={setTranscript}
              isTranscribing={isTranscribing}
              setIsTranscribing={setIsTranscribing}
            />
          ) : (
            <URLTranscribe
              onTranscript={setTranscript}
              isTranscribing={isTranscribing}
              setIsTranscribing={setIsTranscribing}
            />
          )}
        </div>

        {/* Transcript Display */}
        {transcript && (
          <TranscriptDisplay transcript={transcript} />
        )}

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 dark:text-gray-400 mt-12">
          <p>
            Supports 12+ languages including English, Pidgin, Twi, Igbo, Yoruba, and more.
          </p>
          <p className="mt-2">
            <a
              href="https://github.com/muntakabasit/TRANSCRIBE"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 dark:text-primary-400"
            >
              Open Source on GitHub
            </a>
          </p>
        </footer>
      </div>
    </main>
  );
}
