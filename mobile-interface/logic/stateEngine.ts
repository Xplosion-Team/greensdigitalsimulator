
import { classifyGlucoseState, GlucoseState } from './glucoseStates';
import { generateMockData, GlucoseDataPoint } from './mockGlucoseData';

export interface GlucoseStatePoint extends GlucoseDataPoint {
    trend: number;
    state: GlucoseState;
}

export function processGlucoseData(data: GlucoseDataPoint[]): GlucoseStatePoint[] {
    const processedData: GlucoseStatePoint[] = [];

    for (let i = 0; i < data.length; i++) {
        const current = data[i];
        if (!current) continue;

        let trend = 0;

        if (i > 0) {
            // Simple difference for trend (assuming 5 min intervals)
            // trend = (current - prev) / 5 min
            const prev = data[i - 1];
            if (prev) {
                trend = (current.value - prev.value) / 5;
            }
        }

        const state = classifyGlucoseState(current.value, trend);

        processedData.push({
            ...current,
            trend,
            state
        });
    }

    return processedData;
}

if (require.main === module) {
    const mockData = generateMockData();
    const results = processGlucoseData(mockData);
    console.log(`Processed ${results.length} points.`);
    console.log('Sample results:', results.slice(0, 5));

    // Count states
    const stateCounts: Record<string, number> = {};
    results.forEach(p => {
        stateCounts[p.state] = (stateCounts[p.state] || 0) + 1;
    });
    console.log('State Distribution:', stateCounts);
}
