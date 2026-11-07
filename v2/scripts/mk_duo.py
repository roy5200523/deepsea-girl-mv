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

import json
from pathlib import Path
D = Path(str(REPO_ROOT / "v2" / "styletest"))
DF = str(DESKTOP / "Claude" / "深海少女" / "大肥鱼" / "B0B64586E4BDC525C40509A2DC53497A.png")
CK = str(DESKTOP / "Claude" / "深海少女" / "小克_设定图.png")
chars = """Characters (keep identities exactly as in the references):
- The whale girl from the FIRST reference: very long wavy dark indigo-blue hair fading to periwinkle tips, one ahoge, dark navy beret with a tiny white whale clip and blue ribbon, floppy dark-blue whale-fin ears with white frilled edges, violet-blue eyes, white sailor blouse with black bow, oversized cream knit cardigan with navy whale prints, navy plaid skirt with lace frill, dark-blue whale tail.
- The orange-haired girl from the SECOND reference: very long wavy bright orange hair, one ahoge, warm amber eyes, large orange flower hair ornament with a pearl centre on her left side with black ribbon and cream tassels, cream frilled high-collar blouse with orange flower brooch and black cravat, cream capelet with orange embroidery, black corset, layered cream/orange/black skirt.
Scene: underwater, dim indigo water lit by the warm glow coming from the orange-haired girl. Medium two-shot from the side: the orange-haired girl gently holds the whale girl's right hand with her left hand, fingers interlaced, and smiles softly; the whale girl blushes and looks down, her free hand pressed to her chest. Hair floating, a few bubbles. Tender, shy, romantic yuri mood.
Anatomy: each girl has exactly two arms and two hands with five fingers; the joined hands are clearly drawn, one hand from each girl.
No text, no letters, no signature, no watermark, no border."""
A = ("A single frame from a hand-drawn Japanese tegaki music video, drawn by a human artist: rough expressive pencil line art with visible "
     "construction lines and sketchy double strokes, wobbly varying line weight, transparent watercolor and gouache washes bleeding outside "
     "the lines, pigment pooling, cold-press paper grain, white gouache splatters, limited palette of indigo, prussian blue and warm orange. "
     "Imperfect, alive, sketchbook feeling. NOT glossy, NOT 3D, no airbrush gradients, no plastic skin.\n\n" + chars)
B = ("A single frame from a hand-drawn Japanese tegaki (手書き) music video made by one hobbyist artist in a drawing app: rough loose sketch "
     "lines in dark blue pencil brush left un-cleaned, flat anime cel colors laid in quickly with slightly misaligned fills that do not quite "
     "reach the lines, one simple shadow tone, a few hand-drawn highlight scribbles, grainy textured paper overlay, simplified background "
     "painted with a big rough brush. Charming and imperfect, clearly hand-made. NOT glossy, NOT 3D, no soft airbrush rendering, no lens effects.\n\n" + chars)
jobs = []
for tag, p in (("A", A), ("B", B)):
    for m, mt in (("gpt-image-2", "g2"), ("gpt-image-2.6-sunburst", "sun")):
        jobs.append({"out": str(D / f"duo_{tag}_{mt}.png"), "prompt": p, "refs": [DF, CK], "model": m})
(D / "jobs_duo.json").write_text(json.dumps(jobs, ensure_ascii=False, indent=1), encoding="utf-8")
