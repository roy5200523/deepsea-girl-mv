"""Render 深海少女 MV v2.

Per shot: painting split into background + character layer (mask from rembg, if present) for parallax;
camera move by motion code; "boil" (wobbly redraw every 3 frames) to mimic hand-drawn animation; particles;
paper grain + noise; beat-synced flashes and shakes; handwritten bilingual subtitles.

Usage: python render2.py [--preview T0 T1] [--still t ...] [--workers N] [--out file.mp4]
"""

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
import argparse, math, random, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT)]
from shotlist import timeline, lyrics, BAR, BEAT, T0, END

IMG, MASK, TMP = ROOT / "img", ROOT / "masks", ROOT / "tmp"
VID, VFR, VFPS = ROOT / "vid", ROOT / "tmp" / "vidframes", 10
AUDIO = Path(str(REPO_ROOT / "ref" / "song.mp3"))
W, H, FPS = 1920, 1080, 30
FONT_JP = str(ROOT / "fonts" / "KleeOne-SemiBold.ttf")
FONT_CN = str(ROOT / "fonts" / "LXGWWenKai-Medium.ttf")
BOIL_EVERY = 3  # frames per drawing ("on threes")
XF = 0.12       # very short dissolve at cuts (hard cut feel)

SUNNY = ("l", "m")  # above-water shots: no bubbles, sparkles instead
HOT_LINES = {"「ほらね、", "君も素敵な色を隠してた」", "もう放っておいてよ！"}

# moments that get a white flash / screen shake (time, strength)
FLASH = [(19.03, 0.45), (40.04, 0.25), (43.11, 0.3), (82.10, 0.25), (92.17, 0.3), (121.12, 0.5), (138.66, 0.2),
         (160.57, 0.25), (164.07, 0.75), (170.87, 0.35), (195.63, 0.9)]
SHAKE = [(25.58, 0.6), (43.11, 0.4), (104.03, 0.6), (113.0, 0.5), (121.12, 1.0), (122.88, 0.7), (164.07, 0.6),
         (195.63, 0.8)]


def clamp01(x):
    return min(max(x, 0.0), 1.0)


