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
    <div className="space-y-8">
      <div>
        <label className="block text-[13px] font-medium tracking-wide text-dawt-text-secondary mb-2">
          LANGUAGE
        </label>
        <LanguageSelector
          value={selectedLanguage}
          onChange={setSelectedLanguage}
          disabled={isRecording || isTranscribing}
        />
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="flex flex-col items-center space-y-10 py-12">
        <div className="text-center space-y-3">
          <h2 className="text-xl font-semibold tracking-wider text-dawt-text-primary">
            {isRecording ? 'RECORDING' : isTranscribing ? 'TRANSCRIBING' : 'READY'}
          </h2>

          {isRecording && (
            <p className="text-[13px] text-dawt-text-secondary">
              {formatTime(recordingTime)}
            </p>
          )}

          {!isRecording && !isTranscribing && (
            <p className="text-[13px] text-dawt-text-secondary">
              Tap to start recording
            </p>
          )}

          {isTranscribing && (
            <p className="text-[13px] text-dawt-text-secondary">
              Processing your audio...
            </p>
          )}
        </div>

        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isTranscribing}
          className={`
            w-20 h-20 rounded-full transition-all
            ${
              isRecording
                ? 'bg-red-500'
                : isTranscribing
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-dawt-accent hover:bg-opacity-90'
            }
          `}
        >
          <div className="flex items-center justify-center">
            {isTranscribing ? (
              <svg
                className="animate-spin h-8 w-8 text-white"
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
              <div className="w-6 h-6 bg-white" />
            ) : (
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                />
              </svg>
            )}
          </div>
        </button>
      </div>
    </div>
  );
}
