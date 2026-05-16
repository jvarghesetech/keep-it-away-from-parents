# keep-it-away-from-parents

A voice-activated panic button for macOS. Say **"home"** and your screen goes completely black in under a second — hiding everything you had open. Move the mouse or press any key to wake it back up.

## How it works

- Listens for the word **"home"** using your microphone
- Instantly sleeps the display — hides every app, fullscreen or not
- Everything is still running when you wake the screen back up

## Install

```bash
bash install.sh
```

Or manually:

```bash
brew install portaudio
pip3 install SpeechRecognition pyaudio pyobjc
```

## Run

```bash
python3 panic.py
```

Use a custom trigger word instead of "home":

```bash
python3 panic.py hide
python3 panic.py clear
python3 panic.py safe
```

Press `Ctrl+C` to stop.

## Requirements

- macOS
- Python 3
- Microphone
