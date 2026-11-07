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

from PIL import Image
a = Image.open(str(DESKTOP / "Claude" / "深海少女" / "大肥鱼" / "B0B64586E4BDC525C40509A2DC53497A.png")).convert("RGB")
b = Image.open(str(DESKTOP / "Claude" / "深海少女" / "大肥鱼" / "F83CCD692922DE1571D580ECFBFC54E5.jpg")).convert("RGB")
print(a.size, b.size)
a.thumbnail((1400, 1400))
w, h = b.size; b = b.crop((int(w*0.3), 0, int(w*0.7), int(h*0.6))); b.thumbnail((700, 900))
S = Image.new("RGB", (a.width + b.width, max(a.height, b.height)), (0,0,0)); S.paste(a, (0,0)); S.paste(b, (a.width, 0))
S.save(str(REPO_ROOT / "v2" / "chk" / "df_detail.jpg"), quality=88); print(S.size)
