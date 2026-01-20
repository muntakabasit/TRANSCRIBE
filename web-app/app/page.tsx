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
    <main className="min-h-screen bg-dawt-background">
      <div className="container mx-auto px-6 py-16 max-w-2xl">
        {/* Header */}
        <header className="mb-12">
          <div className="flex items-baseline gap-2 mb-1">
            <h1 className="text-xl font-semibold tracking-wider text-dawt-text-primary">
              Transcribe
            </h1>
          </div>
          <p className="text-[11px] font-medium tracking-wide text-dawt-text-secondary opacity-40">
            DAWT
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-8">
          <button
            onClick={() => setActiveTab('record')}
            className={`flex-1 py-3 px-4 rounded-lg text-[13px] font-medium tracking-wide transition-colors ${
              activeTab === 'record'
                ? 'bg-dawt-accent text-white'
                : 'bg-dawt-card text-dawt-text-secondary hover:bg-dawt-card/80'
            }`}
          >
            Record
          </button>
          <button
            onClick={() => setActiveTab('url')}
            className={`flex-1 py-3 px-4 rounded-lg text-[13px] font-medium tracking-wide transition-colors ${
              activeTab === 'url'
                ? 'bg-dawt-accent text-white'
                : 'bg-dawt-card text-dawt-text-secondary hover:bg-dawt-card/80'
            }`}
          >
            URL
          </button>
        </div>

        {/* Content */}
        <div className="bg-dawt-card rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.04)] p-5 mb-4">
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
        <footer className="text-center mt-12 space-y-3">
          <p className="text-[13px] text-dawt-text-secondary">
            Supports 12+ languages including English, Pidgin, Twi, Igbo, Yoruba, and more.
          </p>
          <p>
            <a
              href="https://github.com/muntakabasit/TRANSCRIBE"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[13px] text-dawt-text-secondary hover:text-dawt-text-primary transition-colors"
            >
              Open Source on GitHub →
            </a>
          </p>
        </footer>
      </div>
    </main>
  );
}
