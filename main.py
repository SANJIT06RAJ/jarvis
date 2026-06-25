"""Entry point for Jarvis."""

import os
from dotenv import load_dotenv
from jarvis.assistant import Jarvis


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    # Get Groq API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file")
        print("Please create a .env file with your Groq API key.")
        return
    
    # Initialize and run Jarvis
    jarvis = Jarvis(groq_api_key)
    jarvis.run()


if __name__ == "__main__":
    main()