def ease(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


# ------------------------------------------------------------------ textures (precomputed once per process)
_TEX = {}


def paper():
    """Paper grain: low-frequency blotches + fibres, multiplicative around 1.0."""
    if "paper" not in _TEX:
        rng = np.random.default_rng(7)
        lo = Image.fromarray((rng.random((H // 24, W // 24)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        mid = Image.fromarray((rng.random((H // 4, W // 4)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        fib = Image.fromarray((rng.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
        p = (np.asarray(lo, np.float32) - 128) * 0.00035 + (np.asarray(mid, np.float32) - 128) * 0.0005 \
            + (np.asarray(fib, np.float32) - 128) * 0.0011
        _TEX["paper"] = (1 + p)[..., None].astype(np.float32)
    return _TEX["paper"]


def grain(frame_no):
    """Film/pencil grain that changes on each drawing (on threes)."""
    k = frame_no // BOIL_EVERY % 6
    key = ("grain", k)
    if key not in _TEX:
        rng = np.random.default_rng(100 + k)
        g = rng.normal(0, 5.5, (H // 2, W // 2)).astype(np.float32)
        _TEX[key] = np.asarray(Image.fromarray(g).resize((W, H), Image.NEAREST))[..., None]
    return _TEX[key]


def vignette():
    if "vig" not in _TEX:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 * 0.85 + ((yy - H / 2) / (H / 2)) ** 2)
        _TEX["vig"] = (1 - 0.38 * np.clip((r - 0.5) / 0.8, 0, 1) ** 1.5)[..., None].astype(np.float32)
    return _TEX["vig"]


def boil_field(k, amp=1.6):
    """Smooth random displacement map for one drawing index k (wobbly redraw)."""
    key = ("boil", k)
    if key not in _TEX:
        rng = np.random.default_rng(1000 + k)
        dx = Image.fromarray(rng.normal(0, 1, (12, 20)).astype(np.float32)).resize((W, H), Image.BICUBIC)
        dy = Image.fromarray(rng.normal(0, 1, (12, 20)).astype(np.float32)).resize((W, H), Image.BICUBIC)
        _TEX[key] = (np.asarray(dx) * amp, np.asarray(dy) * amp)
    return _TEX[key]


_GRID = None


def warp(arr, k):
    """Apply boil displacement (nearest-pixel remap, cheap)."""
    global _GRID
    if _GRID is None:
        _GRID = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = boil_field(k % 8)
    yy = np.clip(_GRID[0] + dy, 0, H - 1).astype(np.int32)
    xx = np.clip(_GRID[1] + dx, 0, W - 1).astype(np.int32)
    return arr[yy, xx]


# ------------------------------------------------------------------ shots
MOTION = {
    # (zoom0, zoom1, dx0, dx1, dy0, dy1) in fractions of frame; char layer gets extra parallax
    "push": (1.00, 1.10, 0, 0, 0, 0), "pull": (1.12, 1.00, 0, 0, 0, 0),
    "pan-l": (1.10, 1.10, 0.04, -0.04, 0, 0), "pan-r": (1.10, 1.10, -0.04, 0.04, 0, 0),
    "tilt-u": (1.12, 1.12, 0, 0, 0.045, -0.045), "tilt-d": (1.12, 1.12, 0, 0, -0.045, 0.045),
    "sink": (1.10, 1.14, 0, 0, -0.04, 0.05), "rise": (1.14, 1.10, 0, 0, 0.05, -0.04),
    "drift": (1.08, 1.11, -0.015, 0.015, 0.01, -0.01), "shake": (1.12, 1.16, 0, 0, 0, 0),
}


class Shot:
    def __init__(self, idx, sid, start, end, key, motion):
        self.idx, self.sid, self.start, self.end, self.key, self.motion = idx, sid, start, end, key, motion
        self.rng = random.Random(idx * 7919 + 3)
        self.flip = self.rng.random() < 0.0
        self._src = None
        self.sunny = key[0] in SUNNY
        self.particles = self._make_particles()

    @property
    def vframes(self):
        """Sorted frame files of the image-to-video clip (10 fps, i.e. drawn "on threes" at 30 fps), or []."""
        if not hasattr(self, "_vf"):
            d = VFR / self.key
            self._vf = sorted(d.glob("*.jpg")) if d.exists() else []
        return self._vf

    def video_frame(self, t):
        lt = t - self.start + 0.3  # skip the first 0.3 s, which often has a static hold
        i = min(int(lt * VFPS), len(self.vframes) - 1)
        if getattr(self, "_vcache", (None,))[0] != i:
            im = Image.open(self.vframes[i]).convert("RGB")
            k = max(W * 1.1 / im.width, H * 1.1 / im.height)
            self._vcache = (i, im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS))
        return self._vcache[1]

    def load(self):
        if self._src is None:
            im = Image.open(IMG / f"{self.key}.png").convert("RGB")
            k = max(W * 1.2 / im.width, H * 1.2 / im.height)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
            mpath = MASK / f"{self.key}.png"
            m = Image.open(mpath).convert("L").resize(im.size, Image.BILINEAR) if mpath.exists() else None
            self._src = (im, m)
        return self._src

    def cam(self, t):
        z0, z1, x0, x1, y0, y1 = MOTION[self.motion]
        u = ease((t - self.start) / max(self.end - self.start, 0.3))
        z, x, y = z0 + (z1 - z0) * u, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        if self.motion == "shake":
            f = 8.0
            x += math.sin(t * f * 6.28) * 0.006 * (1 - u * 0.6)
            y += math.cos(t * f * 5.1) * 0.005 * (1 - u * 0.6)
        return z, x, y

    def view(self, img, z, x, y):
        bw, bh = img.size
        vw, vh = W * 1.2 / z * (bw / (W * 1.2)), H * 1.2 / z * (bh / (H * 1.2))
        cx, cy = bw / 2 + x * bw, bh / 2 + y * bh
        x0 = min(max(cx - vw / 2, 0), bw - vw)
        y0 = min(max(cy - vh / 2, 0), bh - vh)
        s = vw / W
        return img.transform((W, H), Image.AFFINE, (s, 0, x0, 0, s, y0), Image.BILINEAR)

    def render(self, t):
        if self.vframes:
            # the clip already moves; add only a gentle push so it still feels like a camera
            u = ease((t - self.start) / max(self.end - self.start, 0.3))
            return np.asarray(self.view(self.video_frame(t), 1.0 + 0.04 * u, 0, 0), np.float32)
        im, m = self.load()
        z, x, y = self.cam(t)
        bg = self.view(im, z, x, y)
        if m is None:
            return np.asarray(bg, np.float32)
        # parallax: background moves 70% as far and zooms less; character uses full move plus a slight float
        u = (t - self.start) / max(self.end - self.start, 0.3)
        zb = 1 + (z - 1) * 0.7
        bgl = np.asarray(self.view(im, zb, x * 0.6, y * 0.6), np.float32)
        bob = math.sin(t * 1.3 + self.idx) * 0.004
        fg = np.asarray(self.view(im, z * 1.01, x * 1.15, y * 1.15 + bob), np.float32)
        a = np.asarray(self.view(m, z * 1.01, x * 1.15, y * 1.15 + bob), np.float32)[..., None] / 255
        return bgl * (1 - a) + fg * a

    def _make_particles(self):
        r, P = self.rng, []
        nb = 0 if self.sunny else r.randint(10, 22)
        for _ in range(nb):
            P.append(("bub", r.uniform(0, W), r.uniform(0, H), r.uniform(70, 220), r.uniform(6, 30), r.uniform(0, 6.3),
                      r.choice([10, 14, 18, 24, 32, 44])))
        for _ in range(0 if self.sunny else r.randint(25, 45)):
            P.append(("dust", r.uniform(0, W), r.uniform(0, H), r.uniform(-12, 12), r.uniform(-18, 6), r.uniform(0, 6.3),
                      r.choice([2, 3, 3, 4])))
        if self.key[0] in "jk" or self.key in ("b12_marine_snow", "b11_godrays_whale"):
            for _ in range(120):
                P.append(("snow", r.uniform(0, W), r.uniform(0, H), r.uniform(25, 70), r.uniform(0, 6.3),
                          r.choice([3, 4, 5, 7])))
        if self.sunny or self.key[0] == "i":
            for _ in range(28):
                P.append(("spk", r.uniform(0, W), r.uniform(0, H * 0.8), r.uniform(1.2, 3.0), r.uniform(0, 6.3),
                          r.choice([10, 14, 20])))
        return P

    def draw_particles(self, img, t, frame_no):
        lt = t - self.start
        d = ImageDraw.Draw(img, "RGBA")
        jit = frame_no // BOIL_EVERY  # particles also step on threes
        for p in self.particles:
            k = p[0]
            if k == "bub":
                _, x, y, vy, amp, ph, s = p
                yy = (y - vy * lt) % (H + 120) - 60
                xx = x + math.sin(lt * 1.7 + ph) * amp
                wob = ((jit * 31 + int(ph * 10)) % 3) - 1
                d.ellipse((xx - s / 2 + wob, yy - s / 2, xx + s / 2, yy + s / 2 + wob), outline=(225, 240, 255, 150),
                          width=2 if s < 30 else 3)
                d.arc((xx - s / 3, yy - s / 3, xx + s / 6, yy + s / 6), 190, 260, fill=(255, 255, 255, 200), width=2)
            elif k == "dust":
                _, x, y, vx, vy, ph, s = p
                xx, yy = (x + vx * lt) % W, (y + vy * lt) % H
                a = int(70 + 60 * math.sin(lt * 1.5 + ph))
                d.ellipse((xx, yy, xx + s, yy + s), fill=(210, 230, 255, a))
            elif k == "snow":
                _, x, y, vy, ph, s = p
                yy = (y + vy * lt) % (H + 40) - 20
                xx = (x + math.sin(lt * 0.8 + ph) * 20) % W
                d.ellipse((xx, yy, xx + s, yy + s), fill=(240, 248, 255, 170))
            elif k == "spk":
                _, x, y, sp, ph, s = p
                a = max(0.0, math.sin(lt * sp + ph)) ** 4
                if a > 0.05:
                    c = (255, 250, 230, int(230 * a))
                    d.line((x - s, y, x + s, y), fill=c, width=2)
                    d.line((x, y - s, x, y + s), fill=c, width=2)


# ------------------------------------------------------------------ subtitles (handwritten fonts)
_SUB = {}
CN = {}


def load_cn():
    """Chinese translations: reuse v1 lines by Japanese text."""
    if not CN:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from scenes import LYRICS as V1
        for _, _, jp, cn in V1:
            CN[jp] = cn
        CN["「ほらね、"] = "「你看，"
        CN["君も素敵な色を隠してた」"] = "你也藏着那么美丽的颜色呢」"
    return CN


def sub_img(jp, cn):
    key = (jp, cn)
    if key in _SUB:
        return _SUB[key]
    fj, fc = ImageFont.truetype(FONT_JP, 54), ImageFont.truetype(FONT_CN, 34)
    hot = jp in HOT_LINES
    col = (255, 214, 160) if hot else (250, 247, 238)
    bj, bc = fj.getbbox(jp), fc.getbbox(cn)
    w = max(bj[2] - bj[0], bc[2] - bc[0]) + 120
    h = (bj[3] - bj[1]) + (bc[3] - bc[1]) + 120
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    xj, yj = (w - (bj[2] - bj[0])) / 2 - bj[0], 40 - bj[1]
    xc, yc = (w - (bc[2] - bc[0])) / 2 - bc[0], 40 + (bj[3] - bj[1]) + 24 - bc[1]
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for (x, y, s, f) in ((xj, yj, jp, fj), (xc, yc, cn, fc)):
        sd.text((x + 3, y + 4), s, font=f, fill=(10, 14, 40, 200), stroke_width=5, stroke_fill=(10, 14, 40, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    d.text((xj, yj), jp, font=fj, fill=col + (255,), stroke_width=2, stroke_fill=(20, 26, 60, 230))
    d.text((xc, yc), cn, font=fc, fill=(232, 236, 245, 255), stroke_width=2, stroke_fill=(20, 26, 60, 220))
    out = Image.alpha_composite(sh, im)
    _SUB[key] = out
    return out


def draw_subs(frame, t, frame_no):
    cn = load_cn()
    for s, e, jp in lyrics():
        if s - 0.05 <= t <= e:
            im = sub_img(jp, cn.get(jp, ""))
            a = clamp01((t - s) / 0.25) * clamp01((e - t) / 0.35)
            # per-character "write-on" reveal from left to right over 0.45s
            rev = ease_out((t - s) / 0.45)
            wob = ((frame_no // BOIL_EVERY) % 3 - 1)
            crop = im.crop((0, 0, max(1, int(im.width * rev)), im.height))
            if a < 1:
                crop = crop.copy()
                crop.putalpha(crop.getchannel("A").point(lambda v, a=a: int(v * a)))
            x = (W - im.width) // 2
            y = H - im.height - 28 + wob
            frame.alpha_composite(crop, (x, y))


TITLE = {}


def title(frame, t):
    items = []
    if 0.6 < t < 3.5:
        items.append(("深海少女", 140, H * 0.42, clamp01((t - 0.6) / 0.8) * clamp01((3.5 - t) / 0.5), (t - 0.6) / 1.2))
    if t > 211.0:
        items.append(("大肥鱼 × 小克", 64, H * 0.45, clamp01((t - 211.0) / 1.2), (t - 211.0) / 1.5))
        items.append(("深海少女", 44, H * 0.58, clamp01((t - 212.0) / 1.2), 1.0))
    for txt, size, y, a, rev in items:
        key = (txt, size)
        if key not in TITLE:
            f = ImageFont.truetype(FONT_JP if txt == "深海少女" else FONT_CN, size)
            b = f.getbbox(txt)
            im = Image.new("RGBA", (b[2] - b[0] + 60, b[3] - b[1] + 60), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((30 - b[0], 30 - b[1]), txt, font=f, fill=(250, 246, 236, 255),
                                    stroke_width=2, stroke_fill=(20, 26, 60, 200))
            TITLE[key] = im
        im = TITLE[key]
        im = im.crop((0, 0, max(1, int(im.width * ease_out(rev))), im.height))
        if a < 1:
            im = im.copy()
            im.putalpha(im.getchannel("A").point(lambda v, a=a: int(v * a)))
        frame.alpha_composite(im, ((W - TITLE[key].width) // 2, int(y - im.height / 2)))


# ------------------------------------------------------------------ frame
_SHOTS = None


def shots():
    global _SHOTS
    if _SHOTS is None:
        _SHOTS = [Shot(i, *row[:4], row[4]) for i, row in enumerate(timeline())]
    return _SHOTS


def shot_frame(sh, t, fno):
    arr = sh.render(t)
    k = fno // BOIL_EVERY + sh.idx * 3
    arr = warp(arr, k)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    sh.draw_particles(img, t, fno)
    return np.asarray(img.convert("RGB"), np.float32)


def bump(t, c, w):
    x = (t - c) / w
    return 0.0 if x < 0 or x > 1 else (1 - x) ** 2


def make_frame(fno):
    t = fno / FPS
    S = shots()
    cur = next((s for s in S if s.start <= t < s.end), S[-1])
    arr = shot_frame(cur, t, fno)
    i = cur.idx
    if i > 0 and t - cur.start < XF:
        w = ease((t - cur.start) / XF)
        arr = shot_frame(S[i - 1], t, fno) * (1 - w) + arr * w
    # screen shake on accents (whole frame offset)
    sx = sy = 0.0
    for c, s in SHAKE:
        b = bump(t, c, 0.35) * s
        if b > 0:
            sx += math.sin(t * 90) * 14 * b
            sy += math.cos(t * 77) * 10 * b
    if sx or sy:
        arr = np.roll(arr, (int(sy), int(sx)), (0, 1))
    arr = arr * paper() * vignette() + grain(fno)
    # flashes go on after the paper pass and are additive warm light, so they read as light, not grey fog
    for c, s in FLASH:
        b = bump(t, c - 0.03, 0.3) * s
        if b > 0:
            arr = arr + np.array([255, 236, 205], np.float32) * b
    dim = ease(t / 0.8) * ease((END - t) / 3.5)
    arr *= dim
    frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    title(frame, t)
    draw_subs(frame, t, fno)
    return frame.convert("RGB").tobytes()


def render_chunk(args):
    ci, f0, f1, path = args
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(make_frame(f))
    p.stdin.close()
    p.wait()
    return ci, p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", nargs=2, type=float)
    ap.add_argument("--still", nargs="*", type=float)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=str(ROOT / "深海少女_MV_v2.mp4"))
    a = ap.parse_args()
    TMP.mkdir(exist_ok=True)
    # unpack each i2v clip once at 10 fps so worker processes only read small jpgs
    for v in sorted(VID.glob("*.mp4")):
        d = VFR / v.stem
        if not d.exists():
            d.mkdir(parents=True)
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-vf", f"fps={VFPS}", "-q:v", "2",
                            str(d / "%03d.jpg")], check=True)
    if a.still is not None:
        for t in a.still:
            Image.frombytes("RGB", (W, H), make_frame(int(t * FPS))).save(TMP / f"still_{t:07.2f}.jpg", quality=90)
        return
    t0, t1 = a.preview if a.preview else (0.0, END)
    f0, f1 = int(t0 * FPS), int(t1 * FPS)
    n = max(1, min(a.workers, (f1 - f0) // 60))
    step = math.ceil((f1 - f0) / n)
    jobs = [(i, f0 + i * step, min(f0 + (i + 1) * step, f1), str(TMP / f"v2chunk_{i:03d}.mp4")) for i in range(n)]
    with ProcessPoolExecutor(n) as ex:
        for ci, rc in ex.map(render_chunk, jobs):
            print(f"chunk {ci} rc={rc}", flush=True)
    lst = TMP / "v2chunks.txt"
    lst.write_text("".join(f"file '{j[3]}'\n" for j in jobs), encoding="utf-8")
    dur = t1 - t0
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ss", f"{t0}",
                    "-t", f"{dur}", "-i", str(AUDIO), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "256k", "-af", f"afade=t=out:st={max(0, dur - 4)}:d=4", "-movflags", "+faststart",
                    "-shortest", a.out], check=True)
    print("WROTE", a.out)


if __name__ == "__main__":
    main()
