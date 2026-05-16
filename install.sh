#!/bin/bash
echo "Installing dependencies..."
brew install portaudio
pip3 install SpeechRecognition pyaudio pyobjc
echo "Done! Run with: python3 panic.py"
