"""Run many generations in parallel from a JSON job list.

Usage: python batch.py <jobs.json> [--workers 4] [--force]
jobs.json: [{"out": "...png", "prompt": "text" | "prompt_file": "...", "refs": [...], "size": "1536x1024",
             "model": "gpt-image-2", "bg": null}, ...]
Skips jobs whose output exists unless --force.
"""
import json, sys, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen2 import generate

args = sys.argv[1:]
workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 4
force = "--force" in args
jobs = json.loads(Path(args[0]).read_text(encoding="utf-8"))
lock = threading.Lock()


def log(msg):
    with lock:
        print(msg, flush=True)


def run(j):
    if Path(j["out"]).exists() and not force:
        return j["out"], True
    prompt = j.get("prompt") or Path(j["prompt_file"]).read_text(encoding="utf-8")
    ok = generate(j["out"], prompt, j.get("refs", []), j.get("size", "1536x1024"), j.get("model", "gpt-image-2"),
                  j.get("bg"), retries=j.get("retries", 4), log=log)
    return j["out"], ok


with ThreadPoolExecutor(workers) as ex:
    for out, ok in ex.map(run, jobs):
        log(("DONE " if ok else "FAIL ") + Path(out).name)
