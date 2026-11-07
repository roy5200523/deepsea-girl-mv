"""Generate storyboard paintings with automatic anatomy QA and retry.

Usage: python paint.py <key-prefix ...|all> [--workers 4] [--tries 3] [--force]
Writes img/<key>.png (accepted), img/rejects/<key>_tN.png (failed QA), and appends to qa_log.jsonl.
"""
import json, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from gen2 import generate
from prompts import PAINT, build
from qa import check
from shotlist import SHOTS

IMG, REJ = ROOT / "img", ROOT / "img" / "rejects"
IMG.mkdir(exist_ok=True)
REJ.mkdir(exist_ok=True)
LOCK = threading.Lock()
EXPECT = {"DF": "one whale girl (blue hair) only",
          "CK": "one orange-haired girl only",
          "DUO": "whale girl (blue hair) and orange-haired girl; in hand-only close-ups exactly one hand from each girl",
          "-": "no people at all"}


def log(msg, rec=None):
    with LOCK:
        print(msg, flush=True)
        if rec:
            with open(ROOT / "qa_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def defects(res):
    return [x for k in ("gpt", "gpt2", "gemini") for x in (res.get(k) or {}).get("defects", [])]


def job(key, tries, force):
    out = IMG / f"{key}.png"
    if out.exists() and not force:
        return key, "skip"
    prompt, refs, model, cast = build(key)
    for n in range(1, tries + 1):
        tmp = REJ / f"{key}_t{n}.png"
        if not generate(str(tmp), prompt, refs, "1536x1024", model, retries=4, log=log):
            continue
        res = check(tmp, EXPECT[cast])
        for _ in range(3):  # API trouble is not a defect: re-check the same image instead of paying for a new one
            if res["verdict"] != "ERROR":
                break
            time.sleep(60)
            res = check(tmp, EXPECT[cast])
        if res["verdict"] == "ERROR":
            log(f"QA-ERROR {key} try{n}: kept {tmp.name} for a later re-check")
            return key, "QA-ERROR"
        d = defects(res)
        log(f"{res['verdict']}  {key} try{n}  {'; '.join(d)[:240]}", {"key": key, "try": n, **res})
        if res["verdict"] == "PASS":
            tmp.replace(out)
            return key, f"PASS(t{n})"
        # feed the defects back so the next attempt avoids them
        prompt = build(key)[0] + "\n\nA previous attempt had these problems, avoid them: " + "; ".join(d)[:600]
    return key, "FAIL"


if __name__ == "__main__":
    a = sys.argv[1:]
    workers = int(a[a.index("--workers") + 1]) if "--workers" in a else 4
    tries = int(a[a.index("--tries") + 1]) if "--tries" in a else 3
    force = "--force" in a
    pre = [x for x in a if not x.startswith("--") and not x.isdigit()]
    order = [s[2] for s in SHOTS]
    missing = [k for k in order if k not in PAINT]
    assert not missing, missing
    keys = order if pre == ["all"] else [k for k in order if k.startswith(tuple(pre))]
    with ThreadPoolExecutor(workers) as ex:
        res = list(ex.map(lambda k: job(k, tries, force), keys))
    for k, r in res:
        log(f"== {k}: {r}")
    print("SUMMARY", {r: sum(1 for _, x in res if x.startswith(r)) for r in ("PASS", "FAIL", "QA-ERROR", "skip")})
