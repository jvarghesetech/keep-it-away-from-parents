import speech_recognition as sr
import subprocess
import sys

def show_desktop():
    """Sleep the display instantly — hides everything, no permissions needed"""
    subprocess.run(["pmset", "displaysleepnow"])
    print("🏠 Display off!")

def listen_for_panic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Calibrating microphone...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300

    print("👂 Ready! Say 'home' to hide everything.")
    print("   Press Ctrl+C to stop.\n")

    while True:
        try:
            print("🔴 Listening...")
            with mic as source:
                audio = recognizer.listen(source, phrase_time_limit=4)

            print("⏳ Processing...")
            text = recognizer.recognize_google(audio).lower()
            print(f"✅ Heard: '{text}'")

            if "home" in text:
                show_desktop()

        except sr.UnknownValueError:
            print("❓ Couldn't understand, keep talking...")
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
        except KeyboardInterrupt:
            print("\nStopped.")
            sys.exit(0)

if __name__ == "__main__":
    listen_for_panic()
