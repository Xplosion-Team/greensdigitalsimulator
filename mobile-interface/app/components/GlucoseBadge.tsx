import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export enum GlucoseState {
    Stable = "Stable",
    TrendingHigh = "Trending High",
    High = "High",
    TrendingLow = "Trending Low",
    Low = "Low",
    RapidRise = "Rapid Rise",
    RapidFall = "Rapid Fall"
}

interface GlucoseBadgeProps {
    state: GlucoseState;
}

const GlucoseBadge: React.FC<GlucoseBadgeProps> = ({ state }) => {
    const getBadgeStyles = () => {
        switch (state) {
            case GlucoseState.High:
            case GlucoseState.RapidRise:
                return { backgroundColor: '#FFEDEB', color: '#D32F2F', borderColor: '#FFCDD2' };
            case GlucoseState.Low:
            case GlucoseState.RapidFall:
                return { backgroundColor: '#FFF4E5', color: '#EF6C00', borderColor: '#FFE0B2' };
            default:
                return { backgroundColor: '#E8F5E9', color: '#2E7D32', borderColor: '#C8E6C9' };
        }
    };

    const styles = getBadgeStyles();

    return (
        <View style={[badgeStyles.container, { backgroundColor: styles.backgroundColor, borderColor: styles.borderColor }]}>
            <Text style={[badgeStyles.text, { color: styles.color }]}>{state}</Text>
        </View>
    );
};

const badgeStyles = StyleSheet.create({
    container: {
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 16,
        borderWidth: 1,
        alignSelf: 'center',
        marginTop: 8,
    },
    text: {
        fontSize: 14,
        fontWeight: '600',
        textTransform: 'uppercase',
    },
});

export default GlucoseBadge;
