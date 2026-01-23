'use client';

import { useState, useRef } from 'react';
import { transcribeAudio } from '@/lib/api';
import { Transcript } from '@/lib/types';
import LanguageSelector from './LanguageSelector';

interface Props {
  onTranscript: (transcript: Transcript) => void;
  isTranscribing: boolean;
  setIsTranscribing: (value: boolean) => void;
}

export default function FileUpload({ onTranscript, isTranscribing, setIsTranscribing }: Props) {
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check file type - support both audio and video
      const validAudioTypes = ['audio/mpeg', 'audio/wav', 'audio/mp3', 'audio/m4a', 'audio/webm', 'audio/ogg', 'audio/aac', 'audio/flac'];
      const validVideoTypes = ['video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska'];
      const validTypes = [...validAudioTypes, ...validVideoTypes];

      const isValidExtension = /\.(mp3|wav|m4a|webm|ogg|aac|flac|mp4|mov|avi|mkv)$/i.test(file.name);

      if (!validTypes.includes(file.type) && !isValidExtension) {
        setError('Please select a valid audio or video file (MP3, WAV, M4A, MP4, MOV, etc.)');
        return;
      }

      // Check file size (max 100MB for video)
      if (file.size > 100 * 1024 * 1024) {
        setError('File size must be less than 100MB');
        return;
      }

      setSelectedFile(file);
      setError(null);
    }
  };

  const handleTranscribe = async () => {
    if (!selectedFile) return;

    setIsTranscribing(true);
    setError(null);

    try {
      const response = await transcribeAudio(selectedFile, selectedLanguage);

      if (response.success && response.full_text) {
        const transcript: Transcript = {
          fullText: response.full_text,
          segments: response.segments || [],
          language: response.language || selectedLanguage,
          duration: response.duration,
          sourceType: 'file',
          date: new Date().toISOString(),
        };

        onTranscript(transcript);
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
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
    <div className="space-y-6">
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
          MEDIA FILE
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*,video/*"
          onChange={handleFileSelect}
          disabled={isTranscribing}
          className="hidden"
          id="audio-file-input"
        />
        <label
          htmlFor="audio-file-input"
          className={`block w-full px-4 py-8 rounded-lg border-2 border-dashed border-dawt-divider bg-dawt-card text-center cursor-pointer transition-colors hover:border-dawt-accent hover:bg-gray-50 ${
            isTranscribing ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          <svg className="w-12 h-12 mx-auto mb-3 text-dawt-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          {selectedFile ? (
            <div>
              <p className="text-base font-medium text-dawt-text-primary">{selectedFile.name}</p>
              <p className="text-[11px] text-dawt-text-secondary mt-1">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          ) : (
            <div>
              <p className="text-base font-medium text-dawt-text-primary">Choose audio or video</p>
              <p className="text-[11px] text-dawt-text-secondary mt-1">
                MP3, WAV, M4A, MP4, MOV (max 100MB)
              </p>
            </div>
          )}
        </label>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <button
        onClick={handleTranscribe}
        disabled={!selectedFile || isTranscribing}
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
          'TRANSCRIBE FILE'
        )}
      </button>
    </div>
  );
}
