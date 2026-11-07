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
sr = 22050
raw = subprocess.run(["ffmpeg","-v","error","-i",str(REPO_ROOT / "ref" / "song.mp3"),"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
x = np.frombuffer(raw, np.float32); print("dur", len(x)/sr)
hop, n = 256, 2048
win = np.hanning(n)
frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * win
S = np.abs(np.fft.rfft(frames, axis=1))
S = np.log1p(S * 10)
flux = np.maximum(S[1:] - S[:-1], 0).sum(1); flux = np.concatenate([[0], flux])
flux = flux - np.convolve(flux, np.ones(16)/16, "same"); flux = np.maximum(flux, 0)
fps = sr / hop
def tempo(seg):
    ac = np.correlate(seg, seg, "full")[len(seg)-1:]
    lags = np.arange(len(ac)) / fps
    best = None
    for bpm in np.arange(70, 200, 0.1):
        L = fps * 60 / bpm
        sc = sum(np.interp(L * k, np.arange(len(ac)), ac) for k in (1, 2, 4))
        if best is None or sc > best[0]: best = (sc, bpm)
    return best[1]
a, b = int(10*fps), int(200*fps)
bpm = tempo(flux[a:b]); print("bpm", round(bpm, 2))
# phase: find offset maximizing sum of flux on grid
period = 60 / bpm
best = max(((sum(np.interp((off + k*period) * fps, np.arange(len(flux)), flux) for k in range(int(200/period))), off) for off in np.arange(0, period, 0.005)))
print("phase offset", round(best[1], 3))
np.save(str(REPO_ROOT / "v2" / "flux.npy"), flux)
# local tempo check in windows
for t0 in range(10, 210, 40):
    print(t0, round(tempo(flux[int(t0*fps):int((t0+30)*fps)]), 2))
