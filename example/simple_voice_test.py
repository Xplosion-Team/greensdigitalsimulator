#!/usr/bin/env python3
"""
Very simple voice test
"""

import speech_recognition as sr

print("🎤 Simple Voice Test")
print("Say 'Hello' or 'Test' clearly...")

recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        
        print("Processing...")
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: '{text}'")
        
except sr.UnknownValueError:
    print("❌ Could not understand audio")
    print("Try speaking louder and more clearly")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check microphone permissions in System Preferences")
