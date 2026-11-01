"""Start the local server with the active Python environment."""
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = "http://127.0.0.1:8773/"

def ready():
    try:
        with urllib.request.urlopen(URL, timeout=1) as response:
            return "蟲族對局筆記" in response.read().decode("utf-8")
    except (OSError, UnicodeError):
        return False

if __name__ == "__main__":
    if not ready():
        with (ROOT / "server.log").open("a") as log:
            child = subprocess.Popen(
                [sys.executable, str(ROOT / "app.py")], cwd=ROOT,
                stdout=log, stderr=log, start_new_session=True,
            )
        for _ in range(30):
            if ready():
                break
            if child.poll() is not None:
                break
            time.sleep(0.2)
    if not ready():
        raise SystemExit("啟動失敗，請查看 server.log，並確認 8773 未被其他程式占用。")
    webbrowser.open(URL)
