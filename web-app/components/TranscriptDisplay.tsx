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
    <div className="bg-dawt-card rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.04)] p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-dawt-divider pb-3">
        <h2 className="text-[13px] font-semibold tracking-widest text-dawt-text-primary">
          TRANSCRIPT
        </h2>
        <div className="flex gap-2">
          <button
            onClick={copyToClipboard}
            className="p-2 rounded-lg hover:bg-gray-50 transition-colors"
            title="Copy to clipboard"
          >
            {copied ? (
              <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className="w-5 h-5 text-dawt-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            )}
          </button>
          <button
            onClick={downloadText}
            className="p-2 rounded-lg hover:bg-gray-50 transition-colors"
            title="Download as text"
          >
            <svg className="w-5 h-5 text-dawt-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>
        </div>
      </div>

      <div className="flex gap-4 text-[11px] font-medium tracking-wide">
        <span className="text-dawt-text-secondary">
          {transcript.language.toUpperCase()}
        </span>
        {transcript.duration && (
          <>
            <span className="text-dawt-text-secondary">•</span>
            <span className="text-dawt-text-secondary">
              {Math.floor(transcript.duration)}s
            </span>
          </>
        )}
      </div>

      <div className="pt-2">
        <p className="text-base leading-[1.625] text-dawt-text-primary whitespace-pre-wrap">
          {transcript.fullText}
        </p>
      </div>

      {transcript.segments.length > 0 && (
        <details className="mt-6 border-t border-dawt-divider pt-4">
          <summary className="cursor-pointer text-[13px] font-medium text-dawt-text-secondary hover:text-dawt-text-primary">
            View timestamps ({transcript.segments.length} segments)
          </summary>
          <div className="mt-4 space-y-3 max-h-96 overflow-y-auto">
            {transcript.segments.map((segment, i) => (
              <div key={i} className="flex gap-4 text-sm">
                <span className="text-[12px] text-dawt-text-timestamp font-mono min-w-[90px] flex-shrink-0">
                  {Math.floor(segment.start)}s - {Math.floor(segment.end)}s
                </span>
                <span className="text-dawt-text-primary">{segment.text}</span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
