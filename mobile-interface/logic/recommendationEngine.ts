import { GlucoseState } from './glucoseStates';

export enum TimeOfDay {
    Morning = "Morning",
    Afternoon = "Afternoon",
    Evening = "Evening",
    Night = "Night"
}

export enum MealContext {
    PreMeal = "Pre-meal",
    PostMeal = "Post-meal",
    Fasting = "Fasting",
    None = "None"
}

export enum ActivityContext {
    Resting = "Resting",
    Active = "Active",
    Exercise = "Exercise",
    PostExercise = "Post-exercise"
}

export interface Recommendation {
    action: string;
    reason: string;
    urgency: 'low' | 'medium' | 'high' | 'immediate';
}

export function getRecommendation(
    state: GlucoseState,
    time: TimeOfDay,
    meal: MealContext,
    activity: ActivityContext
): Recommendation {
    // Logic for High/Rapid Rise
    if (state === GlucoseState.High || state === GlucoseState.RapidRise) {
        if (meal === MealContext.PostMeal) {
            return {
                action: "Wait and monitor.",
                reason: "Your glucose is high after a meal. This is expected, but monitor for 1-2 hours before correcting.",
                urgency: 'medium'
            };
        }
        if (activity === ActivityContext.Exercise) {
            return {
                action: "Consider a small correction bolus if advised by doctor.",
                reason: "Glucose is high during exercise. Be careful as exercise can sometimes keep glucose high initially.",
                urgency: 'medium'
            };
        }
        if (time === TimeOfDay.Night) {
            return {
                action: "Check for ketones if very high.",
                reason: "High glucose before bed or overnight needs caution to avoid overnight hyperglycemia.",
                urgency: 'high'
            };
        }
        return {
            action: "Check hydration and consider a correction dose.",
            reason: "Glucose is above target range.",
            urgency: 'medium'
        };
    }

    // Logic for Low/Rapid Fall
    if (state === GlucoseState.Low || state === GlucoseState.RapidFall) {
        const isCrisis = state === GlucoseState.Low;
        if (activity === ActivityContext.Exercise || activity === ActivityContext.Active) {
            return {
                action: "Stop activity and consume 15-30g of fast-acting carbs.",
                reason: "Low glucose during or after activity is dangerous. Rest immediately.",
                urgency: isCrisis ? 'immediate' : 'high'
            };
        }
        if (time === TimeOfDay.Night) {
            return {
                action: "Consume carbs and set an alarm for 1 hour.",
                reason: "Nocturnal hypoglycemia risk. Ensure you are stable before sleeping.",
                urgency: isCrisis ? 'immediate' : 'high'
            };
        }
        return {
            action: "Consume 15g of fast-acting carbs.",
            reason: "Your glucose is low or dropping rapidly. Follow the 15-15 rule.",
            urgency: isCrisis ? 'immediate' : 'high'
        };
    }

    // Logic for Trending High
    if (state === GlucoseState.TrendingHigh) {
        if (meal === MealContext.PreMeal) {
            return {
                action: "Pre-bolus 5-10 minutes earlier than usual.",
                reason: "Glucose is already trending up before your meal.",
                urgency: 'medium'
            };
        }
        return {
            action: "Consider a short walk.",
            reason: "Light activity can help stabilize a slow rise.",
            urgency: 'low'
        };
    }

    // Logic for Trending Low
    if (state === GlucoseState.TrendingLow) {
        if (activity === ActivityContext.Active) {
            return {
                action: "Have a small snack (10g carbs).",
                reason: "You are active and glucose is trending down.",
                urgency: 'medium'
            };
        }
        return {
            action: "Monitor closely.",
            reason: "Glucose is slowly decreasing. No immediate action needed if above 90.",
            urgency: 'low'
        };
    }

    // Stable state
    return {
        action: "Continue your current routine.",
        reason: "Your glucose is stable and within your target range.",
        urgency: 'low'
    };
}
