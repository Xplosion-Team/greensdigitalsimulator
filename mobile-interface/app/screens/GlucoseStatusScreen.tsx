import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import * as Speech from 'expo-speech';
import GlucoseBadge, { GlucoseState } from '../components/GlucoseBadge';

interface GlucoseStatusScreenProps {
    currentGlucose: number;
    trend: number;
    state: GlucoseState;
    message: { title: string; body: string };
    recommendation: { action: string; reason: string; urgency: string };
    onRefresh: () => void;
}

const GlucoseStatusScreen: React.FC<GlucoseStatusScreenProps> = ({
    currentGlucose,
    trend,
    state,
    message,
    recommendation,
    onRefresh,
}) => {
    const getTrendIcon = (trend: number) => {
        if (trend > 1) return '↑';
        if (trend < -1) return '↓';
        return '→';
    };

    const getUrgencyColor = (urgency: string) => {
        switch (urgency) {
            case 'immediate': return '#D32F2F';
            case 'high': return '#EF6C00';
            case 'medium': return '#FBC02D';
            default: return '#2E7D32';
        }
    };

    const speakStatus = () => {
        const textToSpeak = `Your glucose is ${currentGlucose} mg per deciliter and is ${state}. ${message.title}. ${message.body}. Recommendation: ${recommendation.action}`;
        Speech.speak(textToSpeak, {
            language: 'en',
            pitch: 1.0,
            rate: 0.9,
        });
    };

    return (
        <ScrollView style={styles.container} contentContainerStyle={styles.content}>
            <View
                style={styles.card}
                accessibilityLabel={`Glucose Status: ${currentGlucose} mg per deciliter. State: ${state}`}
                accessibilityRole="summary"
            >
                <Text style={styles.header}>Glucose Status</Text>

                <View style={styles.glucoseContainer}>
                    <Text style={styles.glucoseValue}>{currentGlucose}</Text>
                    <Text style={styles.glucoseUnit}>mg/dL</Text>
                    <Text
                        style={styles.trendArrow}
                        accessibilityLabel={`Trend: ${trend > 1 ? 'Rising' : trend < -1 ? 'Falling' : 'Stable'}`}
                    >
                        {getTrendIcon(trend)}
                    </Text>
                </View>

                <GlucoseBadge state={state} />
            </View>

            <TouchableOpacity
                style={styles.speakButton}
                onPress={speakStatus}
                accessibilityLabel="Read current status out loud"
                accessibilityRole="button"
                accessibilityHint="Reads your glucose level, state, and recommendation"
            >
                <Text style={styles.speakButtonText}>🔊 Speak Status</Text>
            </TouchableOpacity>

            <View style={styles.section} accessibilityRole="text">
                <Text style={styles.sectionTitle}>{message.title}</Text>
                <Text style={styles.sectionBody}>{message.body}</Text>
            </View>

            <View
                style={[styles.section, styles.recommendationSection, { borderLeftColor: getUrgencyColor(recommendation.urgency) }]}
                accessibilityRole="text"
            >
                <Text style={styles.sectionTitle}>Recommendation</Text>
                <Text style={styles.actionText}>{recommendation.action}</Text>
                <Text style={styles.reasonText}>{recommendation.reason}</Text>
            </View>

            <TouchableOpacity
                style={styles.refreshButton}
                onPress={onRefresh}
                accessibilityLabel="Refresh glucose data"
                accessibilityRole="button"
            >
                <Text style={styles.refreshButtonText}>Refresh Data</Text>
            </TouchableOpacity>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },
    content: {
        padding: 20,
        paddingTop: 60,
    },
    card: {
        backgroundColor: '#FFFFFF',
        borderRadius: 24,
        padding: 24,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 12,
        elevation: 8,
        marginBottom: 20,
    },
    header: {
        fontSize: 16,
        color: '#64748B',
        fontWeight: '600',
        marginBottom: 16,
    },
    glucoseContainer: {
        flexDirection: 'row',
        alignItems: 'baseline',
    },
    glucoseValue: {
        fontSize: 64,
        fontWeight: 'bold',
        color: '#1E293B',
    },
    glucoseUnit: {
        fontSize: 20,
        color: '#64748B',
        marginLeft: 4,
        fontWeight: '500',
    },
    trendArrow: {
        fontSize: 40,
        color: '#3B82F6',
        marginLeft: 12,
    },
    speakButton: {
        backgroundColor: '#E2E8F0',
        borderRadius: 12,
        paddingVertical: 12,
        paddingHorizontal: 16,
        alignItems: 'center',
        marginBottom: 24,
        alignSelf: 'stretch',
        minHeight: 48, // Accessibility: minimum touch target size
    },
    speakButtonText: {
        color: '#475569',
        fontSize: 16,
        fontWeight: '600',
    },
    section: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 20,
        marginBottom: 16,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        shadowRadius: 8,
        elevation: 4,
    },
    recommendationSection: {
        borderLeftWidth: 6,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1E293B',
        marginBottom: 8,
    },
    sectionBody: {
        fontSize: 16,
        color: '#475569',
        lineHeight: 24,
    },
    actionText: {
        fontSize: 18,
        fontWeight: '600',
        color: '#0F172A',
        marginBottom: 4,
    },
    reasonText: {
        fontSize: 15,
        color: '#64748B',
        fontStyle: 'italic',
    },
    refreshButton: {
        backgroundColor: '#3B82F6',
        borderRadius: 16,
        paddingVertical: 16,
        alignItems: 'center',
        marginTop: 8,
        minHeight: 56, // Accessibility: touch target
    },
    refreshButtonText: {
        color: '#FFFFFF',
        fontSize: 18,
        fontWeight: 'bold',
    },
});

export default GlucoseStatusScreen;
