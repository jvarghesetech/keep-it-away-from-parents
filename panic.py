import speech_recognition as sr
import subprocess
import sys

def show_desktop():
    """Sleep the display instantly — hides everything, no permissions needed"""
    subprocess.run(["pmset", "displaysleepnow"])
    print("🏠 Display off!")

DEFAULT_TRIGGERS = ["home", "hide", "clear"]

def listen_for_panic(trigger_words=None):
    if trigger_words is None:
        trigger_words = DEFAULT_TRIGGERS

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Calibrating microphone...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300

    print(f"👂 Ready! Say any of {trigger_words} to hide everything.")
    print("   Press Ctrl+C to stop.\n")

    while True:
        try:
            print("🔴 Listening...")
            with mic as source:
                audio = recognizer.listen(source, phrase_time_limit=4)

            print("⏳ Processing...")
            text = recognizer.recognize_google(audio).lower()
            print(f"✅ Heard: '{text}'")

            if any(word in text for word in trigger_words):
                show_desktop()

        except sr.UnknownValueError:
            print("❓ Couldn't understand, keep talking...")
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
        except KeyboardInterrupt:
            print("\nStopped.")
            sys.exit(0)

if __name__ == "__main__":
    words = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_TRIGGERS
    listen_for_panic(trigger_words=words)
