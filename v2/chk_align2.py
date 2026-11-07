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
st=np.frombuffer(raw,np.float32).reshape(-1,2); mid=st.mean(1); side=(st[:,0]-st[:,1])/2
win=np.hanning(n)
def spec(x):
    f=np.lib.stride_tricks.sliding_window_view(x,n)[::hop]*win; return np.abs(np.fft.rfft(f,axis=1))
M=spec(mid); Sd=spec(side); fr=np.fft.rfftfreq(n,1/sr); band=(fr>300)&(fr<4000)
# harmonicity proxy: vocal band energy minus side energy, smoothed
voc=np.maximum(M[:,band]-1.0*Sd[:,band],0).sum(1); voc=np.log1p(voc)
voc=np.convolve(voc,np.ones(5)/5,"same")
per=60/136.9; ph=0.16
lines=[l.split("|") for l in open(str(REPO_ROOT / "ref" / "align_g38.txt"),encoding="utf-8").read().splitlines()]
prev_end=0
print(" g38   rise   diff  nearest-beat  text")
out=[]
for s,e,t in lines:
    s,e=float(s),float(e)
    if t.startswith(("Intro","Interlude","Outro")): continue
    a,b=int((s-0.7)*fps),int((s+0.7)*fps)
    seg=voc[a:b]
    lo_i=int(np.argmin(seg[:int(0.9*fps)]))  # trough before/at start
    hi=seg[lo_i:].max(); lo=seg[lo_i]
    thr=lo+0.5*(hi-lo)
    k=lo_i+int(np.argmax(seg[lo_i:]>=thr)); rt=(a+k)/fps
    nb=ph+round((rt-ph)/per*2)/2*per  # nearest half-beat
    flag="  <--" if abs(rt-s)>0.25 else ""
    print(f"{s:5.1f}  {rt:6.2f}  {rt-s:+5.2f}  {nb:7.2f}     {t}{flag}")
