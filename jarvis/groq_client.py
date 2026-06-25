"""Groq API client for Jarvis."""

from groq import Groq
from typing import Optional


class GroqClient:
    """Client for interacting with Groq API."""

    def __init__(self, api_key: str):
        """Initialize Groq client.
        
        Args:
            api_key: Groq API key.
        """
        self.client = Groq(api_key=api_key)
        self.model = "mixtral-8x7b-32768"  # Latest available model
        self.conversation_history = []

    def chat(self, user_message: str) -> Optional[str]:
        """Send a message to Groq and get a response.
        
        Args:
            user_message: The user's message.
            
        Returns:
            Assistant's response or None if request failed.
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Get response from Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=1024,
                temperature=0.7,
            )
            
            # Extract and store assistant response
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            print(f"❌ Error calling Groq API: {e}")
            return None

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
