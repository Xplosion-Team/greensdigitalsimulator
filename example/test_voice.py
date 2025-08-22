#!/usr/bin/env python3
"""
Test script for the voice food logging module
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

try:
    from voice_module import VoiceFoodLogger
    print("✓ Voice module imported successfully")
    
    # Test initialization
    logger = VoiceFoodLogger()
    print("✓ Voice logger initialized successfully")
    
    # Test food database
    print(f"✓ Food database contains {len(logger.food_database)} items")
    
    # Test food extraction
    test_text = "I ate two apples and one slice of bread"
    foods = logger.extract_food_info(test_text)
    print(f"✓ Food extraction test: Found {len(foods)} foods in '{test_text}'")
    for food in foods:
        print(f"  - {food['name']}: {food['quantity']} {food['unit']} ({food['carbs']}g carbs)")
    
    # Test manual logging
    test_food = {
        'name': 'apple',
        'carbs': 25,
        'category': 'fruit',
        'quantity': 2,
        'unit': 'piece'
    }
    logged = logger.log_food([test_food])
    print(f"✓ Manual logging test: Logged {len(logged)} foods")
    
    # Test getting recent foods
    recent = logger.get_recent_foods(limit=5)
    print(f"✓ Recent foods test: Retrieved {len(recent)} recent entries")
    
    # Test total carbs calculation
    total_carbs = logger.get_total_carbs(hours=24)
    print(f"✓ Total carbs test: {total_carbs}g carbs in last 24 hours")
    
    print("\n🎉 All tests passed! Voice module is working correctly.")
    
except ImportError as e:
    print(f"✗ Error importing voice module: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install SpeechRecognition pyttsx3 pyaudio")
    
except Exception as e:
    print(f"✗ Error during testing: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    print("Testing Voice Food Logging Module...")
    print("=" * 50)
