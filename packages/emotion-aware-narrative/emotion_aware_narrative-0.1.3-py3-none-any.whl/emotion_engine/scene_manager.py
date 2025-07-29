from difflib import get_close_matches
from typing import Dict, List, Optional, Union

class SceneManager:
    def __init__(self):
        # Scene definitions with their properties
        self.scene_definitions = {
            # Original scenes
            "romantic_date": {
                "mood": "romantic",
                "intensity": "high",
                "default_emotions": ["joy", "excitement", "hope"],
                "aliases": ["date", "romance", "love_scene"]
            },
            "battle_scene": {
                "mood": "tense",
                "intensity": "high",
                "default_emotions": ["anger", "fear", "excitement"],
                "aliases": ["battle", "combat", "fight"]
            },
            "casual_conversation": {
                "mood": "relaxed",
                "intensity": "low",
                "default_emotions": ["neutral", "joy", "sympathy"],
                "aliases": ["casual", "chat", "talk"]
            },

            # Social Scenes
            "formal_meeting": {
                "mood": "professional",
                "intensity": "medium",
                "default_emotions": ["neutral", "anxiety", "confidence"],
                "aliases": ["meeting", "business", "conference"]
            },
            "party": {
                "mood": "celebratory",
                "intensity": "high",
                "default_emotions": ["joy", "excitement", "gratitude"],
                "aliases": ["celebration", "festival", "gathering"]
            },
            "family_gathering": {
                "mood": "warm",
                "intensity": "medium",
                "default_emotions": ["joy", "gratitude", "sympathy"],
                "aliases": ["family", "reunion", "home"]
            },
            "interview": {
                "mood": "formal",
                "intensity": "high",
                "default_emotions": ["anxiety", "confidence", "neutral"],
                "aliases": ["job_interview", "audition", "evaluation"]
            },
            "negotiation": {
                "mood": "tense",
                "intensity": "high",
                "default_emotions": ["anxiety", "confidence", "anger"],
                "aliases": ["bargaining", "deal", "discussion"]
            },

            # Action Scenes
            "chase_scene": {
                "mood": "intense",
                "intensity": "high",
                "default_emotions": ["fear", "excitement", "anxiety"],
                "aliases": ["chase", "pursuit", "escape"]
            },
            "stealth_mission": {
                "mood": "suspenseful",
                "intensity": "high",
                "default_emotions": ["fear", "anxiety", "excitement"],
                "aliases": ["stealth", "infiltration", "sneaking"]
            },
            "training_session": {
                "mood": "focused",
                "intensity": "medium",
                "default_emotions": ["determination", "frustration", "joy"],
                "aliases": ["training", "practice", "learning"]
            },
            "competition": {
                "mood": "competitive",
                "intensity": "high",
                "default_emotions": ["excitement", "anxiety", "determination"],
                "aliases": ["contest", "match", "tournament"]
            },
            "rescue_mission": {
                "mood": "urgent",
                "intensity": "high",
                "default_emotions": ["fear", "hope", "determination"],
                "aliases": ["rescue", "save", "recovery"]
            },

            # Emotional Scenes
            "funeral": {
                "mood": "somber",
                "intensity": "high",
                "default_emotions": ["sadness", "gratitude", "sympathy"],
                "aliases": ["memorial", "burial", "farewell"]
            },
            "wedding": {
                "mood": "joyous",
                "intensity": "high",
                "default_emotions": ["joy", "gratitude", "hope"],
                "aliases": ["marriage", "ceremony", "celebration"]
            },
            "graduation": {
                "mood": "proud",
                "intensity": "high",
                "default_emotions": ["joy", "pride", "hope"],
                "aliases": ["commencement", "ceremony", "achievement"]
            },
            "reunion": {
                "mood": "warm",
                "intensity": "medium",
                "default_emotions": ["joy", "gratitude", "sympathy"],
                "aliases": ["meeting", "gathering", "return"]
            },
            "farewell": {
                "mood": "bittersweet",
                "intensity": "high",
                "default_emotions": ["sadness", "gratitude", "hope"],
                "aliases": ["goodbye", "parting", "departure"]
            },

            # Mystery/Thriller Scenes
            "investigation": {
                "mood": "suspenseful",
                "intensity": "medium",
                "default_emotions": ["curiosity", "anxiety", "determination"],
                "aliases": ["detective", "search", "inquiry"]
            },
            "interrogation": {
                "mood": "tense",
                "intensity": "high",
                "default_emotions": ["fear", "anger", "anxiety"],
                "aliases": ["questioning", "interview", "examination"]
            },
            "discovery": {
                "mood": "awe",
                "intensity": "high",
                "default_emotions": ["surprise", "wonder", "excitement"],
                "aliases": ["finding", "revelation", "unveiling"]
            },
            "revelation": {
                "mood": "dramatic",
                "intensity": "high",
                "default_emotions": ["surprise", "shock", "confusion"],
                "aliases": ["disclosure", "exposure", "unveiling"]
            },
            "confrontation": {
                "mood": "tense",
                "intensity": "high",
                "default_emotions": ["anger", "fear", "determination"],
                "aliases": ["conflict", "showdown", "faceoff"]
            },

            # Fantasy/Sci-fi Scenes
            "magic_ritual": {
                "mood": "mysterious",
                "intensity": "high",
                "default_emotions": ["awe", "fear", "excitement"],
                "aliases": ["ritual", "ceremony", "spellcasting"]
            },
            "space_battle": {
                "mood": "epic",
                "intensity": "high",
                "default_emotions": ["fear", "excitement", "determination"],
                "aliases": ["battle", "combat", "war"]
            },
            "time_travel": {
                "mood": "mysterious",
                "intensity": "high",
                "default_emotions": ["wonder", "fear", "excitement"],
                "aliases": ["time_jump", "temporal", "chrono"]
            },
            "dimension_hop": {
                "mood": "surreal",
                "intensity": "high",
                "default_emotions": ["wonder", "fear", "confusion"],
                "aliases": ["portal", "rift", "gateway"]
            },
            "magical_duel": {
                "mood": "intense",
                "intensity": "high",
                "default_emotions": ["determination", "fear", "excitement"],
                "aliases": ["duel", "battle", "confrontation"]
            }
        }

        # Context definitions with their emotion overrides
        self.context_definitions = {
            "flirty": {
                "emotion_override": {
                    "anger": "joy",
                    "neutral": "excitement",
                    "fear": "excitement"
                },
                "priority": "medium"
            },
            "angry": {
                "emotion_override": {
                    "joy": "anger",
                    "neutral": "anger"
                },
                "priority": "high"
            }
        }

        # Default behaviors
        self.default_scene = "casual_conversation"
        self.default_context = None

    def get_scene_context(self, scene_name: str) -> Dict:
        """Get scene context with fuzzy matching for scene names"""
        # Try exact match first
        if scene_name in self.scene_definitions:
            return self.scene_definitions[scene_name]
        
        # Try fuzzy matching
        for scene, definition in self.scene_definitions.items():
            aliases = definition.get("aliases", [])
            if not aliases:
                continue
                
            if scene_name in aliases:
                return definition
            
            # Check if scene_name is similar to any alias
            matches = get_close_matches(scene_name, aliases, n=1, cutoff=0.8)
            if matches:
                return definition
        
        # Return default scene if no match found
        return self.scene_definitions[self.default_scene]

    def get_context_override(self, context: Optional[str], base_emotion: str) -> str:
        """Get emotion override based on context"""
        if not context or context not in self.context_definitions:
            return base_emotion
        
        context_def = self.context_definitions[context]
        return context_def["emotion_override"].get(base_emotion, base_emotion)

    def process_dialogue(self, dialogue: Dict) -> Dict:
        """Process dialogue with scene and context"""
        # Get scene context
        scene = dialogue.get("scene", self.default_scene)
        scene_context = self.get_scene_context(scene)
        
        # Get context override
        context = dialogue.get("context", self.default_context)
        
        # Get base emotion (this will come from the emotion detection model)
        base_emotion = dialogue.get("detected_emotion", "neutral")
        
        # Apply context override
        final_emotion = self.get_context_override(context, base_emotion)
        
        return {
            "emotion": final_emotion,
            "scene_mood": scene_context["mood"],
            "intensity": scene_context["intensity"],
            "original_emotion": base_emotion
        }

    def add_scene(self, scene_name: str, properties: Dict) -> None:
        """Add a new scene definition"""
        self.scene_definitions[scene_name] = properties

    def add_context(self, context_name: str, properties: Dict) -> None:
        """Add a new context definition"""
        self.context_definitions[context_name] = properties 