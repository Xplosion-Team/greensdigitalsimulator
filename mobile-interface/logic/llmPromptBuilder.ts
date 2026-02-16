import { GlucoseReading, GlucoseState } from './glucoseStates';

export interface LLMPromptConfig {
    patientAge: number;
    targetRangeMin: number;
    targetRangeMax: number;
    recentNotes?: string;
}

export function buildGlucoseSummaryPrompt(
    readings: GlucoseReading[],
    currentState: GlucoseState,
    config: LLMPromptConfig
): string {
    const avgGlucose = readings.reduce((acc, r) => acc + r.value, 0) / readings.length;
    const timeInRange = readings.filter(r => r.value >= config.targetRangeMin && r.value <= config.targetRangeMax).length / readings.length * 100;

    let readingsText = readings.slice(-10).map(r => `${r.timestamp}: ${r.value} mg/dL (Trend: ${r.trend})`).join('\n');

    return `
Role: You are a clinical diabetes educator assistant.
Context: You are providing a summary for a ${config.patientAge}-year-old patient.
Current State: ${currentState}
Target Range: ${config.targetRangeMin} - ${config.targetRangeMax} mg/dL

Aggregate Stats:
- Average Glucose: ${avgGlucose.toFixed(1)} mg/dL
- Time in Range: ${timeInRange.toFixed(1)}%

Recent Data Points:
${readingsText}

User Notes: ${config.recentNotes || 'None'}

Task: 
1. Summarize the patient's current glycemic status in one sentence.
2. Provide 3 actionable, empathetic tips based on the data and the current state (${currentState}).
3. Use a tone that is encouraging but professional.

Response format:
Summary: [One sentence]
Tips:
- [Tip 1]
- [Tip 2]
- [Tip 3]
`.trim();
}
