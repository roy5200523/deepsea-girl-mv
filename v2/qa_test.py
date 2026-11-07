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

import base64, io, re, sys, json, requests
from pathlib import Path
from PIL import Image
BASE = _os.environ.get("SHINKAI_GPT_BASE_URL", "").rstrip("/")
key = _os.environ.get("SHINKAI_GPT_API_KEY", "")
im = Image.open(sys.argv[1]).convert("RGB"); im.thumbnail((1600,1600)); b=io.BytesIO(); im.save(b,"JPEG",quality=92)
url = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
prompt = ("You are a strict QA checker for anime illustrations. Count carefully. For EACH character in the image report: "
 "number of visible arms, number of visible hands, and whether every hand is attached to an arm of that character. "
 "Flag extra/missing/fused/malformed hands or fingers, extra limbs, broken anatomy, distorted faces/eyes, and any text/letters. "
 "Reply JSON: {\"characters\":[{\"who\":...,\"arms\":n,\"hands\":n,\"notes\":...}],\"defects\":[...],\"verdict\":\"PASS|FAIL\"}")
body = {"model": "gpt-6.1-sol", "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": url}}]}]}
r = requests.post(BASE + "/chat/completions", headers={"Authorization": "Bearer " + key}, json=body, timeout=600)
print(r.status_code)
try: print(r.json()["choices"][0]["message"]["content"])
except Exception: print(r.text[:800])
