"""Render the 深海少女 MV: Ken Burns scenes + underwater particles + light rays + bilingual subtitles.

Usage: python render.py [--preview T0 T1] [--workers N] [--out file.mp4]
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
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from scenes import SCENES, LYRICS

ROOT = Path(str(REPO_ROOT))
IMG = ROOT / "img"
TMP = ROOT / "tmp"
AUDIO = ROOT / "ref" / "song.mp3"
W, H, FPS = 1920, 1080, 30
END = 214.0
XF = 0.8  # crossfade length between scenes
FONT = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"

BASE_FX = dict(bubbles=14, dust=40, rays=0.0, motes=0, mote_col=(255, 196, 130), snow=0, sparkle=0)
FX = {
    "s01": dict(bubbles=10, dust=50, rays=0.10),
    "s02": dict(bubbles=8, dust=30),
    "s03": dict(bubbles=12, dust=60, rays=0.35, motes=18),
    "s04": dict(bubbles=45, dust=40),
    "s05": dict(bubbles=6, dust=20, rays=0.25, motes=50),
    "s06": dict(bubbles=8, dust=20, motes=60, mote_col=(140, 220, 255)),
    "s07": dict(bubbles=6, dust=40),
    "s08": dict(bubbles=10, dust=40, motes=12),
    "s09": dict(bubbles=6, dust=10, rays=0.45, snow=140),
    "s10": dict(bubbles=6, dust=30, motes=30, mote_col=(120, 230, 220)),
    "s11": dict(bubbles=20, dust=30, rays=0.35, motes=20),
    "s12": dict(bubbles=12, dust=40, rays=0.40, motes=20),
    "s13": dict(bubbles=12, dust=30, rays=0.20, motes=25),
    "s14": dict(bubbles=50, dust=30),
    "s15": dict(bubbles=8, dust=40, motes=10),
    "s16": dict(bubbles=6, dust=50),
    "s17": dict(bubbles=40, dust=40),
    "s18": dict(bubbles=10, dust=30, motes=40, mote_col=(170, 210, 255)),
    "s19": dict(bubbles=10, dust=30, motes=45),
    "s20": dict(bubbles=6, dust=40, motes=10),
    "s21": dict(bubbles=40, dust=50),
    "s22": dict(bubbles=10, dust=30, motes=40),
    "s23": dict(bubbles=12, dust=20, motes=70, mote_col=(160, 200, 255)),
    "s24": dict(bubbles=10, dust=0, snow=170, motes=30),
    "s25": dict(bubbles=40, dust=20, rays=0.40, snow=40),
    "s26": dict(bubbles=70, dust=10, rays=0.50),
    "s27": dict(bubbles=0, dust=0, sparkle=60),
    "s28": dict(bubbles=0, dust=0, sparkle=25),
}
SINK = {"s01", "s07", "s14", "s21"}
RISE = {"s24", "s25", "s26", "s27"}
# (centre time, width, rgb, peak alpha)
FLASHES = [(18.9, 1.0, (255, 225, 180), 0.30), (160.4, 0.6, (255, 230, 200), 0.25),
           (164.2, 1.4, (255, 228, 190), 0.60), (195.8, 1.6, (255, 255, 250), 0.85)]
# (centre time, width) dips to black
DIPS = [(125.1, 0.9), (152.4, 1.2)]
ORANGE_LINES = set()  # 用橙色字幕的那一句（歌词不随仓库分发）


def clamp01(x):
    return min(max(x, 0.0), 1.0)


def ease(x):
    return 0.5 - 0.5 * math.cos(math.pi * clamp01(x))


def bump(t, c, d):
    x = (t - c) / (d / 2)
    return 0.0 if abs(x) >= 1 else 0.5 + 0.5 * math.cos(math.pi * x)


def font(size, weight="SemiBold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def lerp(a, b, u):
    return a + (b - a) * u


# ---------------------------------------------------------------- sprites
_SPR = {}


def bubble_sprite(d):
    key = ("b", d)
    if key not in _SPR:
        S = d * 4
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        dr.ellipse((2, 2, S - 3, S - 3), fill=(190, 225, 255, 22), outline=(220, 242, 255, 175), width=max(3, S // 12))
        dr.ellipse((S * 0.24, S * 0.2, S * 0.46, S * 0.36), fill=(255, 255, 255, 215))
        im = im.resize((d, d), Image.LANCZOS)
        if d > 26:
            im = im.filter(ImageFilter.GaussianBlur(d / 16))
        _SPR[key] = im
    return _SPR[key]


def dot_sprite(d, col, level):
    """Soft round dot; level 1..8 sets opacity."""
    key = ("d", d, col, level)
    if key not in _SPR:
        r = np.linspace(-1, 1, d)
        rr = np.sqrt(r[None, :] ** 2 + r[:, None] ** 2)
        a = np.clip(1 - rr, 0, 1) ** 1.4 * (level / 8)
        arr = np.zeros((d, d, 4), np.uint8)
        arr[..., :3] = col
        arr[..., 3] = (a * 255).astype(np.uint8)
        _SPR[key] = Image.fromarray(arr, "RGBA")
    return _SPR[key]


def glow_arr(d, col):
    """Premultiplied additive glow (float32, HxWx3)."""
    key = ("g", d, col)
    if key not in _SPR:
        r = np.linspace(-1, 1, d)
        rr = np.sqrt(r[None, :] ** 2 + r[:, None] ** 2)
        a = np.exp(-(rr / 0.42) ** 2) * 0.55 + np.exp(-(rr / 0.12) ** 2) * 0.7
        rgb = a[..., None] * np.array(col, np.float32)
        rgb += np.clip(a - 0.75, 0, 1)[..., None] * 400  # white-hot core
        _SPR[key] = rgb.astype(np.float32)
    return _SPR[key]
# ---------------------------------------------------------------- scenes
class Scene:
    def __init__(self, idx, sid, start, end):
        self.idx, self.sid, self.start, self.end = idx, sid, start, end
        self.fx = {**BASE_FX, **FX.get(sid, {})}
        self._big = None
        self.k = 1.2  # 20% headroom for zoom/pan
        rnd = random.Random(idx * 7919 + 17)
        zin = idx % 2 == 0
        self.z0, self.z1 = (1.0, 1.09) if zin else (1.09, 1.0)
        dx, dy = rnd.uniform(-0.035, 0.035), rnd.uniform(-0.03, 0.03)
        if sid in SINK:
            dy = 0.05
        if sid in RISE:
            dy = -0.05
        if sid == "s27":
            self.z0, self.z1 = 1.0, 1.12
        self.c0 = (0.5 - dx, 0.5 - dy)
        self.c1 = (0.5 + dx, 0.5 + dy)
        self.particles = self._make_particles(rnd)

    @property
    def big(self):
        if self._big is None:
            src = Image.open(IMG / f"{self.sid}.png").convert("RGB")
            k = max(W / src.width, H / src.height) * self.k
            self._big = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
        return self._big

    def view(self, t):
        u = ease(lerp(0.0, 1.0, (t - self.start + XF) / (self.end - self.start + 2 * XF)))
        return lerp(self.z0, self.z1, u), lerp(self.c0[0], self.c1[0], u), lerp(self.c0[1], self.c1[1], u)

    def render(self, t):
        z, cx, cy = self.view(t)
        bw, bh = self.big.size
        # window (in big px) that maps to the full output frame; z=1 shows the whole cover-fit image
        vw, vh = W * self.k / z, H * self.k / z
        x0 = min(max(cx * bw - vw / 2, 0), bw - vw)
        y0 = min(max(cy * bh - vh / 2, 0), bh - vh)
        s = vw / W
        return self.big.transform((W, H), Image.AFFINE, (s, 0, x0, 0, s, y0), Image.BICUBIC)

    # particles are deterministic functions of time so frames can render in parallel
    def _make_particles(self, rnd):
        fx, P = self.fx, []
        span = self.end - self.start + 2 * XF + 2
        for _ in range(fx["bubbles"]):
            d = int(rnd.choice([8, 10, 12, 14, 18, 22, 28, 36, 48]))
            P.append(("bub", rnd.uniform(0, W), rnd.uniform(0, H + 200), rnd.uniform(60, 190) * (0.6 + d / 48),
                      rnd.uniform(0.3, 1.4), rnd.uniform(10, 40), rnd.uniform(0, 6.28), d))
        for _ in range(fx["dust"]):
            P.append(("dust", rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(-14, 14), rnd.uniform(-10, 10),
                      rnd.uniform(0, 6.28), rnd.choice([3, 4, 5, 6])))
        for _ in range(fx["snow"]):
            P.append(("snow", rnd.uniform(0, W), rnd.uniform(-100, H), rnd.uniform(25, 70), rnd.uniform(0.2, 0.9),
                      rnd.uniform(0, 6.28), rnd.choice([4, 5, 6, 8, 10])))
        for _ in range(fx["motes"]):
            P.append(("mote", rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(-20, 20), rnd.uniform(-30, 5),
                      rnd.uniform(0, 6.28), rnd.choice([18, 24, 32, 44])))
        for _ in range(fx["sparkle"]):
            P.append(("spk", rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(0.6, 2.2),
                      rnd.uniform(0, 6.28), rnd.choice([20, 28, 40, 56]), 0))
        self.span = span
        return P

    def draw_particles(self, frame, t):
        """Alpha particles onto RGBA layer, additive glows into float array. Returns (rgba_layer, add)."""
        lt = t - self.start + XF + 1
        fx = self.fx
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        add = None
        for p in self.particles:
            kind = p[0]
            if kind == "bub":
                _, x, y, vy, wob, amp, ph, d = p
                yy = (y - vy * lt) % (H + 260) - 130
                xx = x + math.sin(lt * wob + ph) * amp
                layer.alpha_composite(bubble_sprite(d), (int(xx - d / 2), int(yy - d / 2)))
            elif kind == "dust":
                _, x, y, vx, vy, ph, d = p
                xx = (x + vx * lt + math.sin(lt * 0.5 + ph) * 12) % W
                yy = (y + vy * lt + math.cos(lt * 0.4 + ph) * 8) % H
                lvl = 2 + int(2.5 + 2.5 * math.sin(lt * 1.3 + ph))
                layer.alpha_composite(dot_sprite(d, (200, 225, 255), lvl), (int(xx), int(yy)))
            elif kind == "snow":
                _, x, y, vy, wob, ph, d = p
                yy = (y + vy * lt) % (H + 120) - 60
                xx = (x + math.sin(lt * wob + ph) * 25) % W
                layer.alpha_composite(dot_sprite(d, (235, 245, 255), 6), (int(xx), int(yy)))
            elif kind in ("mote", "spk"):
                if add is None:
                    add = np.zeros((H, W, 3), np.float32)
                if kind == "mote":
                    _, x, y, vx, vy, ph, d = p
                    xx = (x + vx * lt + math.sin(lt * 0.7 + ph) * 18) % W
                    yy = (y + vy * lt) % H
                    g = glow_arr(d, fx["mote_col"]) * (0.55 + 0.45 * math.sin(lt * 2.1 + ph))
                else:
                    _, x, y, sp, ph, d, _ = p
                    xx, yy = x, y
                    g = glow_arr(d, (255, 250, 235)) * max(0.0, math.sin(lt * sp + ph)) ** 6
                x0, y0 = int(xx - d / 2), int(yy - d / 2)
                xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + d, W), min(y0 + d, H)
                if xa < xb and ya < yb:
                    add[ya:yb, xa:xb] += g[ya - y0:yb - y0, xa - x0:xb - x0]
        return layer, add


# ---------------------------------------------------------------- global overlays
_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = None
_RAYS = None


def vignette():
    global _VIG
    if _VIG is None:
        nx, ny = (_XX - W / 2) / (W / 2), (_YY - H / 2) / (H / 2)
        r = np.sqrt(nx ** 2 * 0.8 + ny ** 2)
        _VIG = (1 - 0.42 * np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6)[..., None].astype(np.float32)
    return _VIG


def rays_base():
    """Precompute ray angle + falloff for god rays fanning down from a point above the frame."""
    global _RAYS
    if _RAYS is None:
        ox, oy = W * 0.5, -H * 0.55
        ang = np.arctan2(_XX - ox, _YY - oy)
        fall = np.clip(1 - _YY / (H * 1.05), 0, 1) ** 1.3
        _RAYS = (ang.astype(np.float32), fall.astype(np.float32))
    return _RAYS


def rays(t, strength):
    ang, fall = rays_base()
    v = (np.sin(ang * 23 + t * 0.35) * 0.5 + 0.5) ** 3 * 0.6
    v += (np.sin(ang * 41 - t * 0.6 + 1.3) * 0.5 + 0.5) ** 4 * 0.4
    v *= 0.6 + 0.4 * math.sin(t * 0.7)
    return (v * fall * strength * 120)[..., None] * np.array([0.85, 0.95, 1.0], np.float32)


def caustics(t, strength):
    """Shimmering light pattern near the top of the frame."""
    a = np.sin(_XX * 0.011 + t * 1.1 + np.sin(_YY * 0.017 + t * 0.6) * 2.0)
    b = np.sin(_YY * 0.013 - t * 0.9 + np.sin(_XX * 0.009 - t * 0.5) * 2.2)
    v = np.clip(a * b, 0, 1) ** 3
    v *= np.clip(1 - _YY / (H * 0.6), 0, 1) ** 2
    return (v * strength * 90)[..., None] * np.array([0.8, 0.95, 1.0], np.float32)


# ---------------------------------------------------------------- subtitles
_SUB = {}
F_JP, F_CN = None, None


def sub_image(jp, cn):
    global F_JP, F_CN
    key = (jp, cn)
    if key in _SUB:
        return _SUB[key]
    if F_JP is None:
        F_JP, F_CN = font(50, "SemiBold"), font(32, "Medium")
    orange = jp in ORANGE_LINES
    fill_jp = (255, 214, 168) if orange else (246, 250, 255)
    glow_col = (255, 140, 40) if orange else (60, 140, 255)
    pad = 40
    bj, bc = F_JP.getbbox(jp), F_CN.getbbox(cn)
    wj, hj = bj[2] - bj[0], bj[3] - bj[1]
    wc, hc = bc[2] - bc[0], bc[3] - bc[1]
    w, h = max(wj, wc) + pad * 2, hj + hc + 22 + pad * 2
    txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    xj, xc = (w - wj) / 2 - bj[0], (w - wc) / 2 - bc[0]
    yj, yc = pad - bj[1], pad + hj + 22 - bc[1]
    # coloured glow
    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.text((xj, yj), jp, font=F_JP, fill=glow_col + (255,), stroke_width=6, stroke_fill=glow_col + (255,))
    gd.text((xc, yc), cn, font=F_CN, fill=glow_col + (200,), stroke_width=5, stroke_fill=glow_col + (200,))
    gl = gl.filter(ImageFilter.GaussianBlur(11))
    gl.putalpha(gl.getchannel("A").point(lambda v: int(v * 0.75)))
    # dark outline for readability
    d.text((xj, yj), jp, font=F_JP, fill=fill_jp + (255,), stroke_width=3, stroke_fill=(8, 16, 40, 210))
    d.text((xc, yc), cn, font=F_CN, fill=(220, 232, 248, 255), stroke_width=2, stroke_fill=(8, 16, 40, 200))
    out = Image.alpha_composite(gl, txt)
    _SUB[key] = out
    return out


def sub_alpha(t, s, e):
    fi, fo = 0.35, 0.45
    return clamp01((t - s) / fi) * clamp01((e - t) / fo)


def draw_subs(frame, t):
    for s, e, jp, cn in LYRICS:
        if s - 0.05 <= t <= e + 0.05:
            a = sub_alpha(t, s, e)
            if a <= 0:
                continue
            im = sub_image(jp, cn)
            rise = (1 - ease(clamp01((t - s) / 0.5))) * 14
            if a < 1:
                im = im.copy()
                im.putalpha(im.getchannel("A").point(lambda v, a=a: int(v * a)))
            x = (W - im.width) // 2
            y = int(H - 70 - im.height + 40 + rise)
            frame.alpha_composite(im, (x, y))


def title_card(frame, t):
    """Opening title over the first seconds and an ending credit."""
    items = []
    if t < 7.5:
        a = clamp01((t - 0.6) / 1.0) * clamp01((7.2 - t) / 1.2)
        items.append(("深海少女", "Shinkai Shoujo", a, H * 0.40))
    if t > 206.5:
        a = clamp01((t - 207.0) / 1.5)
        items.append(("深海少女", "大肥鱼 × 小克", a, H * 0.80))
    for big, small, a, y in items:
        if a <= 0:
            continue
        key = ("title", big, small)
        if key not in _SUB:
            fb, fs = font(118, "Bold"), font(40, "SemiBold")
            im = Image.new("RGBA", (1100, 330), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            bb = fb.getbbox(big)
            d.text(((1100 - (bb[2] - bb[0])) / 2 - bb[0], 50 - bb[1]), big, font=fb, fill=(240, 248, 255, 255),
                   stroke_width=3, stroke_fill=(10, 20, 50, 150))
            sb = fs.getbbox(small)
            d.text(((1100 - (sb[2] - sb[0])) / 2 - sb[0], 230 - sb[1]), small, font=fs, fill=(225, 238, 255, 255),
                   stroke_width=3, stroke_fill=(10, 20, 50, 190))
            gl = im.filter(ImageFilter.GaussianBlur(14))
            r, g, b, al = gl.split()
            gl = Image.merge("RGBA", (r.point(lambda v: 70), g.point(lambda v: 150), b.point(lambda v: 255), al))
            _SUB[key] = Image.alpha_composite(gl, im)
        im = _SUB[key].copy()
        im.putalpha(im.getchannel("A").point(lambda v, a=a: int(v * a)))
        frame.alpha_composite(im, ((W - im.width) // 2, int(y - im.height / 2)))


# ---------------------------------------------------------------- frame composition
_SCENES = None


def scenes():
    global _SCENES
    if _SCENES is None:
        _SCENES = [Scene(i, sid, s, e) for i, (sid, s, e, _, _) in enumerate(SCENES)]
    return _SCENES


def scene_layer(sc, t):
    img = sc.render(t)
    arr = np.asarray(img, np.float32)
    fx = sc.fx
    if fx["rays"] > 0:
        arr = arr + rays(t, fx["rays"])
    if sc.sid in ("s11", "s25", "s26", "s05"):
        arr = arr + caustics(t, 0.5)
    layer, add = sc.draw_particles(None, t)
    if add is not None:
        arr = arr + add
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    base.alpha_composite(layer)
    return np.asarray(base.convert("RGB"), np.float32)


def make_frame(t):
    S = scenes()
    act = []
    for sc in S:
        if sc.start - XF / 2 <= t < sc.end + XF / 2:
            act.append(sc)
    if not act:
        act = [min(S, key=lambda s: abs(s.start - t))]
    if len(act) == 1:
        arr = scene_layer(act[0], t)
    else:
        a, b = act[0], act[1]
        w = ease((t - (b.start - XF / 2)) / XF)
        arr = scene_layer(a, t) * (1 - w) + scene_layer(b, t) * w

    # flashes and dips
    for c, d, col, peak in FLASHES:
        k = bump(t, c, d) * peak
        if k > 0:
            arr = arr * (1 - k) + np.array(col, np.float32) * k
    dim = 1.0
    for c, d in DIPS:
        dim *= 1 - 0.85 * bump(t, c, d)
    # fade from / to black
    dim *= ease(t / 1.2) * ease((END - t) / 3.0)
    arr = arr * vignette() * dim
    frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    title_card(frame, t)
    draw_subs(frame, t)
    return frame.convert("RGB").tobytes()


def render_chunk(args):
    ci, f0, f1, path = args
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", path],
        stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(make_frame(f / FPS))
    p.stdin.close()
    p.wait()
    return ci, p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", nargs=2, type=float)
    ap.add_argument("--still", nargs="*", type=float)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=str(ROOT / "深海少女_MV.mp4"))
    a = ap.parse_args()
    TMP.mkdir(exist_ok=True)

    if a.still is not None:
        for t in a.still:
            Image.frombytes("RGB", (W, H), make_frame(t)).save(TMP / f"still_{t:07.2f}.jpg", quality=90)
        return

    t0, t1 = a.preview if a.preview else (0.0, END)
    f0, f1 = int(t0 * FPS), int(t1 * FPS)
    n = max(1, min(a.workers, (f1 - f0) // 60))
    step = math.ceil((f1 - f0) / n)
    jobs = [(i, f0 + i * step, min(f0 + (i + 1) * step, f1), str(TMP / f"chunk_{i:03d}.mp4")) for i in range(n)]
    with ProcessPoolExecutor(n) as ex:
        for ci, rc in ex.map(render_chunk, jobs):
            print(f"chunk {ci} rc={rc}", flush=True)
    lst = TMP / "chunks.txt"
    lst.write_text("".join(f"file '{j[3]}'\n" for j in jobs), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ss", f"{t0}", "-t", f"{t1 - t0}",
         "-i", str(AUDIO), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
         "-af", f"afade=t=out:st={max(0, t1 - t0 - 3)}:d=3", "-movflags", "+faststart", "-shortest", a.out],
        check=True)
    print("WROTE", a.out)


if __name__ == "__main__":
    main()