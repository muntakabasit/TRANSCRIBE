import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as DocumentPicker from 'expo-document-picker';
import { Audio } from 'expo-av';
import { MaterialIcons } from '@expo/vector-icons';

const API_URL = 'https://a2d75914-5640-4f09-af56-a4b9e0b7314a-00-1vzd5bc0pcz1x.janeway.replit.dev';

const LANGUAGES = [
  { value: 'auto', label: 'ENGLISH (AUTO-DETECT)' },
  { value: 'pidgin', label: 'GHANAIAN PIDGIN' },
  { value: 'tw', label: 'TWI' },
  { value: 'ig', label: 'IGBO' },
  { value: 'yo', label: 'YORUBA' },
  { value: 'ha', label: 'HAUSA' },
  { value: 'sw', label: 'SWAHILI' },
  { value: 'am', label: 'AMHARIC' },
  { value: 'fr', label: 'FRENCH' },
  { value: 'pt', label: 'PORTUGUESE' },
  { value: 'ee', label: 'EWE' },
  { value: 'dag', label: 'DAGBANI' },
];

export default function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState('');
  const [result, setResult] = useState(null);
  const [recording, setRecording] = useState(null);
  const [showLanguagePicker, setShowLanguagePicker] = useState(false);

  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        const { status } = await Audio.requestPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert('Permission Required', 'Audio recording permission is required');
        }
      }
    })();
  }, []);

  const startRecording = async () => {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      Alert.alert('Recording', 'Recording started...');
    } catch (err) {
      Alert.alert('Error', 'Failed to start recording: ' + err.message);
    }
  };

  const stopRecording = async () => {
    if (!recording) return;

    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      
      await uploadAudioFile(uri);
    } catch (err) {
      Alert.alert('Error', 'Failed to stop recording: ' + err.message);
    }
  };

  const pickAudioFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'audio/*',
        copyToCacheDirectory: true,
      });

      if (result.type === 'success' || !result.canceled) {
        const file = result.assets ? result.assets[0] : result;
        await uploadAudioFile(file.uri);
      }
    } catch (err) {
      Alert.alert('Error', 'Failed to pick file: ' + err.message);
    }
  };

  const uploadAudioFile = async (uri) => {
    try {
      setLoading(true);
      setProgress('Uploading audio...');

      const formData = new FormData();
      formData.append('audio_file', {
        uri,
        type: 'audio/m4a',
        name: 'recording.m4a',
      });
      formData.append('language', selectedLanguage);

      const response = await fetch(`${API_URL}/transcribe`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (data.job_id) {
        pollForResult(data.job_id);
      } else {
        throw new Error('No job ID returned');
      }
    } catch (err) {
      setLoading(false);
      Alert.alert('Error', 'Upload failed: ' + err.message);
    }
  };

  const handleUrlSubmit = async () => {
    if (!videoUrl.trim()) {
      Alert.alert('Error', 'Please enter a video URL');
      return;
    }

    try {
      setLoading(true);
      setProgress('Downloading video...');

      const response = await fetch(`${API_URL}/transcribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_url: videoUrl,
          language: selectedLanguage,
        }),
      });

      const data = await response.json();
      
      if (data.job_id) {
        pollForResult(data.job_id);
      } else {
        throw new Error('No job ID returned');
      }
    } catch (err) {
      setLoading(false);
      Alert.alert('Error', 'Transcription failed: ' + err.message);
    }
  };

  const pollForResult = async (jobId) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/status/${jobId}`);
        const data = await response.json();
        
        setProgress(data.progress || 'Processing...');

        if (data.status === 'completed') {
          clearInterval(interval);
          const resultResponse = await fetch(`${API_URL}/results/${jobId}`);
          const resultData = await resultResponse.json();
          setResult(resultData);
          setLoading(false);
        } else if (data.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
          Alert.alert('Error', data.error || 'Transcription failed');
        }
      } catch (err) {
        clearInterval(interval);
        setLoading(false);
        Alert.alert('Error', 'Status check failed: ' + err.message);
      }
    }, 2000);
  };

  const selectedLangLabel = LANGUAGES.find(l => l.value === selectedLanguage)?.label || 'SELECT LANGUAGE';

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.stripe} />

      <ScrollView style={styles.content} contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>"TRANSCRIBE"</Text>
          <Text style={styles.subtitle}>AUDIO TO TEXT / SOVEREIGN / LOCAL PROCESSING</Text>
        </View>

        {!result && (
          <>
            <View style={styles.card}>
              <View style={styles.cardLabel}>
                <Text style={styles.labelText}>VIDEO URL</Text>
              </View>
              <TextInput
                style={styles.input}
                placeholder="https://..."
                placeholderTextColor="#666"
                value={videoUrl}
                onChangeText={setVideoUrl}
                autoCapitalize="none"
                keyboardType="url"
              />
            </View>

            <View style={styles.card}>
              <View style={styles.cardLabel}>
                <Text style={styles.labelText}>LANGUAGE</Text>
              </View>
              <TouchableOpacity
                style={styles.picker}
                onPress={() => setShowLanguagePicker(!showLanguagePicker)}
              >
                <Text style={styles.pickerText}>{selectedLangLabel}</Text>
                <MaterialIcons name="arrow-drop-down" size={24} color="#000" />
              </TouchableOpacity>
              
              {showLanguagePicker && (
                <View style={styles.pickerOptions}>
                  {LANGUAGES.map((lang) => (
                    <TouchableOpacity
                      key={lang.value}
                      style={styles.pickerOption}
                      onPress={() => {
                        setSelectedLanguage(lang.value);
                        setShowLanguagePicker(false);
                      }}
                    >
                      <Text style={styles.pickerOptionText}>{lang.label}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              )}
            </View>

            <View style={styles.buttonGroup}>
              <TouchableOpacity
                style={styles.primaryButton}
                onPress={handleUrlSubmit}
                disabled={loading}
              >
                <Text style={styles.primaryButtonText}>
                  PROCESS {loading ? '' : '→'}
                </Text>
              </TouchableOpacity>

              <View style={styles.orDivider}>
                <View style={styles.orLine} />
                <Text style={styles.orText}>OR</Text>
                <View style={styles.orLine} />
              </View>

              <TouchableOpacity
                style={styles.secondaryButton}
                onPress={pickAudioFile}
                disabled={loading}
              >
                <MaterialIcons name="upload-file" size={20} color="#fff" />
                <Text style={styles.secondaryButtonText}>UPLOAD FILE</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.secondaryButton}
                onPress={recording ? stopRecording : startRecording}
                disabled={loading}
              >
                <MaterialIcons 
                  name={recording ? 'stop' : 'mic'} 
                  size={20} 
                  color="#fff" 
                />
                <Text style={styles.secondaryButtonText}>
                  {recording ? 'STOP RECORDING' : 'RECORD AUDIO'}
                </Text>
              </TouchableOpacity>
            </View>

            {loading && (
              <View style={styles.loadingCard}>
                <View style={styles.spinner} />
                <Text style={styles.loadingText}>PROCESSING...</Text>
                <Text style={styles.progressText}>{progress}</Text>
              </View>
            )}
          </>
        )}

        {result && (
          <View style={styles.resultCard}>
            <Text style={styles.resultTitle}>TRANSCRIPTION COMPLETE</Text>
            
            <View style={styles.metaInfo}>
              <Text style={styles.metaLabel}>LANGUAGE</Text>
              <Text style={styles.metaValue}>{result.language || 'N/A'}</Text>
            </View>

            <View style={styles.transcriptBox}>
              <Text style={styles.transcriptLabel}>→ TRANSCRIPT</Text>
              <Text style={styles.transcriptText}>{result.text || 'No text available'}</Text>
            </View>

            {result.segments && result.segments.length > 0 && (
              <View style={styles.segmentsBox}>
                <Text style={styles.segmentsLabel}>→ TIMESTAMPED SEGMENTS</Text>
                {result.segments.slice(0, 10).map((segment, index) => (
                  <View key={index} style={styles.segment}>
                    <Text style={styles.segmentTime}>
                      {formatTime(segment.start)} - {formatTime(segment.end)}
                    </Text>
                    <Text style={styles.segmentText}>{segment.text}</Text>
                  </View>
                ))}
              </View>
            )}

            <TouchableOpacity
              style={styles.resetButton}
              onPress={() => {
                setResult(null);
                setVideoUrl('');
                setProgress('');
              }}
            >
              <Text style={styles.resetButtonText}>← NEW TRANSCRIPTION</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  stripe: {
    height: 4,
    backgroundColor: '#000',
  },
  content: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: 40,
  },
  header: {
    marginBottom: 40,
  },
  title: {
    fontSize: 40,
    fontWeight: '900',
    letterSpacing: -1,
    color: '#000',
    textTransform: 'uppercase',
  },
  subtitle: {
    fontSize: 11,
    fontWeight: '400',
    letterSpacing: 1.5,
    color: '#666',
    marginTop: 10,
    textTransform: 'uppercase',
  },
  card: {
    borderWidth: 3,
    borderColor: '#000',
    padding: 20,
    marginBottom: 20,
    position: 'relative',
  },
  cardLabel: {
    position: 'absolute',
    top: -12,
    left: 15,
    backgroundColor: '#fff',
    paddingHorizontal: 10,
  },
  labelText: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1.5,
    color: '#000',
    textTransform: 'uppercase',
  },
  input: {
    fontSize: 16,
    color: '#000',
    padding: 5,
  },
  picker: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 5,
  },
  pickerText: {
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 0.5,
    color: '#000',
  },
  pickerOptions: {
    marginTop: 15,
    borderTopWidth: 2,
    borderTopColor: '#000',
  },
  pickerOption: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  pickerOptionText: {
    fontSize: 13,
    fontWeight: '600',
    letterSpacing: 0.5,
    color: '#000',
  },
  buttonGroup: {
    marginBottom: 20,
  },
  primaryButton: {
    backgroundColor: '#000',
    padding: 20,
    alignItems: 'center',
    marginBottom: 20,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 2,
    textTransform: 'uppercase',
  },
  orDivider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 20,
  },
  orLine: {
    flex: 1,
    height: 2,
    backgroundColor: '#000',
  },
  orText: {
    marginHorizontal: 15,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1.5,
    color: '#000',
  },
  secondaryButton: {
    backgroundColor: '#000',
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
  },
  secondaryButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 1.5,
    marginLeft: 10,
    textTransform: 'uppercase',
  },
  loadingCard: {
    alignItems: 'center',
    padding: 40,
    borderTopWidth: 2,
    borderTopColor: '#000',
  },
  spinner: {
    width: 50,
    height: 50,
    borderWidth: 4,
    borderColor: '#000',
    borderTopColor: 'transparent',
    borderRadius: 0,
    marginBottom: 20,
  },
  loadingText: {
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 1.5,
    color: '#000',
    marginBottom: 10,
  },
  progressText: {
    fontSize: 11,
    color: '#666',
    letterSpacing: 0.5,
  },
  resultCard: {
    borderWidth: 3,
    borderColor: '#000',
    padding: 20,
  },
  resultTitle: {
    fontSize: 24,
    fontWeight: '900',
    letterSpacing: -0.5,
    marginBottom: 20,
    textTransform: 'uppercase',
  },
  metaInfo: {
    marginBottom: 20,
  },
  metaLabel: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1.5,
    color: '#666',
    marginBottom: 5,
  },
  metaValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#000',
  },
  transcriptBox: {
    borderLeftWidth: 4,
    borderLeftColor: '#000',
    paddingLeft: 15,
    marginBottom: 25,
  },
  transcriptLabel: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1.5,
    color: '#000',
    marginBottom: 10,
  },
  transcriptText: {
    fontSize: 15,
    lineHeight: 24,
    color: '#000',
  },
  segmentsBox: {
    marginBottom: 25,
  },
  segmentsLabel: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1.5,
    color: '#000',
    marginBottom: 15,
  },
  segment: {
    borderLeftWidth: 4,
    borderLeftColor: '#000',
    paddingLeft: 15,
    marginBottom: 15,
  },
  segmentTime: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
    color: '#666',
    marginBottom: 5,
  },
  segmentText: {
    fontSize: 14,
    lineHeight: 20,
    color: '#000',
  },
  resetButton: {
    backgroundColor: '#000',
    padding: 15,
    alignItems: 'center',
  },
  resetButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 1.5,
  },
});
