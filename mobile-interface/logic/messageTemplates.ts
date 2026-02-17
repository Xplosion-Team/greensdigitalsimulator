import { GlucoseState } from './glucoseStates';

export enum UserRole {
    Patient = "Patient",
    Caregiver = "Caregiver",
    Clinician = "Clinician"
}

export interface MessageTemplate {
    title: string;
    body: string;
    intensity: 'low' | 'medium' | 'high' | 'critical';
}

const messages: Record<GlucoseState, Record<UserRole, MessageTemplate>> = {
    [GlucoseState.Stable]: {
        [UserRole.Patient]: {
            title: "All Good!",
            body: "Your glucose is stable. Keep up the great work!",
            intensity: 'low'
        },
        [UserRole.Caregiver]: {
            title: "Stable Status",
            body: "Glucose levels are currently stable and in range.",
            intensity: 'low'
        },
        [UserRole.Clinician]: {
            title: "Stable",
            body: "Patient glucose is within target range with no significant trends.",
            intensity: 'low'
        }
    },
    [GlucoseState.TrendingHigh]: {
        [UserRole.Patient]: {
            title: "Trending Up",
            body: "Your glucose is starting to rise. Consider checking your recent activity or meals.",
            intensity: 'medium'
        },
        [UserRole.Caregiver]: {
            title: "Rising Glucose",
            body: "Noticeable upward trend in glucose levels.",
            intensity: 'medium'
        },
        [UserRole.Clinician]: {
            title: "Upward Trend",
            body: "Patient glucose shows a steady upward trend (>1 mg/dL/min).",
            intensity: 'medium'
        }
    },
    [GlucoseState.High]: {
        [UserRole.Patient]: {
            title: "High Glucose",
            body: "Your glucose is above 180 mg/dL. Please follow your high glucose protocol.",
            intensity: 'high'
        },
        [UserRole.Caregiver]: {
            title: "High Alert",
            body: "Glucose has exceeded the high threshold (180 mg/dL).",
            intensity: 'high'
        },
        [UserRole.Clinician]: {
            title: "Hyperglycemia",
            body: "Patient glucose is currently hyperglycemic (>180 mg/dL).",
            intensity: 'high'
        }
    },
    [GlucoseState.TrendingLow]: {
        [UserRole.Patient]: {
            title: "Trending Down",
            body: "Your glucose is starting to drop. Keep an eye on how you're feeling.",
            intensity: 'medium'
        },
        [UserRole.Caregiver]: {
            title: "Falling Glucose",
            body: "Noticeable downward trend in glucose levels.",
            intensity: 'medium'
        },
        [UserRole.Clinician]: {
            title: "Downward Trend",
            body: "Patient glucose shows a steady downward trend (>1 mg/dL/min).",
            intensity: 'medium'
        }
    },
    [GlucoseState.Low]: {
        [UserRole.Patient]: {
            title: "Low Glucose",
            body: "Your glucose is below 70 mg/dL. Please consume 15g of fast-acting carbs immediately.",
            intensity: 'critical'
        },
        [UserRole.Caregiver]: {
            title: "Low Alert",
            body: "Glucose has dropped below the low threshold (70 mg/dL). Immediate action may be needed.",
            intensity: 'critical'
        },
        [UserRole.Clinician]: {
            title: "Hypoglycemia",
            body: "Patient glucose is currently hypoglycemic (<70 mg/dL).",
            intensity: 'critical'
        }
    },
    [GlucoseState.RapidRise]: {
        [UserRole.Patient]: {
            title: "Rapid Rise",
            body: "Your glucose is rising very quickly. Consider if a bolus correction is needed.",
            intensity: 'high'
        },
        [UserRole.Caregiver]: {
            title: "Rapid Rise Alert",
            body: "Glucose is rising sharply (>2 mg/dL/min).",
            intensity: 'high'
        },
        [UserRole.Clinician]: {
            title: "Rapid Glycemic Increase",
            body: "Patient glucose is increasing at a rate >2 mg/dL/min.",
            intensity: 'high'
        }
    },
    [GlucoseState.RapidFall]: {
        [UserRole.Patient]: {
            title: "Rapid Fall",
            body: "Your glucose is dropping very quickly. Have some carbs ready just in case.",
            intensity: 'high'
        },
        [UserRole.Caregiver]: {
            title: "Rapid Fall Alert",
            body: "Glucose is dropping sharply (>2 mg/dL/min).",
            intensity: 'high'
        },
        [UserRole.Clinician]: {
            title: "Rapid Glycemic Decrease",
            body: "Patient glucose is decreasing at a rate >2 mg/dL/min.",
            intensity: 'high'
        }
    }
};

export function getMessageForState(state: GlucoseState, role: UserRole): MessageTemplate {
    return messages[state][role];
}
