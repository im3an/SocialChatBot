from .gemini_client import GeminiClient
import os
from dotenv import load_dotenv
from typing import Optional, List, Tuple

class Chatbot:
    def __init__(self):
        load_dotenv()
        self.personality_file = os.getenv('PERSONALITY_FILE_PATH')
        self.gemini_client = GeminiClient()
        self.conversation_history: List[Tuple[str, str]] = []
        self.personality_prompt = self._load_personality()
        self.error_count = 0
        self.max_errors = 3

    def _load_personality(self) -> str:
        """Load the personality prompt from the file"""
        try:
            with open(self.personality_file, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error loading personality file: {e}")
            return ""

    def _is_error_message(self, message: str) -> bool:
        """Check if a message is an error message"""
        error_phrases = [
            "Error generating response",
            "Failed to chat",
            "Sorry, I'm having trouble"
        ]
        return any(phrase in message for phrase in error_phrases)

    def respond_to_message(self, user_message: str) -> Optional[str]:
        """Generate a response to the user's message"""
        if self._is_error_message(user_message):
            self.error_count += 1
            if self.error_count >= self.max_errors:
                print("Too many consecutive errors, resetting conversation...")
                self.conversation_history.clear()
                self.gemini_client.reset_conversation()
                self.error_count = 0
                return None
            return None

        if user_message.upper() == "STOP TEXTING ME":
            return "Okay, I understand. Bye."
        
        # Reset error count on successful message
        self.error_count = 0
        
        # Create context using the personality file content
        context = f"""
        You are Riley, a friendly and engaging chatbot. Use this personality definition:
        {self.personality_prompt}

        Previous conversation context:
        {' | '.join([f"User: {msg}" for sender, msg in self.conversation_history[-3:] if sender == 'user'])}

        Respond as Riley to this message: {user_message}
        
        Keep your response natural, friendly, and concise. Don't mention that you're an AI or following instructions.
        """
        
        self.conversation_history.append(("user", user_message))
        response = self.gemini_client.generate_response(context)
        
        if response and not self._is_error_message(response):
            self.conversation_history.append(("bot", response))
            return response
        return None

    def get_conversation_history(self) -> List[Tuple[str, str]]:
        return self.conversation_history