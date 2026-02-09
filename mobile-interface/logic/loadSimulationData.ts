
import fs from 'fs';
import path from 'path';
import type { GlucoseDataPoint } from './mockGlucoseData';

export function loadSimulationData(filePath: string): GlucoseDataPoint[] {
    const data: GlucoseDataPoint[] = [];

    try {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const lines = fileContent.split('\n');

        // Skip header (line 0)
        for (let i = 1; i < lines.length; i++) {
            const rawLine = lines[i];
            if (!rawLine) continue;
            const line = rawLine.trim();
            if (!line) continue;

            const columns = line.split(',');

            // CSV Header: ... (many columns) ... cgm_NNDT is at index 34 based on inspection
            // Index 2: datetime_local
            // Index 34: cgm_NNDT (Digital Twin Prediction)

            const timestamp = columns[2];
            const cgmValStr = columns[34]; // Using Digital Twin predicted glucose

            if (!timestamp || !cgmValStr) continue;

            const cgmValue = parseFloat(cgmValStr);

            // Validate data
            if (timestamp && !isNaN(cgmValue)) {
                // Determine format of timestamp. 
                // "4/5/20 00:15" might need parsing if Date() doesn't handle it in this env.
                // But usually JS Date handles "MM/DD/YY HH:mm". 
                // Let's try direct conversion.
                const dateObj = new Date(timestamp);

                if (!isNaN(dateObj.getTime())) {
                    data.push({
                        timestamp: dateObj.toISOString(),
                        value: cgmValue
                    });
                } else {
                    // Fallback for custom parsing if needed (e.g. DD/MM vs MM/DD)
                    // console.warn("Invalid date:", timestamp);
                }
            }
        }

    } catch (error) {
        console.error(`Error loading simulation data from ${filePath}:`, error);
        return [];
    }

    return data;
}
