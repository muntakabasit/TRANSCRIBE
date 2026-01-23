'use client';

import { useState, useEffect, useRef } from 'react';
import AudioRecorder from '@/components/AudioRecorder';
import FileUpload from '@/components/FileUpload';
import URLTranscribe from '@/components/URLTranscribe';
import TranscriptDisplay from '@/components/TranscriptDisplay';
import { Transcript } from '@/lib/types';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'record' | 'upload' | 'url'>('record');
  const [transcript, setTranscript] = useState<Transcript | null>(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [showCompletionRitual, setShowCompletionRitual] = useState(false);
  const transcriptRef = useRef<HTMLDivElement>(null);

  // Completion ritual: when transcription finishes
  useEffect(() => {
    if (transcript && !isTranscribing) {
      setShowCompletionRitual(true);
      const timer = setTimeout(() => {
        setShowCompletionRitual(false);
        // Smooth scroll to transcript
        transcriptRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 600);
      return () => clearTimeout(timer);
    }
  }, [transcript, isTranscribing]);

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
            onClick={() => setActiveTab('upload')}
            className={`flex-1 py-3 px-4 rounded-lg text-[13px] font-medium tracking-wide transition-colors ${
              activeTab === 'upload'
                ? 'bg-dawt-accent text-white'
                : 'bg-dawt-card text-dawt-text-secondary hover:bg-dawt-card/80'
            }`}
          >
            Upload
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
          ) : activeTab === 'upload' ? (
            <FileUpload
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

        {/* Completion Ritual */}
        {showCompletionRitual && (
          <div className="fixed inset-0 bg-black bg-opacity-10 flex items-center justify-center pointer-events-none z-50 transition-opacity duration-600">
            <div className="bg-white rounded-full p-4 shadow-lg animate-pulse">
              <svg className="w-12 h-12 text-dawt-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
        )}

        {/* Transcript Display */}
        {transcript && (
          <div ref={transcriptRef}>
            <TranscriptDisplay transcript={transcript} />
          </div>
        )}

        {/* Footer */}
        <footer className="text-center mt-12 space-y-3">
          <p className="text-[13px] text-dawt-text-secondary">
            Supports YouTube, TikTok, Instagram • 12+ languages including English, Pidgin, Twi, Igbo, Yoruba
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
