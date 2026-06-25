"""Voice input and output handling for Jarvis."""

import speech_recognition as sr
import pyttsx3
from typing import Optional


class VoiceHandler:
    """Handles voice input and output."""

    def __init__(self):
        """Initialize voice recognition and text-to-speech engines."""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speech rate
        self.engine.setProperty('volume', 0.9)  # Volume 0-1
        self.microphone = sr.Microphone()
        
        # Zero-latency optimizations
        self.recognizer.energy_threshold = 4000  # Dynamic energy detection
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Faster pause detection (default 0.8)
        self.recognizer.phrase_threshold = 0.3  # Phrase detection threshold

    def listen(self) -> Optional[str]:
        """Listen to voice input and convert to text with zero-latency.
        
        Returns:
            Recognized text or None if recognition failed.
        """
        try:
            with self.microphone as source:
                print("\n🎤 Listening...")
                # Faster listening with reduced timeout and phrase_time_limit
                audio = self.recognizer.listen(
                    source, 
                    timeout=5,  # Reduced from 10s
                    phrase_time_limit=10  # Max phrase length
                )
                
            print("⏳ Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            return text
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            return None
        except sr.Timeout:
            print("❌ Listening timed out. Please try again.")
            return None

    def speak(self, text: str) -> None:
        """Convert text to speech and play it.
        
        Args:
            text: The text to be spoken.
        """
        print(f"\n🤖 Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
