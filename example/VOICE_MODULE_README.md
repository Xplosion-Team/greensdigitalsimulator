# Voice Food Logging Module

This module adds voice recognition capabilities to the T1D Simulator, allowing users to document their food intake using voice commands.

## Features

- **Voice Recognition**: Speak to log your food intake
- **Food Database**: Built-in database of common foods with carbohydrate content
- **Quantity Detection**: Automatically detects quantities and units from speech
- **Food Logging**: Persistent storage of food entries with timestamps
- **Manual Entry**: Fallback option for manual food entry
- **Integration**: Seamlessly integrates with the existing T1D simulator

## Installation

1. Install the required dependencies:
```bash
pip install SpeechRecognition==3.10.0 pyttsx3==2.90 pyaudio==0.2.11
```

2. For macOS users, you may need to install portaudio first:
```bash
brew install portaudio
```

3. For Linux users:
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

## Usage

### Voice Logging

1. Click the "Start Voice Logging" button in the sidebar
2. Speak clearly about what you're eating (e.g., "I ate two apples and one slice of bread")
3. The system will automatically detect foods and quantities
4. Your food intake will be logged and the meal size in the simulation will be updated

### Manual Entry

1. Use the "Manual Food Entry" section in the sidebar
2. Enter the food name (e.g., "apple", "bread", "rice")
3. Specify quantity and unit
4. Click "Add to Food Log"

### Supported Foods

The system recognizes common foods including:

**Fruits**: apple, banana, orange
**Grains**: bread, rice, pasta, cereal, oatmeal
**Vegetables**: potato, corn, vegetables
**Dairy**: milk, yogurt
**Protein**: chicken, fish, beef, steak, salmon
**Fast Food**: pizza, burger, fries
**Desserts**: cake, cookie, ice cream
**Beverages**: milk, water, tea

### Quantity Recognition

The system can detect various quantity formats:
- Numbers: "2 apples", "1.5 cups rice"
- Words: "one apple", "two slices bread"
- Fractions: "half cup", "quarter slice"
- Units: cups, grams, ounces, slices, pieces

## API Endpoints

### POST /voice_log_food
Starts voice logging and returns logged foods.

### GET /get_food_log
Returns recent food log entries and 24-hour carbohydrate total.

### POST /clear_food_log
Clears the food log.

### POST /manual_log_food
Manually logs a food item.

## File Structure

```
example/
├── voice_module.py          # Main voice logging module
├── test_voice.py           # Test script
├── app.py                  # Flask app with voice routes
├── templates/index.html    # Updated UI with voice controls
├── requirements.txt        # Updated dependencies
└── food_log.json          # Food log storage (created automatically)
```

## Testing

Run the test script to verify the module is working:

```bash
cd example
python test_voice.py
```

## Troubleshooting

### Microphone Issues
- Ensure your microphone is properly connected and working
- Check system permissions for microphone access
- Try running the test script to verify speech recognition

### Import Errors
- Make sure all dependencies are installed correctly
- For pyaudio issues on macOS, try: `pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio`

### Speech Recognition Issues
- Ensure you have an internet connection (uses Google Speech Recognition)
- Speak clearly and in a quiet environment
- Try different microphone settings

## Integration with T1D Simulator

The voice module integrates seamlessly with the existing T1D simulator:

1. **Automatic Meal Size Updates**: When food is logged, the meal size in the simulation is automatically updated
2. **Carbohydrate Tracking**: Total carbohydrates are calculated and displayed
3. **Simulation Integration**: Logged foods affect the digital twin simulation
4. **Real-time Updates**: The simulation updates immediately when food is logged

## Future Enhancements

- Custom food database expansion
- Barcode scanning integration
- Photo recognition of food
- Meal planning suggestions
- Nutritional analysis and recommendations
- Integration with CGM data for better predictions
