import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Optional

class GeminiClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        print("Initializing Gemini client...")
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        self.chat = self.model.start_chat(history=[])
        print("Gemini client initialized successfully!")

    def generate_response(self, message: str) -> Optional[str]:
        """Generate a response using Gemini API"""
        try:
            print(f"Sending message to Gemini: {message[:100]}...")  # Print first 100 chars
            response = self.chat.send_message(message)
            print(f"Received response from Gemini: {response.text[:100]}...")  # Print first 100 chars
            return response.text
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            return None

    def reset_conversation(self):
        """Reset the conversation history"""
        print("Resetting Gemini conversation...")
        self.chat = self.model.start_chat(history=[])
        print("Gemini conversation reset complete!") 