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
raw=subprocess.run(["ffmpeg","-v","error","-i",str(REPO_ROOT / "ref" / "song.mp3"),"-ac","2","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
st=np.frombuffer(raw,np.float32).reshape(-1,2)
mid=st.mean(1)  # vocals usually centre-panned
side=(st[:,0]-st[:,1])/2
win=np.hanning(n)
def spec(x):
    f=np.lib.stride_tricks.sliding_window_view(x,n)[::hop]*win
    return np.abs(np.fft.rfft(f,axis=1))
M=spec(mid); Sd=spec(side)
fr=np.fft.rfftfreq(n,1/sr); band=(fr>250)&(fr<3500)
voc=np.log1p(np.maximum(M[:,band]-1.2*Sd[:,band],0)).sum(1)
voc=np.convolve(voc,np.ones(6)/6,"same")
on=np.maximum(np.diff(voc,prepend=voc[0]),0)
bpm=136.9; per=60/bpm; ph=0.16
lines=[l.split("|") for l in open(str(REPO_ROOT / "ref" / "align_g38.txt"),encoding="utf-8").read().splitlines()]
print("start_g38  vocal_onset  diff   beat#  text")
for s,e,t in lines:
    if t.startswith(("Intro","Interlude","Outro")): continue
    s=float(s); a,b=int((s-0.45)*fps),int((s+0.45)*fps)
    seg=on[a:b]; k=a+int(np.argmax(seg)); vt=k/fps
    # also check vocal level just before start (should be low)
    beat=(vt-ph)/per
    flag="  <--" if abs(vt-s)>0.25 else ""
    print(f"{s:7.1f}  {vt:8.2f}  {vt-s:+5.2f}  {beat:6.2f}  {t}{flag}")
