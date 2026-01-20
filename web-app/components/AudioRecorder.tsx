'use client';

import { useState, useRef, useEffect } from 'react';
import { transcribeAudio } from '@/lib/api';
import { Transcript, SUPPORTED_LANGUAGES } from '@/lib/types';
import LanguageSelector from './LanguageSelector';

interface Props {
  onTranscript: (transcript: Transcript) => void;
  isTranscribing: boolean;
  setIsTranscribing: (value: boolean) => void;
}

export default function AudioRecorder({ onTranscript, isTranscribing, setIsTranscribing }: Props) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        stream.getTracks().forEach((track) => track.stop());

        // Transcribe
        await handleTranscribe(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      setError('Microphone permission denied or not available');
      console.error('Recording error:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);

      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };

  const handleTranscribe = async (audioBlob: Blob) => {
    setIsTranscribing(true);
    setError(null);

    try {
      const response = await transcribeAudio(audioBlob, selectedLanguage);

      if (response.success && response.full_text) {
        const transcript: Transcript = {
          fullText: response.full_text,
          segments: response.segments || [],
          language: response.language || selectedLanguage,
          duration: response.duration,
          sourceType: 'recording',
          date: new Date().toISOString(),
        };

        onTranscript(transcript);
      } else {
        setError(response.error || 'Transcription failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Transcription failed');
    } finally {
      setIsTranscribing(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Language
        </label>
        <LanguageSelector
          value={selectedLanguage}
          onChange={setSelectedLanguage}
          disabled={isRecording || isTranscribing}
        />
      </div>

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      <div className="flex flex-col items-center space-y-8 py-8">
        {isRecording && (
          <div className="text-4xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-pink-500 animate-pulse">
            {formatTime(recordingTime)}
          </div>
        )}

        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isTranscribing}
          className={`
            relative w-28 h-28 rounded-full shadow-2xl transition-all transform hover:scale-110 active:scale-95
            ${
              isRecording
                ? 'bg-gradient-to-br from-red-500 to-pink-500 animate-pulse shadow-red-500/50'
                : isTranscribing
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500 hover:shadow-indigo-500/50'
            }
          `}
        >
          <div className="absolute inset-0 flex items-center justify-center">
            {isTranscribing ? (
              <svg
                className="animate-spin h-10 w-10 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            ) : isRecording ? (
              <div className="w-8 h-8 rounded-md bg-white shadow-lg" />
            ) : (
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2.5}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                />
              </svg>
            )}
          </div>
        </button>

        <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
          {isTranscribing
            ? 'Transcribing your audio...'
            : isRecording
            ? 'Tap to stop recording'
            : 'Tap to start recording'}
        </p>
      </div>
    </div>
  );
}
