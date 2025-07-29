# Emotion-Aware Narrative Engine

A sophisticated emotion detection system for games and interactive narratives that combines scene context with emotion detection to provide accurate emotional analysis and mood suggestions.

## Features

- **Emotion Detection**: Uses advanced NLP to detect emotions in text
- **Scene Context**: Understands different scene types and their emotional implications
- **Context Overrides**: Allows for specific emotional contexts to modify detected emotions
- **Mood Suggestions**: Provides game mood cues based on detected emotions
- **Flexible Integration**: Works with various dialogue systems and game engines

## Supported Emotions

### Basic Emotions
- joy
- anger
- sadness
- fear
- surprise
- disgust
- neutral

### Additional Emotions
- hope
- excitement
- gratitude
- anxiety
- disappointment
- guilt
- jealousy
- confusion
- sympathy

## Scene Types

The system supports various scene types that can influence emotion detection:

### Social Scenes
- `formal_meeting` - Business meetings, conferences
- `party` - Celebrations, festivals, gatherings
- `family_gathering` - Family reunions, home gatherings
- `interview` - Job interviews, auditions
- `negotiation` - Business deals, bargaining

### Action Scenes
- `chase_scene` - Pursuits, escapes
- `stealth_mission` - Infiltration, sneaking
- `training_session` - Practice, learning
- `competition` - Contests, matches, tournaments
- `rescue_mission` - Saving, recovery operations

### Emotional Scenes
- `funeral` - Memorials, burials
- `wedding` - Marriage ceremonies
- `graduation` - Commencement ceremonies
- `reunion` - Meetings, gatherings
- `farewell` - Goodbyes, departures

### Mystery/Thriller Scenes
- `investigation` - Detective work, searches
- `interrogation` - Questioning, examinations
- `discovery` - Findings, revelations
- `revelation` - Disclosures, exposures
- `confrontation` - Conflicts, showdowns

### Fantasy/Sci-fi Scenes
- `magic_ritual` - Spellcasting, ceremonies
- `space_battle` - Space combat, wars
- `time_travel` - Time jumps, temporal events
- `dimension_hop` - Portal travel, rifts
- `magical_duel` - Magical battles, confrontations

### Original Scenes
- `romantic_date` - Romantic encounters
- `battle_scene` - Combat situations
- `casual_conversation` - Informal chats

Each scene type has:
- A specific mood
- Intensity level (low/medium/high)
- Default emotions
- Scene aliases for flexible matching

## Installation

```bash
pip install emotion-aware-narrative
```

## Quick Start

```python
from emotion_engine import EmotionEngine

# Initialize the engine
engine = EmotionEngine().initialize()

# Process dialogue with scene and context
result = engine.process_dialogue_file({
    "text": "quit it",
    "scene": "romantic_date",
    "context": "flirty"
})

print(f"Detected Emotion: {result['emotion']}")
print(f"Mood Suggestion: {result['mood_suggestion']}")
```

## Usage Examples

### Basic Emotion Detection
```python
result = engine.detect_emotion("quit it")
```

### Scene-Based Detection
```python
result = engine.detect_emotion("quit it", scene="romantic_date")
```

### Context Override
```python
result = engine.detect_emotion("quit it", context="flirty")
```

### Combined Scene and Context
```python
result = engine.detect_emotion("quit it", scene="romantic_date", context="flirty")
```

## How It Works

1. **Base Emotion Detection**: Uses a pre-trained model to detect the initial emotion
2. **Scene Context**: Applies scene-specific emotional adjustments
3. **Context Override**: Applies any specified context overrides
4. **Mood Suggestion**: Generates appropriate mood cues for the final emotion

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses the emotion detection model from Hugging Face
- Inspired by the need for better emotional understanding in games 