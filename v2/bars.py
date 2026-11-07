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
sr=22050; hop=256; n=2048; fps=sr/hop
raw=subprocess.run(["ffmpeg","-v","error","-i",str(REPO_ROOT / "ref" / "song.mp3"),"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
x=np.frombuffer(raw,np.float32)
f=np.lib.stride_tricks.sliding_window_view(x,n)[::hop]*np.hanning(n); S=np.abs(np.fft.rfft(f,axis=1)); fr=np.fft.rfftfreq(n,1/sr)
low=np.log1p(S[:,(fr>40)&(fr<130)].sum(1)); lf=np.maximum(np.diff(low,prepend=low[0]),0)
hi=np.log1p(S[:,(fr>5000)].sum(1)); hf=np.maximum(np.diff(hi,prepend=hi[0]),0)
per=60/136.9; ph=0.16
idx=lambda t:np.interp(t*fps,np.arange(len(lf)),lf)
for m in range(4):
    ts=ph+per*np.arange(m,480,4); ts=ts[ts<214]
    print("beat mod4 =",m,"kick",round(float(np.mean([idx(t) for t in ts])),3))
rms=np.sqrt(np.convolve(x**2,np.ones(sr)/sr,"same"))[::sr//2]
print(" ".join(f"{i/2:.0f}:{v*100:.0f}" for i,v in enumerate(rms) if i%4==0))
