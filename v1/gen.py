"""Generate images with gpt-image-2 via an OpenAI-compatible relay (credentials from environment variables).

Usage: python gen.py <out.png> <prompt_file> [ref_image ...] [--size 1536x1024]
With refs -> /images/edits (multipart); without -> /images/generations.
"""

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
import base64, io, re, sys, time
from pathlib import Path

import requests
from PIL import Image

BASE = _os.environ.get("SHINKAI_IMAGE_BASE_URL", "").rstrip("/")
KEY = _os.environ.get("SHINKAI_IMAGE_API_KEY", "").rstrip("/")
KEY = re.search(r'experimental_bearer_token\s*=\s*"([^"]+)"', sec).group(1)
MODEL = "gpt-image-2"


def ref_bytes(path, max_side=1536):
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


def save(data, out):
    item = data["data"][0]
    if item.get("b64_json"):
        raw = base64.b64decode(item["b64_json"])
    else:
        raw = requests.get(item["url"], timeout=300).content
    Path(out).write_bytes(raw)


def generate(out, prompt, refs, size="1536x1024", retries=3):
    h = {"Authorization": f"Bearer {KEY}"}
    for attempt in range(1, retries + 1):
        try:
            if refs:
                files = [("image[]", (f"ref{i}.png", ref_bytes(r), "image/png")) for i, r in enumerate(refs)]
                resp = requests.post(f"{BASE}/images/edits", headers=h, files=files,
                                     data={"model": MODEL, "prompt": prompt, "size": size, "quality": "high", "n": "1"},
                                     timeout=900)
            else:
                resp = requests.post(f"{BASE}/images/generations", headers=h,
                                     json={"model": MODEL, "prompt": prompt, "size": size, "quality": "high", "n": 1},
                                     timeout=900)
            if resp.status_code != 200:
                print(f"[{attempt}] HTTP {resp.status_code}: {resp.text[:400]}", flush=True)
                time.sleep(8)
                continue
            save(resp.json(), out)
            print(f"OK {out}", flush=True)
            return True
        except Exception as e:
            print(f"[{attempt}] error: {e}", flush=True)
            time.sleep(8)
    return False


if __name__ == "__main__":
    args = sys.argv[1:]
    size = "1536x1024"
    if "--size" in args:
        i = args.index("--size")
        size = args[i + 1]
        del args[i:i + 2]
    out, prompt_file, *refs = args
    ok = generate(out, Path(prompt_file).read_text(encoding="utf-8"), refs, size)
    sys.exit(0 if ok else 1)
