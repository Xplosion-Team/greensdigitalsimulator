import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, SafeAreaView, ActivityIndicator, Text, TouchableOpacity, Platform } from 'react-native';
import * as Speech from 'expo-speech';
import GlucoseStatusScreen from './screens/GlucoseStatusScreen';
import { getMessageForState, UserRole } from '../logic/messageTemplates';
import { getRecommendation, TimeOfDay, MealContext, ActivityContext } from '../logic/recommendationEngine';

// Types from logic
import { GlucoseState } from './components/GlucoseBadge';

// Dynamic API URL for Universal Compatibility
// localhost works for web/simulators on the same machine
// 192.168.4.25 is required for physical devices on the same Wi-Fi
const API_BASE = Platform.OS === 'web' ? 'localhost' : '192.168.4.25';
const API_URL = `http://${API_BASE}:8000`;

export default function App() {
  const [dataPoints, setDataPoints] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSimulation();
  }, []);

  const fetchSimulation = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/simulate/1`);
      if (!response.ok) throw new Error('Failed to fetch simulation');
      const data = await response.json();
      setDataPoints(data);
      setCurrentIndex(0);
    } catch (err: any) {
      setError(err.message || 'Connection Error');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    if (dataPoints.length === 0) return;

    // Cycle through real-time data
    const nextIndex = (currentIndex + 1) % dataPoints.length;
    const nextPoint = dataPoints[nextIndex];

    // Auto-read if critical intensity
    const nextMessage = getMessageForState(nextPoint.state as any, UserRole.Patient);
    if (nextMessage.intensity === 'critical' || nextMessage.intensity === 'high') {
      const textToSpeak = `Alert: ${nextMessage.title}. ${nextMessage.body}`;
      Speech.speak(textToSpeak);
    }

    setCurrentIndex(nextIndex);
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#3B82F6" />
        <Text style={styles.loadingText}>Connecting to Digital Twin...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>⚠️ {error}</Text>
        <TouchableOpacity onPress={fetchSimulation} style={styles.retryButton}>
          <Text style={styles.retryText}>Retry Connection</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const currentPoint = dataPoints[currentIndex];
  if (!currentPoint) return null;

  // Derive logic-driven content
  const message = getMessageForState(currentPoint.state as any, UserRole.Patient);
  const recommendation = getRecommendation(
    currentPoint.state as any,
    TimeOfDay.Morning,
    MealContext.None,
    ActivityContext.Resting
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      <GlucoseStatusScreen
        currentGlucose={Math.round(currentPoint.cgm_NNDT || currentPoint.value || 0)} // Use Digital Twin value
        trend={currentPoint.trend || 0}
        state={currentPoint.state as any}
        message={message}
        recommendation={recommendation}
        onRefresh={handleRefresh}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F7FA',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F7FA',
    padding: 20,
  },
  loadingText: {
    marginTop: 20,
    fontSize: 16,
    color: '#64748B',
  },
  errorText: {
    fontSize: 16,
    color: '#D32F2F',
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#3B82F6',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 12,
  },
  retryText: {
    color: '#FFFFFF',
    fontWeight: '600',
  }
});
