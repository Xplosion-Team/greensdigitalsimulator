import { GlucoseState } from './glucoseStates';
import {
    getRecommendation,
    TimeOfDay,
    MealContext,
    ActivityContext
} from './recommendationEngine';

describe('recommendationEngine', () => {
    test('Stable state returns low urgency recommendation', () => {
        const rec = getRecommendation(
            GlucoseState.Stable,
            TimeOfDay.Morning,
            MealContext.Fasting,
            ActivityContext.Resting
        );
        expect(rec.urgency).toBe('low');
        expect(rec.action).toContain('Continue');
    });

    test('High state post-meal advises waiting', () => {
        const rec = getRecommendation(
            GlucoseState.High,
            TimeOfDay.Afternoon,
            MealContext.PostMeal,
            ActivityContext.Resting
        );
        expect(rec.action).toContain('Wait and monitor');
        expect(rec.urgency).toBe('medium');
    });

    test('Low state overnight is immediate urgency', () => {
        const rec = getRecommendation(
            GlucoseState.Low,
            TimeOfDay.Night,
            MealContext.None,
            ActivityContext.Resting
        );
        expect(rec.urgency).toBe('immediate');
        expect(rec.action).toContain('Consume carbs');
    });

    test('Trending High pre-meal advises pre-bolus', () => {
        const rec = getRecommendation(
            GlucoseState.TrendingHigh,
            TimeOfDay.Evening,
            MealContext.PreMeal,
            ActivityContext.Resting
        );
        expect(rec.action).toContain('Pre-bolus');
        expect(rec.urgency).toBe('medium');
    });

    test('Rapid Fall during exercise is high urgency', () => {
        const rec = getRecommendation(
            GlucoseState.RapidFall,
            TimeOfDay.Afternoon,
            MealContext.None,
            ActivityContext.Exercise
        );
        expect(rec.urgency).toBe('high');
        expect(rec.action).toContain('Stop activity');
    });
});
