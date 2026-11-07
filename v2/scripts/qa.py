"""Anatomy QA for storyboard images using a vision model (two independent passes).

Usage: python qa.py <out.jsonl> <img> [img ...] [--expect "whale girl:2 arms; orange girl:2 arms"]
Each image gets one JSON line: {file, verdict, defects, characters}. FAIL if either pass fails.
"""
import base64, io, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import creds

ROUTE = {"gpt-6.1-sol": (creds.GPT, creds.GPT_MODELS), "gemini-3.8-flash": (creds.GEMINI, creds.GEMINI_MODELS)}

PROMPT = (
    "You are a strict QA checker for hand-drawn anime storyboard frames. Look very carefully and COUNT. "
    "For EACH character report the number of visible arms and visible hands, and trace every hand back to the "
    "shoulder it belongs to. Flag: extra or missing arms/hands, a hand not connected to any arm, fused or "
    "malformed hands, wrong finger count where fingers are clearly visible, extra legs/tails, broken or twisted "
    "limbs, melted or distorted faces/eyes, two characters merged together, and any visible text, letters or "
    "watermarks. ALSO check whole-body pose coherence for each character: decide which way the chest faces and "
    "which way the hips/pelvis face (toward viewer, away, up, down, sideways) and FAIL if they disagree by more "
    "than about 90 degrees (e.g. upper body lying face-down while the lower body lies face-up), if the legs do not "
    "attach to the hips naturally, if knees or elbows bend the wrong way, or if the spine is impossibly twisted. "
    "Report chest and hip facing in notes. Rough sketchy pencil lines and flat misaligned colours are intended style, "
    "NOT defects; small zigzag or squiggle highlight scribbles on hair, hats or clothes are intended style, NOT text. "
    "By design the blue-haired whale girl has BOTH human legs AND a whale tail growing from behind her waist; that is "
    "correct, not an extra limb. "
    "Hands hidden behind the body or out of frame are fine; only count what is visible. {expect}"
    "Reply with JSON only: {{\"characters\":[{{\"who\":str,\"arms\":int,\"hands\":int,\"notes\":str}}],"
    "\"defects\":[str],\"verdict\":\"PASS\"|\"FAIL\"}}")


def img_url(path, side=1600):
    im = Image.open(path).convert("RGB")
    im.thumbnail((side, side))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def ask(model, path, expect):
    (base, key), allowed = ROUTE[model]
    creds.guard(model, allowed)
    URL, KEY = base + "/chat/completions", key
    body = {"model": model, "messages": [{"role": "user", "content": [
        {"type": "text", "text": PROMPT.format(expect=expect)},
        {"type": "image_url", "image_url": {"url": img_url(path)}}]}]}
    err = ""
    for attempt in range(6):
        try:
            r = requests.post(URL, headers={"Authorization": "Bearer " + KEY}, json=body, timeout=600)
            if r.status_code != 200:
                err = f"HTTP {r.status_code} {r.text[:120]}"
                time.sleep(8 * (attempt + 1))
                continue
            txt = r.json()["choices"][0]["message"]["content"]
            return json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
        except Exception as e:
            err = repr(e)[:160]
            time.sleep(8 * (attempt + 1))
    return {"verdict": "ERROR", "defects": [f"[api error] {err}"], "characters": []}


def check(path, expect=""):
    """gpt-6.1-sol is the checker. It runs twice independently; both must PASS.

    Gemini is used only as a tie-break when the two gpt passes disagree, so most images never touch it.
    """
    exp = f"Expected cast: {expect}. " if expect else ""
    a = ask("gpt-6.1-sol", path, exp)
    b = ask("gpt-6.1-sol", path, exp)
    va, vb = a.get("verdict"), b.get("verdict")
    g = {}
    if va == vb == "PASS":
        verdict = "PASS"
    elif "FAIL" in (va, vb) and va != vb and "ERROR" not in (va, vb):
        # one PASS, one FAIL: break the tie with a third gpt pass first; gemini only if that pass also errors
        c = ask("gpt-6.1-sol", path, exp)
        if c.get("verdict") == "ERROR":
            c = ask("gemini-3.8-flash", path, exp)
        g = c
        verdict = "PASS" if c.get("verdict") == "PASS" else "FAIL"
    elif "FAIL" in (va, vb):
        verdict = "FAIL"
    else:
        verdict = "ERROR"  # api trouble only; caller should re-check, not regenerate
    return {"file": str(path), "verdict": verdict, "gpt": a, "gpt2": b, "gemini": g}


if __name__ == "__main__":
    args = sys.argv[1:]
    expect = ""
    if "--expect" in args:
        i = args.index("--expect")
        expect = args[i + 1]
        del args[i:i + 2]
    out, *imgs = args
    with ThreadPoolExecutor(6) as ex, open(out, "a", encoding="utf-8") as f:
        for res in ex.map(lambda p: check(p, expect), imgs):
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            f.flush()
            d = [x for k in ("gpt", "gpt2", "gemini") for x in (res.get(k) or {}).get("defects", [])]
            print(f"{res['verdict']}  {Path(res['file']).name}  {'; '.join(d)[:300]}", flush=True)
