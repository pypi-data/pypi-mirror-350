import sqlite3
from pathlib import Path

class EmotionDatabase:
    def __init__(self, db_path="emotion_contexts.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def connect(self):
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        """Create the database tables if they don't exist"""
        self.connect()
        
        # Create contexts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contexts (
                id INTEGER PRIMARY KEY,
                context_type TEXT NOT NULL,
                context_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(context_type, context_name)
            )
        ''')

        # Create emotion mappings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotion_mappings (
                id INTEGER PRIMARY KEY,
                context_id INTEGER,
                original_emotion TEXT NOT NULL,
                adjusted_emotion TEXT NOT NULL,
                confidence_adjustment FLOAT DEFAULT 1.0,
                FOREIGN KEY (context_id) REFERENCES contexts(id),
                UNIQUE(context_id, original_emotion)
            )
        ''')

        # Insert default contexts if they don't exist
        self._insert_default_contexts()
        
        self.conn.commit()
        self.close()

    def _insert_default_contexts(self):
        """Insert default contexts and their emotion mappings"""
        # Basic Personality Contexts
        personality_contexts = [
            ('personality', 'nonchalant', 'Character is laid-back and calm'),
            ('personality', 'dramatic', 'Character is expressive and theatrical'),
            ('personality', 'calm', 'Character is composed and peaceful'),
            ('personality', 'sarcastic', 'Character is ironic and mocking'),
            ('personality', 'professional', 'Character is formal and composed'),
            ('personality', 'childlike', 'Character is innocent and playful'),
            ('personality', 'flirty', 'Character is playful and romantic')
        ]

        # Emotional State Contexts
        emotional_contexts = [
            ('emotional', 'tired', 'Character is exhausted and sleepy'),
            ('emotional', 'energetic', 'Character is excited and lively'),
            ('emotional', 'nervous', 'Character is anxious and worried'),
            ('emotional', 'confident', 'Character is assured and self-assured'),
            ('emotional', 'mysterious', 'Character is enigmatic and secretive'),
            ('emotional', 'angry', 'Character is irritated and frustrated')
        ]

        # Character Role Contexts
        role_contexts = [
            ('role', 'heroic', 'Character is brave and noble'),
            ('role', 'villainous', 'Character is evil and malicious'),
            ('role', 'mentor', 'Character is wise and guiding'),
            ('role', 'sidekick', 'Character is loyal and supportive'),
            ('role', 'rival', 'Character is competitive and challenging'),
            ('role', 'neutral', 'Character is balanced and impartial')
        ]

        # Situational Contexts
        situation_contexts = [
            ('situation', 'battle', 'Combat or fighting scenario'),
            ('situation', 'stealth', 'Sneaky or quiet scenario'),
            ('situation', 'social', 'Conversational and friendly scenario'),
            ('situation', 'tense', 'Suspenseful and dramatic scenario'),
            ('situation', 'relaxed', 'Casual and informal scenario'),
            ('situation', 'formal', 'Official and ceremonial scenario'),
            ('situation', 'romantic', 'Romantic or intimate scenario')
        ]

        # Relationship Contexts
        relationship_contexts = [
            ('relationship', 'friendly', 'Warm and kind interaction'),
            ('relationship', 'hostile', 'Unfriendly and aggressive interaction'),
            ('relationship', 'romantic', 'Loving and affectionate interaction'),
            ('relationship', 'familial', 'Family-oriented and caring interaction'),
            ('relationship', 'professional', 'Business-like and formal interaction'),
            ('relationship', 'stranger', 'Distant and unfamiliar interaction')
        ]

        # Insert all contexts
        all_contexts = (personality_contexts + emotional_contexts + 
                       role_contexts + situation_contexts + relationship_contexts)
        
        for context_type, context_name, description in all_contexts:
            try:
                self.cursor.execute('''
                    INSERT INTO contexts (context_type, context_name, description)
                    VALUES (?, ?, ?)
                ''', (context_type, context_name, description))
            except sqlite3.IntegrityError:
                # Context already exists, skip
                pass

        # Insert default emotion mappings for some contexts
        self._insert_default_mappings()

    def _insert_default_mappings(self):
        """Insert default emotion mappings for contexts"""
        # Get context IDs
        self.cursor.execute("SELECT id, context_name FROM contexts")
        contexts = {name: id for id, name in self.cursor.fetchall()}

        # Default mappings for nonchalant context
        nonchalant_mappings = [
            ('anger', 'neutral', 0.8),
            ('fear', 'neutral', 0.8),
            ('disgust', 'neutral', 0.8),
            ('surprise', 'neutral', 0.8),
            ('joy', 'neutral', 0.8),
            ('sadness', 'neutral', 0.8)
        ]

        # Default mappings for dramatic context
        dramatic_mappings = [
            ('neutral', 'surprise', 0.9),
            ('joy', 'surprise', 0.9),
            ('sadness', 'surprise', 0.9),
            ('anger', 'surprise', 0.9)
        ]

        # Default mappings for battle context
        battle_mappings = [
            ('neutral', 'anger', 0.7),
            ('joy', 'anger', 0.7),
            ('sadness', 'anger', 0.7)
        ]

        # Default mappings for flirty context
        flirty_mappings = [
            ('anger', 'joy', 0.8),
            ('neutral', 'joy', 0.8),
            ('fear', 'excitement', 0.8),
            ('sadness', 'hope', 0.8)
        ]

        # Insert mappings
        mappings = {
            'nonchalant': nonchalant_mappings,
            'dramatic': dramatic_mappings,
            'battle': battle_mappings,
            'flirty': flirty_mappings
        }

        for context_name, context_mappings in mappings.items():
            if context_name in contexts:
                for orig_emotion, adj_emotion, conf in context_mappings:
                    try:
                        self.cursor.execute('''
                            INSERT INTO emotion_mappings 
                            (context_id, original_emotion, adjusted_emotion, confidence_adjustment)
                            VALUES (?, ?, ?, ?)
                        ''', (contexts[context_name], orig_emotion, adj_emotion, conf))
                    except sqlite3.IntegrityError:
                        # Mapping already exists, skip
                        pass

    def get_emotion_mapping(self, context_name, original_emotion):
        """Get the adjusted emotion and confidence for a given context and emotion"""
        self.connect()
        self.cursor.execute('''
            SELECT em.adjusted_emotion, em.confidence_adjustment
            FROM emotion_mappings em
            JOIN contexts c ON em.context_id = c.id
            WHERE c.context_name = ? AND em.original_emotion = ?
        ''', (context_name, original_emotion))
        
        result = self.cursor.fetchone()
        self.close()
        
        if result:
            return {
                'adjusted_emotion': result[0],
                'confidence_adjustment': result[1]
            }
        return None

    def get_all_contexts(self):
        """Get all available contexts"""
        self.connect()
        self.cursor.execute('SELECT context_type, context_name, description FROM contexts')
        contexts = self.cursor.fetchall()
        self.close()
        return contexts 