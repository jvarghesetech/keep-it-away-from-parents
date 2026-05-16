import speech_recognition as sr
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

LOG_FILE = Path.home() / ".panic_log.txt"

DEFAULT_TRIGGERS = ["home", "hide", "clear"]
WAKE_WORD = "back"
SILENT = "--silent" in sys.argv
COOLDOWN = 3  # seconds before it can trigger again
last_triggered = 0

def log(msg):
    if not SILENT:
        print(msg)

def write_log(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — {event}\n")

def show_desktop():
    """Sleep the display instantly — hides everything, no permissions needed"""
    write_log("panic triggered — display off")
    subprocess.run(["afplay", "/System/Library/Sounds/Funk.aiff"])
    subprocess.run(["pmset", "displaysleepnow"])
    log("🏠 Display off!")

def wake_display():
    """Wake the display back up"""
    write_log("wake triggered — display on")
    subprocess.run(["caffeinate", "-u", "-t", "1"])
    subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
    log("👀 Display on!")

def listen_for_panic(trigger_words=None):
    if trigger_words is None:
        trigger_words = DEFAULT_TRIGGERS

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    log("🎤 Calibrating microphone...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300

    log(f"👂 Ready! Say any of {trigger_words} to hide, '{WAKE_WORD}' to wake.")
    log("   Press Ctrl+C to stop.\n")

    while True:
        try:
            log("🔴 Listening...")
            with mic as source:
                audio = recognizer.listen(source, phrase_time_limit=4)

            text = recognizer.recognize_google(audio).lower()
            log(f"✅ Heard: '{text}'")

            if any(word in text for word in trigger_words):
                if time.time() - last_triggered >= COOLDOWN:
                    last_triggered = time.time()
                    show_desktop()
                else:
                    log("⏳ Cooldown active, wait a moment...")
            elif WAKE_WORD in text:
                wake_display()

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            log(f"❌ Speech recognition error: {e}")
        except KeyboardInterrupt:
            log("\nStopped.")
            sys.exit(0)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--silent"]
    words = args if args else DEFAULT_TRIGGERS
    listen_for_panic(trigger_words=words)
