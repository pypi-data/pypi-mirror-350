# Jarvis OS

**Jarvis OS** is a local, privacy-focused voice assistant designed to run entirely on your machine. It integrates offline speech recognition, AI-powered natural language responses, and system-level command execution.

## Features

- Offline speech recognition with [Vosk](https://alphacephei.com/vosk/)
- Natural voice synthesis using [Yapper TTS](https://github.com/n1teshy/yapper-tts)
- Streaming responses from a local or remote LLM (e.g., LM Studio)
- Terminal-based interface with dynamic boot and loading screens
- Executes system commands: open applications, perform searches, shut down, and more

## Installation

```bash
pip install jarvis-os

## Example commands:

"Jarvis open vscode"

"Jarvis google how to bake sourdough"

"Jarvis shutdown"

"Jarvis explain quantum entanglement"

## Configuration
Python version 3.8 or higher is required

Ensure microphone input is enabled on your system

To use an AI backend (like LM Studio), modify the API endpoint in main.py

## License
This project is licensed under the Apache License 2.0.

## Author
Arvin Adeli