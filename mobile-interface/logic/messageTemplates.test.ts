import { GlucoseState } from './glucoseStates';
import { getMessageForState, UserRole } from './messageTemplates';

describe('messageTemplates', () => {
    test('returns correct message for Stable state - Patient', () => {
        const message = getMessageForState(GlucoseState.Stable, UserRole.Patient);
        expect(message.title).toBe("All Good!");
        expect(message.intensity).toBe('low');
    });

    test('returns correct message for Low state - Caregiver', () => {
        const message = getMessageForState(GlucoseState.Low, UserRole.Caregiver);
        expect(message.title).toBe("Low Alert");
        expect(message.intensity).toBe('critical');
    });

    test('returns correct message for Rapid Rise - Clinician', () => {
        const message = getMessageForState(GlucoseState.RapidRise, UserRole.Clinician);
        expect(message.title).toBe("Rapid Glycemic Increase");
        expect(message.intensity).toBe('high');
    });

    test('returns a message for every state and role combo', () => {
        const states = Object.values(GlucoseState);
        const roles = Object.values(UserRole);

        states.forEach(state => {
            roles.forEach(role => {
                const message = getMessageForState(state, role);
                expect(message).toBeDefined();
                expect(message.title).toBeTruthy();
                expect(message.body).toBeTruthy();
                expect(message.intensity).toBeTruthy();
            });
        });
    });
});
