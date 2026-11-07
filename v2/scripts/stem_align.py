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
x=np.frombuffer(raw,np.float32)
hop=160; fps=sr/hop
e=np.sqrt(np.convolve(x**2,np.ones(400)/400,"same"))[::hop]
db=20*np.log10(e+1e-6); ref=np.percentile(db[db>-60],95)
on=db>ref-24
# fill tiny gaps
from itertools import groupby
segs=[];i=0
for k,g in groupby(enumerate(on),key=lambda t:t[1]):
    g=list(g)
    if k: segs.append([g[0][0]/fps,(g[-1][0]+1)/fps])
m=[]
for s in segs:
    if m and s[0]-m[-1][1]<0.12: m[-1][1]=s[1]
    else: m.append(s)
m=[s for s in m if s[1]-s[0]>0.08]
lines=[l.split("|") for l in open(str(REPO_ROOT / "ref" / "align_g38.txt"),encoding="utf-8").read().splitlines()]
lines=[(float(s),float(e),t) for s,e,t in lines if not t.startswith(("Intro","Interlude","Outro"))]
starts=np.array([s[0] for s in m]); ends=np.array([s[1] for s in m])
print("g38s  stem_s  d     g38e  stem_e  text")
res=[]
for i,(s,e,t) in enumerate(lines):
    c=starts[(starts>s-0.75)&(starts<s+0.6)]
    vs=float(c[np.argmin(np.abs(c-s))]) if len(c) else float("nan")
    nxt=lines[i+1][0] if i+1<len(lines) else 1e9
    ce=ends[(ends>e-1.0)&(ends<min(e+1.2,nxt+0.3))]
    ve=float(ce.max()) if len(ce) else float("nan")
    flag=" <--" if abs(vs-s)>0.25 else ""
    print(f"{s:6.1f} {vs:6.2f} {vs-s:+5.2f}  {e:6.1f} {ve:6.2f}  {t}{flag}")
