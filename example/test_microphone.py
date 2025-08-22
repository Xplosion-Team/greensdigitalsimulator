#!/usr/bin/env python3
"""
Simple microphone test script
"""

import speech_recognition as sr
import time

def test_microphone():
    """Test if microphone is working"""
    recognizer = sr.Recognizer()
    
    # List available microphones
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")
    
    # Test microphone
    try:
        with sr.Microphone() as source:
            print(f"\nUsing microphone: {source.device_index}")
            
            # Adjust for ambient noise
            print("Adjusting for ambient noise... Please be quiet for 2 seconds.")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("\n🎤 Microphone test ready!")
            print("Please speak something clearly for 5 seconds...")
            print("(You can say anything like 'Hello, this is a test')")
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("\nProcessing speech...")
            
            # Try to recognize speech
            try:
                text = recognizer.recognize_google(audio)
                print(f"✅ SUCCESS! You said: '{text}'")
                print("🎉 Your microphone is working correctly!")
                return True
                
            except sr.UnknownValueError:
                print("❌ Could not understand what you said")
                print("Please try speaking more clearly")
                return False
                
            except sr.RequestError as e:
                print(f"❌ Error with speech recognition service: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error with microphone: {e}")
        return False

def test_simple_audio():
    """Test if we can record audio at all"""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Testing basic audio recording...")
            print("Please make any sound for 3 seconds...")
            
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            print("✅ Audio recording successful!")
            print(f"Audio length: {len(audio.frame_data)} bytes")
            return True
            
    except Exception as e:
        print(f"❌ Audio recording failed: {e}")
        return False

if __name__ == "__main__":
    print("🎤 Microphone Test Script")
    print("=" * 40)
    
    # Test basic audio recording first
    if test_simple_audio():
        print("\n" + "=" * 40)
        # Test speech recognition
        test_microphone()
    else:
        print("\n❌ Basic audio recording failed. Check your microphone permissions.")
        print("On macOS, go to System Preferences > Security & Privacy > Privacy > Microphone")
        print("Make sure your terminal/IDE has microphone access.")
