"""
Sets up panic.py to run automatically when your Mac starts.
Run once: python3 autostart.py
"""

import os
import subprocess
from pathlib import Path

PLIST_NAME = "com.keepitaway.panic"
PLIST_PATH = Path.home() / "Library/LaunchAgents" / f"{PLIST_NAME}.plist"
SCRIPT_PATH = Path(__file__).parent.resolve() / "panic.py"

PLIST_CONTENT = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{SCRIPT_PATH}</string>
        <string>--silent</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""

def install():
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(PLIST_CONTENT)
    subprocess.run(["launchctl", "load", str(PLIST_PATH)])
    print(f"✅ Auto-start enabled! panic.py will run silently on every login.")
    print(f"   To remove: python3 autostart.py --remove")

def remove():
    if PLIST_PATH.exists():
        subprocess.run(["launchctl", "unload", str(PLIST_PATH)])
        PLIST_PATH.unlink()
        print("✅ Auto-start removed.")
    else:
        print("❌ Auto-start not installed.")

if __name__ == "__main__":
    import sys
    if "--remove" in sys.argv:
        remove()
    else:
        install()
