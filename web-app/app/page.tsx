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
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-slate-900 dark:to-gray-900">
      <div className="container mx-auto px-4 py-12 max-w-5xl">
        {/* Header */}
        <header className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500 mb-6 shadow-2xl shadow-indigo-500/30 animate-pulse-slow">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <h1 className="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 dark:from-blue-400 dark:via-indigo-400 dark:to-purple-400 mb-4 tracking-tight">
            DAWT-Transcribe
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 font-medium">
            Free audio transcription for everyone
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex gap-3 mb-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg p-2 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setActiveTab('record')}
            className={`flex-1 py-4 px-8 rounded-xl font-semibold transition-all duration-300 ${
              activeTab === 'record'
                ? 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/50 scale-105'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 hover:scale-102'
            }`}
          >
            <div className="flex items-center justify-center gap-3">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              <span className="text-lg">Record</span>
            </div>
          </button>
          <button
            onClick={() => setActiveTab('url')}
            className={`flex-1 py-4 px-8 rounded-xl font-semibold transition-all duration-300 ${
              activeTab === 'url'
                ? 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/50 scale-105'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 hover:scale-102'
            }`}
          >
            <div className="flex items-center justify-center gap-3">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
              <span className="text-lg">URL</span>
            </div>
          </button>
        </div>

        {/* Content */}
        <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-gray-200 dark:border-gray-700 p-8 md:p-12 mb-8">
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
        <footer className="text-center text-gray-600 dark:text-gray-400 mt-16 space-y-4">
          <p className="text-base">
            Supports 12+ languages including English, Pidgin, Twi, Igbo, Yoruba, and more.
          </p>
          <p>
            <a
              href="https://github.com/muntakabasit/TRANSCRIBE"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 font-medium transition-colors"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
              Open Source on GitHub
            </a>
          </p>
        </footer>
      </div>
    </main>
  );
}
