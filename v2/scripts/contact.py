"""Contact sheets of the rendered MV: one frame from the middle of every shot, timecode-labelled.

Usage: python contact.py <video.mp4> <out_prefix> [--per 30]
Writes <out_prefix>_1.jpg, _2.jpg ... (6 columns x 5 rows each).
"""
import subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT)]
from shotlist import timeline

video, prefix = sys.argv[1], sys.argv[2]
per = int(sys.argv[sys.argv.index("--per") + 1]) if "--per" in sys.argv else 30
cols, cw = 6, 400
ch = cw * 9 // 16
font = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 17)
tmp = ROOT / "tmp" / "contact"
tmp.mkdir(parents=True, exist_ok=True)
shots = timeline()
for page in range((len(shots) + per - 1) // per):
    part = shots[page * per:(page + 1) * per]
    rows = (len(part) + cols - 1) // cols
    S = Image.new("RGB", (cols * cw, rows * ch), (0, 0, 0))
    d = ImageDraw.Draw(S)
    for i, (sid, s, e, key, *_rest) in enumerate(part):
        t = s + (e - s) * 0.55
        fp = tmp / f"{sid}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                        "-vf", f"scale={cw - 4}:{ch - 4}", str(fp)], check=True)
        x, y = (i % cols) * cw, (i // cols) * ch
        S.paste(Image.open(fp), (x + 2, y + 2))
        label = f"{sid}  {int(t // 60)}:{t % 60:04.1f}"
        d.rectangle((x + 2, y + 2, x + 10 + 9 * len(label), y + 24), fill=(0, 0, 0))
        d.text((x + 6, y + 3), label, fill=(255, 230, 120), font=font)
    out = f"{prefix}_{page + 1}.jpg"
    S.save(out, quality=86)
    print(out, S.size, len(part), "shots")
