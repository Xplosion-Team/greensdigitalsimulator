import speech_recognition as sr
import json
import re
from datetime import datetime
import os

# Try to import text-to-speech, but make it optional
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: pyttsx3 not available. Text-to-speech will be disabled.")

class VoiceFoodLogger:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech if available
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                print(f"Warning: Could not initialize text-to-speech: {e}")
                self.engine = None
        else:
            self.engine = None
        
        # Food database with common foods and their carb content
        self.food_database = {
            "apple": {"carbs": 25, "category": "fruit"},
            "banana": {"carbs": 27, "category": "fruit"},
            "orange": {"carbs": 15, "category": "fruit"},
            "bread": {"carbs": 15, "category": "grains"},
            "rice": {"carbs": 45, "category": "grains"},
            "pasta": {"carbs": 43, "category": "grains"},
            "potato": {"carbs": 37, "category": "vegetables"},
            "corn": {"carbs": 25, "category": "vegetables"},
            "milk": {"carbs": 12, "category": "dairy"},
            "yogurt": {"carbs": 17, "category": "dairy"},
            "chicken": {"carbs": 0, "category": "protein"},
            "fish": {"carbs": 0, "category": "protein"},
            "beef": {"carbs": 0, "category": "protein"},
            "pizza": {"carbs": 30, "category": "fast_food"},
            "burger": {"carbs": 35, "category": "fast_food"},
            "fries": {"carbs": 45, "category": "fast_food"},
            "cake": {"carbs": 50, "category": "dessert"},
            "cookie": {"carbs": 25, "category": "dessert"},
            "ice cream": {"carbs": 30, "category": "dessert"},
            "cereal": {"carbs": 30, "category": "breakfast"},
            "oatmeal": {"carbs": 27, "category": "breakfast"},
            "pancakes": {"carbs": 35, "category": "breakfast"},
            "sandwich": {"carbs": 30, "category": "lunch"},
            "salad": {"carbs": 10, "category": "lunch"},
            "soup": {"carbs": 15, "category": "lunch"},
            "steak": {"carbs": 0, "category": "dinner"},
            "salmon": {"carbs": 0, "category": "dinner"},
            "vegetables": {"carbs": 10, "category": "dinner"}
        }
        
        # Load food log
        self.food_log_file = "food_log.json"
        self.load_food_log()
    
    def load_food_log(self):
        """Load existing food log from file"""
        try:
            if os.path.exists(self.food_log_file):
                with open(self.food_log_file, 'r') as f:
                    self.food_log = json.load(f)
            else:
                self.food_log = []
        except:
            self.food_log = []
    
    def save_food_log(self):
        """Save food log to file"""
        try:
            with open(self.food_log_file, 'w') as f:
                json.dump(self.food_log, f, indent=2)
        except Exception as e:
            print(f"Error saving food log: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error with text-to-speech: {e}")
        else:
            print(f"TTS: {text}")
    
    def listen_for_food(self):
        """Listen for food input and return recognized text"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for food input...")
                self.speak("What food are you eating?")
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text.lower()
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None
    
    def extract_food_info(self, text):
        """Extract food name and quantity from speech text"""
        if not text:
            return None
        
        # Look for quantity patterns
        quantity_patterns = [
            r'(\d+)\s*(cup|cups|gram|grams|g|ounce|ounces|oz|slice|slices|piece|pieces)',
            r'(one|two|three|four|five|six|seven|eight|nine|ten)\s*(cup|cups|gram|grams|g|ounce|ounces|oz|slice|slices|piece|pieces)',
            r'(\d+)\s*(small|medium|large)',
            r'(half|quarter|third)\s*(cup|cups|slice|slices|piece|pieces)'
        ]
        
        quantity = 1
        unit = "serving"
        
        for pattern in quantity_patterns:
            match = re.search(pattern, text)
            if match:
                if match.group(1).isdigit():
                    quantity = int(match.group(1))
                elif match.group(1) in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']:
                    quantity = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'].index(match.group(1)) + 1
                elif match.group(1) == 'half':
                    quantity = 0.5
                elif match.group(1) == 'quarter':
                    quantity = 0.25
                elif match.group(1) == 'third':
                    quantity = 1/3
                
                unit = match.group(2)
                break
        
        # Find food items in the database
        found_foods = []
        for food_name, food_info in self.food_database.items():
            if food_name in text:
                found_foods.append({
                    'name': food_name,
                    'carbs': food_info['carbs'],
                    'category': food_info['category'],
                    'quantity': quantity,
                    'unit': unit
                })
        
        return found_foods
    
    def log_food(self, food_items):
        """Log food items to the food log"""
        timestamp = datetime.now().isoformat()
        
        for food in food_items:
            log_entry = {
                'timestamp': timestamp,
                'food_name': food['name'],
                'carbs': food['carbs'] * food['quantity'],
                'category': food['category'],
                'quantity': food['quantity'],
                'unit': food['unit']
            }
            self.food_log.append(log_entry)
        
        self.save_food_log()
        return food_items
    
    def get_total_carbs(self, hours=24):
        """Get total carbs consumed in the last N hours"""
        now = datetime.now()
        total_carbs = 0
        
        for entry in self.food_log:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            if (now - entry_time).total_seconds() <= hours * 3600:
                total_carbs += entry['carbs']
        
        return total_carbs
    
    def voice_log_food(self):
        """Main method to voice log food intake"""
        self.speak("Starting voice food logging")
        
        # Listen for food input
        text = self.listen_for_food()
        if not text:
            self.speak("I didn't catch that. Please try again.")
            return None
        
        # Extract food information
        food_items = self.extract_food_info(text)
        if not food_items:
            self.speak("I couldn't identify any foods. Please try again.")
            return None
        
        # Log the foods
        logged_foods = self.log_food(food_items)
        
        # Provide feedback
        total_carbs = sum(food['carbs'] * food['quantity'] for food in logged_foods)
        feedback = f"Logged {len(logged_foods)} food items with {total_carbs} grams of carbohydrates."
        self.speak(feedback)
        
        return logged_foods
    
    def get_recent_foods(self, limit=5):
        """Get recent food entries"""
        return self.food_log[-limit:] if self.food_log else []
    
    def clear_food_log(self):
        """Clear the food log"""
        self.food_log = []
        self.save_food_log()
        self.speak("Food log cleared")

# Example usage
if __name__ == "__main__":
    logger = VoiceFoodLogger()
    logger.voice_log_food()
