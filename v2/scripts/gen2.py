"""Image generation via an OpenAI-compatible image relay (creds.IMAGE). Only gpt-image-2.6-sunburst / gpt-image-2 are allowed.

Usage: python gen2.py <out.png> <prompt_file> [ref ...] [--size 1536x1024] [--model gpt-image-2] [--bg transparent]
With refs -> /images/edits (multipart); without -> /images/generations.
"""
import base64, io, re, sys, time
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import creds

BASE, KEY = creds.IMAGE


def ref_bytes(path, max_side=1536):
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


def save(data, out):
    item = data["data"][0]
    raw = base64.b64decode(item["b64_json"]) if item.get("b64_json") else requests.get(item["url"], timeout=300).content
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_bytes(raw)


def data_url(path):
    return "data:image/png;base64," + base64.b64encode(ref_bytes(path)).decode()


# the relay sometimes rejects multipart edits; then send refs as data URLs in a JSON body
JSON_EDITS = [False]


def generate(out, prompt, refs=(), size="1536x1024", model="gpt-image-2.6-sunburst", bg=None, retries=4, log=print):
    creds.guard(model, creds.IMAGE_MODELS)
    h = {"Authorization": f"Bearer {KEY}"}
    extra = {"background": bg} if bg else {}
    for attempt in range(1, retries + 1):
        try:
            if refs and JSON_EDITS[0]:
                resp = requests.post(f"{BASE}/images/edits", headers=h, timeout=900,
                                     json={"model": model, "prompt": prompt, "size": size, "quality": "high", "n": 1,
                                           "images": [{"image_url": data_url(r)} for r in refs], **extra})
            elif refs:
                files = [("image[]", (f"ref{i}.png", ref_bytes(r), "image/png")) for i, r in enumerate(refs)]
                resp = requests.post(f"{BASE}/images/edits", headers=h, files=files, timeout=900,
                                     data={"model": model, "prompt": prompt, "size": size, "quality": "high", "n": "1",
                                           **extra})
            else:
                resp = requests.post(f"{BASE}/images/generations", headers=h, timeout=900,
                                     json={"model": model, "prompt": prompt, "size": size, "quality": "high", "n": 1,
                                           **extra})
            if resp.status_code != 200:
                log(f"[{attempt}] {Path(out).name} HTTP {resp.status_code}: {resp.text[:300]}")
                if "multipart/form-data" in resp.text and not JSON_EDITS[0]:
                    JSON_EDITS[0] = True
                    continue
                time.sleep(10 * attempt)
                continue
            save(resp.json(), out)
            log(f"OK {out}")
            return True
        except Exception as e:
            log(f"[{attempt}] {Path(out).name} error: {e}")
            time.sleep(10 * attempt)
    return False


if __name__ == "__main__":
    args = sys.argv[1:]
    opts = {"--size": "1536x1024", "--model": "gpt-image-2", "--bg": None}
    for k in list(opts):
        if k in args:
            i = args.index(k)
            opts[k] = args[i + 1]
            del args[i:i + 2]
    out, prompt_file, *refs = args
    ok = generate(out, Path(prompt_file).read_text(encoding="utf-8"), refs, opts["--size"], opts["--model"], opts["--bg"])
    sys.exit(0 if ok else 1)
