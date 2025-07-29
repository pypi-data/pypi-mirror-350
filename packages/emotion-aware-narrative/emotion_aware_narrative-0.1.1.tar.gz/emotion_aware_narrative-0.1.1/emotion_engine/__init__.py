from transformers import pipeline
from .database import EmotionDatabase
from .scene_manager import SceneManager

class EmotionEngine:
    def __init__(self):
        self._model = None
        self._emotion_to_mood = {
            "joy": "Upbeat music, bright lighting",
            "anger": "Intense music, red lighting",
            "sadness": "Somber music, dim lighting",
            "fear": "Tense music, flickering lights",
            "surprise": "Sudden sound, quick lighting change",
            "disgust": "Unsettling music, greenish lighting",
            "neutral": "Ambient music, normal lighting",
            "hope": "Uplifting music, soft golden lighting",
            "excitement": "Energetic music, vibrant lighting",
            "gratitude": "Warm music, gentle lighting",
            "anxiety": "Unsettling music, shaky camera",
            "disappointment": "Melancholic music, muted lighting",
            "guilt": "Heavy music, shadowy lighting",
            "jealousy": "Dark music, green-tinted lighting",
            "confusion": "Disjointed music, distorted lighting",
            "sympathy": "Soft music, warm lighting"
        }
        self._db = EmotionDatabase()
        self._scene_manager = SceneManager()

    def initialize(self):
        """Initialize the emotion detection model."""
        if self._model is None:
            self._model = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=1
            )
        return self

    def detect_emotion(self, text: str, context: str = None, scene: str = None) -> dict:
        """
        Detect emotion in the given text, with optional context and scene.
        
        Args:
            text (str): The text to analyze
            context (str, optional): Character mood or scene context
            scene (str, optional): The scene type
            
        Returns:
            dict: A dictionary containing:
                - emotion (str): The detected emotion
                - confidence (float): Confidence score
                - mood_suggestion (str): Suggested game mood
                - original_emotion (str): The emotion before context override
                - scene_mood (str): The mood of the scene
                - intensity (str): The intensity of the scene
        """
        if self._model is None:
            self.initialize()
            
        # Get base emotion from model
        results = self._model(text)
        result = results[0][0]
        base_emotion = result['label'].lower()
        confidence = result['score']
        
        # Process with scene and context
        dialogue = {
            "text": text,
            "scene": scene,
            "context": context,
            "detected_emotion": base_emotion
        }
        
        processed = self._scene_manager.process_dialogue(dialogue)
        
        # Get mood suggestion
        mood = self._emotion_to_mood.get(processed["emotion"], "Default mood cue")
        
        return {
            "emotion": processed["emotion"],
            "confidence": confidence,
            "mood_suggestion": mood,
            "original_emotion": processed["original_emotion"],
            "scene_mood": processed["scene_mood"],
            "intensity": processed["intensity"]
        }

    def process_dialogue_file(self, dialogue_data: dict) -> dict:
        """
        Process a complete dialogue entry with scene and context information.
        
        Args:
            dialogue_data (dict): A dictionary containing:
                - text (str): The dialogue text
                - scene (str, optional): The scene type
                - context (str, optional): The context
                - speaker (str, optional): The speaker's name
                
        Returns:
            dict: Processed emotion and mood information
        """
        return self.detect_emotion(
            text=dialogue_data["text"],
            scene=dialogue_data.get("scene"),
            context=dialogue_data.get("context")
        )

    def get_mood_suggestion(self, emotion: str) -> str:
        """
        Get mood suggestion for a specific emotion.
        
        Args:
            emotion (str): The emotion to get mood for
            
        Returns:
            str: The mood suggestion
        """
        return self._emotion_to_mood.get(emotion.lower(), "Default mood cue")

    def get_available_contexts(self) -> list:
        """
        Get all available contexts and their descriptions.
        
        Returns:
            list: List of tuples containing (context_type, context_name, description)
        """
        return self._db.get_all_contexts() 