#!/usr/bin/env python3
"""
Debug voice recognition step by step
"""

import speech_recognition as sr
import os
import subprocess

def check_flac():
    """Check if FLAC is available"""
    try:
        result = subprocess.run(['flac', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FLAC is available")
            print(f"FLAC version: {result.stdout.split()[1]}")
            return True
        else:
            print("❌ FLAC is not working properly")
            return False
    except FileNotFoundError:
        print("❌ FLAC not found in PATH")
        return False

def test_voice_recognition():
    """Test voice recognition with detailed debugging"""
    recognizer = sr.Recognizer()
    
    print("🎤 Voice Recognition Debug Test")
    print("=" * 50)
    
    # Check FLAC
    print("\n1. Checking FLAC installation...")
    flac_ok = check_flac()
    
    # List microphones
    print("\n2. Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"   {index}: {name}")
    
    # Test microphone
    print("\n3. Testing microphone...")
    try:
        with sr.Microphone() as source:
            print(f"   Using microphone: {source.device_index}")
            
            # Adjust for ambient noise
            print("   Adjusting for ambient noise... Please be quiet for 2 seconds.")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("\n   🎤 Ready to listen!")
            print("   Please say something clearly like 'Hello world' or 'Test one two three'")
            print("   You have 5 seconds to speak...")
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print(f"\n   ✅ Audio captured! Length: {len(audio.frame_data)} bytes")
            
            # Try to recognize speech
            print("\n4. Attempting speech recognition...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"   ✅ SUCCESS! Recognized: '{text}'")
                return True
                
            except sr.UnknownValueError:
                print("   ❌ Google Speech Recognition could not understand audio")
                print("   This could mean:")
                print("   - Speech was not clear enough")
                print("   - Background noise was too loud")
                print("   - Microphone quality issues")
                return False
                
            except sr.RequestError as e:
                print(f"   ❌ Error with Google Speech Recognition service: {e}")
                print("   This could mean:")
                print("   - No internet connection")
                print("   - Google service is down")
                print("   - FLAC conversion issues")
                return False
                
    except Exception as e:
        print(f"   ❌ Error with microphone: {e}")
        return False

def test_manual_food_logging():
    """Test manual food logging as a fallback"""
    print("\n5. Testing manual food logging...")
    
    try:
        from voice_module import VoiceFoodLogger
        logger = VoiceFoodLogger()
        
        # Test manual logging
        test_food = {
            'name': 'apple',
            'carbs': 25,
            'category': 'fruit',
            'quantity': 2,
            'unit': 'piece'
        }
        
        logged = logger.log_food([test_food])
        print(f"   ✅ Manual food logging works! Logged: {len(logged)} foods")
        
        # Test food extraction
        test_text = "I ate two apples and one slice of bread"
        foods = logger.extract_food_info(test_text)
        print(f"   ✅ Food extraction works! Found {len(foods)} foods in text")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Manual food logging failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Voice Module Debug Test")
    print("=" * 50)
    
    # Test voice recognition
    voice_ok = test_voice_recognition()
    
    # Test manual logging as fallback
    manual_ok = test_manual_food_logging()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   Voice Recognition: {'✅ Working' if voice_ok else '❌ Failed'}")
    print(f"   Manual Food Logging: {'✅ Working' if manual_ok else '❌ Failed'}")
    
    if not voice_ok:
        print("\n💡 TROUBLESHOOTING TIPS:")
        print("   1. Check microphone permissions in System Preferences")
        print("   2. Try speaking more clearly and loudly")
        print("   3. Reduce background noise")
        print("   4. Use manual food entry as a fallback")
        print("   5. Check internet connection for Google Speech Recognition")
    
    if manual_ok:
        print("\n✅ You can still use the food logging feature via manual entry!")
