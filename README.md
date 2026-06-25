# Jarvis - AI Voice Assistant

A Python-based voice assistant powered by Groq API that listens to voice input and responds with synthesized speech.

## Features
- 🎤 Voice input recognition
- 🤖 AI-powered responses via Groq API
- 🔊 Text-to-speech output
- 💬 Natural conversation flow
- 📝 Conversation memory

## Setup

### Prerequisites
- Python 3.9+
- Groq API key
- Microphone (for voice input)
- Speakers (for voice output)

### Installation

```bash
git clone https://github.com/SANJIT06RAJ/jarvis.git
cd jarvis
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

2. Run Jarvis:
```bash
python main.py
```

## Usage

Once running, Jarvis will:
1. Listen for your voice input
2. Send it to Groq API for processing
3. Respond with synthesized speech

Just speak naturally and Jarvis will understand!

### Commands
- Say anything to chat with Jarvis
- Say "exit", "quit", or "bye" to stop

## Architecture

- `main.py` - Entry point
- `jarvis/` - Core package
  - `voice.py` - Voice input/output handling
  - `groq_client.py` - Groq API integration
  - `assistant.py` - Main assistant logic
- `.env` - Configuration (API keys)

## Future Enhancements
- Context awareness & memory
- Multiple language support
- Custom actions/integrations
- Web interface
- Task automation
