"""Generate all scene images (skips ones that already exist).

Usage: python batch_gen.py [scene_id ...]
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
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen import generate
from scenes import SCENES, STYLE

OUT = Path(str(REPO_ROOT / "img"))
only = set(sys.argv[1:])


def job(scene):
    sid, _, _, refs, prompt = scene
    out = OUT / f"{sid}.png"
    if out.exists() and not only:
        return sid, True
    ok = generate(str(out), STYLE + prompt, refs, "1536x1024", retries=6)
    return sid, ok


todo = [s for s in SCENES if not only or s[0] in only]
with ThreadPoolExecutor(4) as ex:
    for sid, ok in ex.map(job, todo):
        print(("DONE " if ok else "FAIL ") + sid, flush=True)
