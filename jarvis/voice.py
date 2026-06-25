"""Voice input and output handling for Jarvis."""

import speech_recognition as sr
import pyttsx3
import threading
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
        
        # Interruption support
        self.is_speaking = False
        self.interrupt_flag = False

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
        """Convert text to speech and play it with interruption support.
        
        Args:
            text: The text to be spoken.
        """
        print(f"\n🤖 Jarvis: {text}")
        self.is_speaking = True
        self.interrupt_flag = False
        
        # Start speaking in a separate thread to allow interruption detection
        speak_thread = threading.Thread(target=self._speak_with_interrupt, args=(text,))
        speak_thread.daemon = True
        speak_thread.start()
        
        # Listen for interruption while speaking
        self._listen_for_interruption()
        
        # Wait for speech to finish
        speak_thread.join(timeout=30)
        self.is_speaking = False

    def _speak_with_interrupt(self, text: str) -> None:
        """Internal method to speak text and check for interruption.
        
        Args:
            text: The text to be spoken.
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def _listen_for_interruption(self) -> None:
        """Listen for interruption commands while Jarvis is speaking."""
        interrupt_thread = threading.Thread(target=self._interrupt_listener)
        interrupt_thread.daemon = True
        interrupt_thread.start()

    def _interrupt_listener(self) -> None:
        """Background thread that listens for interruption keywords."""
        try:
            with self.microphone as source:
                # Listen with very short timeout while speaking
                audio = self.recognizer.listen(
                    source,
                    timeout=0.5,
                    phrase_time_limit=2
                )
            
            text = self.recognizer.recognize_google(audio).lower()
            
            # Check for interruption keywords
            if any(keyword in text for keyword in ["stop", "wait", "quiet", "pause"]):
                print("\n⏹️  Interruption detected!")
                self.interrupt_flag = True
                self.engine.stop()
                
        except (sr.UnknownValueError, sr.RequestError, sr.Timeout):
            # No speech or error - continue speaking
            pass
        except Exception:
            # Silently handle any other exceptions
            pass

    def was_interrupted(self) -> bool:
        """Check if speech was interrupted.
        
        Returns:
            True if speech was interrupted, False otherwise.
        """
        return self.interrupt_flag
