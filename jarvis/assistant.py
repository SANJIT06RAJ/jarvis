"""Main assistant logic for Jarvis."""

from jarvis.voice import VoiceHandler
from jarvis.groq_client import GroqClient
from typing import Optional


class Jarvis:
    """Main Jarvis assistant."""

    def __init__(self, groq_api_key: str):
        """Initialize Jarvis assistant.
        
        Args:
            groq_api_key: Groq API key.
        """
        self.voice = VoiceHandler()
        self.groq = GroqClient(groq_api_key)
        self.running = False

    def process_voice_input(self) -> Optional[str]:
        """Get voice input from user.
        
        Returns:
            Recognized text or None if failed.
        """
        return self.voice.listen()

    def get_response(self, user_input: str) -> Optional[str]:
        """Get AI response from Groq.
        
        Args:
            user_input: User's message.
            
        Returns:
            AI response or None if failed.
        """
        return self.groq.chat(user_input)

    def respond_with_voice(self, response: str) -> None:
        """Respond with synthesized speech.
        
        Args:
            response: The response text.
        """
        self.voice.speak(response)

    def run(self) -> None:
        """Main loop for Jarvis."""
        self.running = True
        print("\n" + "="*50)
        print("🤖 Jarvis - AI Voice Assistant")
        print("="*50)
        print("Say 'exit' or 'quit' to stop\n")

        while self.running:
            try:
                # Get voice input
                user_input = self.process_voice_input()
                
                if user_input is None:
                    continue

                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self.voice.speak("Goodbye! See you later.")
                    self.running = False
                    break

                # Get AI response
                response = self.get_response(user_input)
                
                if response:
                    self.respond_with_voice(response)
                else:
                    self.voice.speak("Sorry, I encountered an error. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down Jarvis...")
                self.running = False
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                self.voice.speak("An error occurred. Please try again.")

    def clear_memory(self) -> None:
        """Clear conversation history."""
        self.groq.clear_history()
        print("🧠 Memory cleared")
