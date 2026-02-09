
import path from 'path';
import fs from 'fs';
import { loadSimulationData } from './loadSimulationData';
import { processGlucoseData } from './stateEngine';

const SIMULATION_FILE = path.resolve(__dirname, '../../example/sim_output_unique.csv');

if (!fs.existsSync(SIMULATION_FILE)) {
    console.error(`Simulation file not found at: ${SIMULATION_FILE}`);
    console.error("Please run the Python simulation first!");
    process.exit(1);
}

console.log("VERSION 8 - DEBUG START");
console.log(`Loading simulation data from: ${SIMULATION_FILE}`);
const stats = fs.statSync(SIMULATION_FILE);
console.log(`DEBUG: File size: ${stats.size} bytes`);
const rawData = loadSimulationData(SIMULATION_FILE);
console.log(`Loaded ${rawData.length} data points.`);

if (rawData.length === 0) {
    console.error("No valid data points loaded.");
    process.exit(1);
}

console.log("First 3 points:", rawData.slice(0, 3));

console.log("Processing data with State Engine...");
const processedData = processGlucoseData(rawData);

console.log(`Processed ${processedData.length} output states.`);

// Analyze produced states
const stateCounts: Record<string, number> = {};
processedData.forEach(p => {
    stateCounts[p.state] = (stateCounts[p.state] || 0) + 1;
});

console.log("Integration Results - State Distribution:", stateCounts);

// Export mapped data for frontend usage (optional)
const outputJsonPath = path.resolve(__dirname, 'integrated_data.json');
fs.writeFileSync(outputJsonPath, JSON.stringify(processedData, null, 2));
console.log(`Integrated data saved to: ${outputJsonPath}`);
