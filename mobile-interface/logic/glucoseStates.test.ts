
import { classifyGlucoseState, GlucoseState } from './glucoseStates';

describe('classifyGlucoseState', () => {
    test('should classify Low glucose', () => {
        expect(classifyGlucoseState(60, 0)).toBe(GlucoseState.Low);
    });

    test('should classify High glucose', () => {
        expect(classifyGlucoseState(200, 0)).toBe(GlucoseState.High);
    });

    test('should classify Stable glucose', () => {
        expect(classifyGlucoseState(100, 0.5)).toBe(GlucoseState.Stable);
    });

    test('should classify Rapid Rise', () => {
        expect(classifyGlucoseState(100, 2.5)).toBe(GlucoseState.RapidRise);
    });

    test('should classify Rapid Fall', () => {
        expect(classifyGlucoseState(100, -2.5)).toBe(GlucoseState.RapidFall);
    });
});
