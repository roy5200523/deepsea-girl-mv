# --- open-source portability (added for the public release) ---
import os as _os
from pathlib import Path as _Path


def _repo_root():
    for _p in _Path(__file__).resolve().parents:
        if (_p / "README.md").exists():
            return _p
    return _Path(__file__).resolve().parent


REPO_ROOT = _repo_root()
DESKTOP = _Path(_os.environ.get("SHINKAI_DESKTOP", _Path.home() / "Desktop"))
# --- end ---

import base64, re, sys, requests
from pathlib import Path

BASE = _os.environ.get("SHINKAI_GPT_BASE_URL", "").rstrip("/")
key = _os.environ.get("SHINKAI_GPT_API_KEY", "")
model = sys.argv[1]
out = sys.argv[2]
audio = base64.b64encode(Path(str(REPO_ROOT / "ref" / "song.mp3")).read_bytes()).decode()
lyrics = Path(str(DESKTOP / "Claude" / "深海少女" / "歌曲和歌词" / "歌词.txt")).read_text(encoding="utf-8")

prompt = ("This is the Vocaloid song 深海少女 (about 3:37 long). Listen carefully and give, for every lyric line below, "
          "the exact time in the audio when the vocal for that line STARTS and ENDS, in seconds with one decimal. "
          "Some lines may be sung in a different order or repeated; follow the audio. Also list instrumental sections (intro, interlude, outro) with times. "
          "Output one line per entry in the format: start|end|text . No other commentary.\n\nLyrics:\n" + lyrics)

body = {"model": model, "messages": [{"role": "user", "content": [
    {"type": "text", "text": prompt},
    {"type": "input_audio", "input_audio": {"data": audio, "format": "mp3"}}]}]}
r = requests.post(BASE + "/chat/completions", headers={"Authorization": "Bearer " + key}, json=body, timeout=900)
print(r.status_code)
txt = r.text
try:
    txt = r.json()["choices"][0]["message"]["content"]
except Exception:
    pass
Path(out).write_text(txt, encoding="utf-8")
