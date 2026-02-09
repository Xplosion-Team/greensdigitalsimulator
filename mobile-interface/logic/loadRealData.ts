
import fs from 'fs';
import path from 'path';
import type { GlucoseDataPoint } from './mockGlucoseData';

export function loadRealData(filePath: string): GlucoseDataPoint[] {
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

            // Index 1: timestamp (e.g., "2020-03-20 00:05:00")
            // Index 6: cgm (e.g., "104.0")

            const timestamp = columns[1];
            const cgmValStr = columns[6];

            if (!timestamp || !cgmValStr) continue;

            const cgmValue = parseFloat(cgmValStr);

            // Validate data
            if (timestamp && !isNaN(cgmValue)) {
                // Convert timestamp to ISO string if needed, but the format "yyyy-mm-dd hh:mm:ss" 
                // is usually parseable by Date constructor, so let's normalize it to ISO for consistency.
                const dateObj = new Date(timestamp);

                if (!isNaN(dateObj.getTime())) {
                    data.push({
                        timestamp: dateObj.toISOString(),
                        value: cgmValue
                    });
                }
            }
        }

    } catch (error) {
        console.error(`Error loading real data from ${filePath}:`, error);
        return [];
    }

    return data;
}

if (require.main === module) {
    // Default test path
    const testPath = path.resolve(__dirname, '../../src/t1dsim_ai/models/IndividualModel/T1DEXI-01-0102/T1DEXIMAIN_T1DEXI-01-0102.csv');
    console.log(`Loading data from: ${testPath}`);

    if (fs.existsSync(testPath)) {
        const results = loadRealData(testPath);
        console.log(`Loaded ${results.length} data points.`);
        if (results.length > 0) {
            console.log('First 5 points:', results.slice(0, 5));
        }
    } else {
        console.error("File not found at default test path.");
    }
}
