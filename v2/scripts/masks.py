"""Character masks for parallax layers (rembg isnet-anime). Run with the v2 venv python.

Usage: venv\\Scripts\\python.exe masks.py [key ...]   (default: all img/*.png without a mask, skipping no-people shots)
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter
from rembg import new_session, remove

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT)]
from prompts import PAINT

IMG, MASK = ROOT / "img", ROOT / "masks"
MASK.mkdir(exist_ok=True)
sess = new_session("isnet-anime")
keys = sys.argv[1:] or [p.stem for p in sorted(IMG.glob("*.png"))]
for k in keys:
    out = MASK / f"{k}.png"
    if out.exists() or PAINT.get(k, ("-",))[0] == "-":
        continue
    im = Image.open(IMG / f"{k}.png").convert("RGB")
    m = remove(im, session=sess, only_mask=True, post_process_mask=True)
    # soften + slightly shrink so the parallax seam hides inside the line art
    m = m.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(3))
    cover = sum(m.histogram()[128:]) / (m.width * m.height)
    if cover < 0.02 or cover > 0.85:  # segmentation failed or the girl fills the frame: no parallax
        print(f"skip {k} cover={cover:.2f}", flush=True)
        continue
    m.save(out)
    print(f"mask {k} cover={cover:.2f}", flush=True)
