"""Labelled contact sheet of storyboard paintings in shot order.

Usage: python sheet.py <out.jpg> <key-prefix ...> [--cols 5] [--w 480]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT)]
from shotlist import SHOTS

a = sys.argv[1:]
cols = int(a[a.index("--cols") + 1]) if "--cols" in a else 5
cw = int(a[a.index("--w") + 1]) if "--w" in a else 480
out, *pre = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or not a[i - 1].startswith("--"))]
keys = [s[2] for s in SHOTS if s[2].startswith(tuple(pre)) and (ROOT / "img" / f"{s[2]}.png").exists()]
ch = round(cw * 1024 / 1536)
rows = (len(keys) + cols - 1) // cols
S = Image.new("RGB", (cols * cw, rows * ch), (0, 0, 0))
d = ImageDraw.Draw(S)
f = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 18)
for i, k in enumerate(keys):
    im = Image.open(ROOT / "img" / f"{k}.png").convert("RGB").resize((cw - 4, ch - 4))
    x, y = (i % cols) * cw, (i // cols) * ch
    S.paste(im, (x + 2, y + 2))
    d.rectangle((x + 2, y + 2, x + 12 + 11 * len(k), y + 26), fill=(0, 0, 0))
    d.text((x + 6, y + 3), k, fill=(255, 230, 120), font=f)
S.save(out, quality=85)
print(len(keys), S.size)
