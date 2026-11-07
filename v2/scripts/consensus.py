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

import subprocess, numpy as np, re
sr=16000
raw=subprocess.run(["ffmpeg","-v","error","-i",str(REPO_ROOT / "v2" / "stems" / "htdemucs" / "song" / "vocals.wav"),"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
x=np.frombuffer(raw,np.float32); hop=80; fps=sr/hop
e=np.sqrt(np.convolve(x**2,np.ones(320)/320,"same"))[::hop]; db=20*np.log10(e+1e-6)
def load(p):
    L=[]
    for l in open(p,encoding="utf-8").read().splitlines():
        s,en,t=l.split("|"); t=t.rstrip("，,")
        if t.startswith(("[","Intro","Interlude","Outro")): continue
        L.append((float(s),float(en) if en.count(".")<2 else 74.8,t))
    return L
g38=load(str(REPO_ROOT / "ref" / "align_g38.txt")); g35=load(str(REPO_ROOT / "ref" / "align_g35.txt"))
assert len(g38)==len(g35), (len(g38),len(g35))
def stem_on(s):
    a,b=int((s-0.7)*fps),int((s+0.5)*fps); seg=db[a:b]; k=int(np.argmin(seg))
    peak=db[a+k:a+k+int(0.4*fps)].max(); thr=seg[k]+0.6*(peak-seg[k]); j=a+k+int(np.argmax(db[a+k:]>=thr))
    depth=float(np.median(db[int(s*fps):int((s+1.5)*fps)])-seg[k]); return j/fps, depth
def stem_off(en, nxt):
    a,b=int((en-1.2)*fps),int(min(en+0.8,nxt)*fps); seg=db[a:b]
    loud=np.flatnonzero(seg>np.percentile(db[int((en-3)*fps):int(en*fps)],60)-18)
    return (a+loud[-1])/fps if len(loud) else en
rows=[]
for i,((s8,e8,t),(s5,e5,_)) in enumerate(zip(g38,g35)):
    so,dep=stem_on(s8)
    cands=[s8,s5]+([so] if dep>15 else [])
    c=float(np.median(cands))
    nxt=g38[i+1][0] if i+1<len(g38) else 217
    rows.append([c,max(cands)-min(cands),s8,s5,so,dep,t,e8])
for i,r in enumerate(rows):
    nxt=rows[i+1][0] if i+1<len(rows) else 217
    off=stem_off(r[7], nxt)
    r.append(min(max(off+0.25, r[0]+1.0), nxt-0.05))
with open(str(REPO_ROOT / "v2" / "lyrics_times.txt"),"w",encoding="utf-8") as f:
    for r in rows: f.write(f"{r[0]:.2f}|{r[8]:.2f}|{r[6]}\n")
print(" v2用   g38    g35   stem(深度)  分歧  句子")
for r in rows:
    flag="  ★" if abs(r[0]-r[2])>=0.2 else ""
    print(f"{r[0]:6.2f} {r[2]:6.1f} {r[3]:6.1f} {r[4]:6.2f}({r[5]:4.0f}) {r[1]:4.2f}  {r[6]}{flag}")
