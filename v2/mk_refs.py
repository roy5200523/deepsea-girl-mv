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

from PIL import Image, ImageDraw
import glob
def fit(p, w, h):
    im = Image.open(p).convert("RGB"); im.thumbnail((w, h)); c = Image.new("RGB", (w, h), (40,40,40)); c.paste(im, ((w-im.width)//2, (h-im.height)//2)); return c
items = [str(DESKTOP / "QQ_1793944415098.png"), str(DESKTOP / "Claude" / "深海少女" / "小克_设定图.png")]
items += sorted(glob.glob(str(DESKTOP / "Claude" / "深海少女" / "大肥鱼" / "*")))
items += sorted(glob.glob(str(DESKTOP / "Claude" / "深海少女" / "Claude" / "*")))
cols, cw, ch = 5, 480, 400
rows = (len(items)+cols-1)//cols
S = Image.new("RGB", (cols*cw, rows*ch), (0,0,0)); d = ImageDraw.Draw(S)
for i,p in enumerate(items):
    x, y = (i%cols)*cw, (i//cols)*ch; S.paste(fit(p, cw-6, ch-6), (x+3, y+3)); d.text((x+8, y+8), str(i), fill=(255,255,0))
S.save("refs_sheet.jpg", quality=85); print(len(items), S.size)
