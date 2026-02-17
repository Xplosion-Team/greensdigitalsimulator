import { buildGlucoseSummaryPrompt, LLMPromptConfig } from './llmPromptBuilder';
import { GlucoseReading, GlucoseState } from './glucoseStates';

describe('llmPromptBuilder', () => {
    test('builds a prompt with correct clinical context', () => {
        const readings: GlucoseReading[] = [
            { timestamp: "2026-02-16T10:00:00", value: 120, trend: 0.5 },
            { timestamp: "2026-02-16T10:05:00", value: 125, trend: 1.0 },
            { timestamp: "2026-02-16T10:10:00", value: 135, trend: 2.0 }
        ];

        const config: LLMPromptConfig = {
            patientAge: 45,
            targetRangeMin: 70,
            targetRangeMax: 180,
            recentNotes: "Feeling a bit tired."
        };

        const prompt = buildGlucoseSummaryPrompt(readings, GlucoseState.TrendingHigh, config);

        expect(prompt).toContain('45-year-old patient');
        expect(prompt).toContain('Trending High');
        expect(prompt).toContain('Feeling a bit tired.');
        expect(prompt).toContain('Average Glucose: 126.7 mg/dL');
        expect(prompt).toContain('Time in Range: 100.0%');
    });

    test('handles missing notes gracefully', () => {
        const readings: GlucoseReading[] = [
            { timestamp: "2026-02-16T10:00:00", value: 200, trend: 0.5 }
        ];

        const config: LLMPromptConfig = {
            patientAge: 30,
            targetRangeMin: 70,
            targetRangeMax: 180
        };

        const prompt = buildGlucoseSummaryPrompt(readings, GlucoseState.High, config);
        expect(prompt).toContain('User Notes: None');
    });
});
