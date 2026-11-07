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

import subprocess, numpy as np
sr=16000
raw=subprocess.run(["ffmpeg","-v","error","-i",str(REPO_ROOT / "v2" / "stems" / "htdemucs" / "song" / "vocals.wav"),"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
x=np.frombuffer(raw,np.float32); hop=80; fps=sr/hop
e=np.sqrt(np.convolve(x**2,np.ones(320)/320,"same"))[::hop]; db=20*np.log10(e+1e-6)
lines=[l.split("|") for l in open(str(REPO_ROOT / "ref" / "align_g38.txt"),encoding="utf-8").read().splitlines()]
lines=[(float(s),float(e),t) for s,e,t in lines if not t.startswith(("Intro","Interlude","Outro"))]
out=[]
print("  g38   dip   onset   Δ      dipdepth  text")
for s,e,t in lines:
    a,b=int((s-0.7)*fps),int((s+0.5)*fps)
    seg=db[a:b]; k=int(np.argmin(seg)); dip=(a+k)/fps
    peak=db[a+k:a+k+int(0.4*fps)].max(); thr=seg[k]+0.6*(peak-seg[k])
    j=a+k+int(np.argmax(db[a+k:]>=thr)); on=j/fps
    depth=float(np.median(db[int(s*fps):int((s+1.5)*fps)])-seg[k])
    flag=" <--" if abs(on-s)>0.2 else ""
    print(f"{s:6.1f} {dip:6.2f} {on:6.2f} {on-s:+5.2f}   {depth:5.1f}dB   {t}{flag}")
    out.append((s,on,t))
