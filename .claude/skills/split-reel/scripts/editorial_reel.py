#!/usr/bin/env python3
"""Split-Reel im Magazin-Look mit Filmkorn (Standard-Look des Skills).

  editorial_reel.py spec.json

Oben: Magazin-Typografie (League Gothic + Cormorant + Inter), Foto-Wipes mit Akzentkante, Stempel,
Durchstreichen, Checklisten - alles erscheint genau beim gesprochenen Wort. Mitte: Untertitel.
Unten: das Querformat-Video als Karte. Darueber Lichtschimmer, Vignette und Filmkorn.
Alle Zeitangaben ("at", "from") sind Sekunden der ORIGINAL-Datei (wie in transcript.json).

Spec-Felder (Beispiel: examples/editorial_spec_example.json):
  src, out, pieces[[a,b],...] oder [{a,b}], transcript (Pfad oder Liste), fixes {alt: neu|null},
  header {left, right}, keywords [...] (Woerter, die im Untertitel in Akzentfarbe stehen),
  colors {bg, accent, ink, dim}, grain (Standard 6), fps (25), punch_in (true = jeder 2. Schnitt
  leicht gezoomt, versteckt Jumpcuts), voice_src (optional: Tonspur aus anderer Datei),
  images {name: pfad oder {path, crop:[x0,y0,x1,y1]}}, scenes [{from, elements:[...]}].

Element-Typen (y = Grundlinie in px, Bildhoehe 1920; oberer Bereich ca. 150-900):
  eyebrow  {text, y, x?}                      kleine Ueberschrift mit Linie, bei Szenenstart
  serif    {text, at, y, size?, color?}       elegante Zeile (Cormorant)
  big      {text, at, y, size?, color?, outline?}  grosse Zeile (League Gothic)
  slam     {text, at, y, size?, color?}       grosse Zeile, die reinknallt
  small    {text, at, y, color?}              kleine Versalzeile
  stamp    {text, at, x, y, size?, rot?}      Stempel
  photo    {image, at?, box?, dim?, zoom?}    Foto mit Wisch-Einblendung (Standard-Box 40,140,1040,880)
  tiles    {items:[{image, label, sub, at, dull?}]}  zwei Fotokacheln nebeneinander
  ranking  {items:[{text, at, out?}], y?, badge?}   Liste; Eintrag wird bei "out" durchgestrichen
  checklist{items:[{text, at}], y?, size?}    Haken-Liste
  strike   {text, at, out, y, x?, size?, label?}   Zeile, die bei "out" durchgestrichen wird
Farben: "ink" (hell), "accent" (Gold), "dim" (grau) oder [r,g,b].
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, '..', 'assets', 'fonts')
X = lambda p: os.path.expanduser(p)

spec_path = sys.argv[1]
SPEC = json.load(open(spec_path))
BASE = os.path.dirname(os.path.abspath(spec_path))
def P(p): p = X(p); return p if os.path.isabs(p) else os.path.join(BASE, p)

W, H = 1080, 1920
FPS = int(SPEC.get('fps', 25))
C = SPEC.get('colors', {})
def rgb(v, d): return tuple(v) if isinstance(v, (list, tuple)) else (tuple(int(v.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) if v else d)
BLACK = rgb(C.get('bg'), (9, 9, 10)); GOLD = rgb(C.get('accent'), (232, 176, 74))
WHITE = rgb(C.get('ink'), (244, 241, 234)); DIM = rgb(C.get('dim'), (120, 116, 108))
COL = {'ink': WHITE, 'white': WHITE, 'accent': GOLD, 'gold': GOLD, 'dim': DIM}
def col(v, d=None): return d if v is None else (COL[v] if isinstance(v, str) else tuple(v))
GRAIN = float(SPEC.get('grain', 6))

SRC = P(SPEC['src']); ASRC = P(SPEC.get('voice_src', SPEC['src']))
PIECES = [(p['a'], p['b']) if isinstance(p, dict) else tuple(p) for p in SPEC['pieces']]
VDUR = sum(b - a for a, b in PIECES); DUR = VDUR; N = int(DUR * FPS)
def T(t):
    off = 0.0
    for a, b in PIECES:
        if a <= t <= b: return off + (t - a)
        off += b - a
    off = 0.0
    for a, b in PIECES:                       # Toleranz fuer Werte knapp ausserhalb
        if a - 0.3 <= t <= b + 0.3: return off + min(max(t - a, 0), b - a)
        off += b - a
    raise SystemExit('Zeit %.2f liegt in keinem Stueck (pieces pruefen)' % t)

FC = {}
def F(kind, size, w=700):
    k = (kind, size, w)
    if k not in FC:
        if kind == 'LG': f = ImageFont.truetype(os.path.join(FD, 'LeagueGothic.ttf'), size)
        elif kind == 'CO':
            f = ImageFont.truetype(os.path.join(FD, 'Cormorant.ttf'), size)
            try: f.set_variation_by_axes([w])
            except Exception: pass
        else:
            f = ImageFont.truetype(os.path.join(FD, 'Inter.ttf'), size)
            try: f.set_variation_by_axes([min(32, max(14, size // 3)), w])
            except Exception:
                try: f.set_variation_by_axes([w])
                except Exception: pass
        FC[k] = f
    return FC[k]
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

IMGS = {}
for k, v in SPEC.get('images', {}).items():
    if isinstance(v, str): v = {'path': v}
    im = Image.open(P(v['path'])).convert('RGB')
    IMGS[k] = im.crop(tuple(v['crop'])) if v.get('crop') else im
def dull(im): return ImageEnhance.Brightness(ImageOps.grayscale(im).convert('RGB')).enhance(0.55).filter(ImageFilter.GaussianBlur(2))

# ---------------- Zeichen-Bausteine ----------------
def tracked(draw, xy, text, font, fill, track=6):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + track
    return x
def tracked_w(text, font, track=6): return sum(font.getlength(c) + track for c in text) - track
def cover(im, w, h, z=1.0, fy=0.5):
    r = max(w / im.width, h / im.height) * z
    im2 = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = (im2.width - w) // 2; y = int((im2.height - h) * fy)
    return im2.crop((x, y, x + w, y + h))
def fit(txt, kind, size, maxw, w=700):
    while size > 30 and F(kind, size, w).getlength(txt) > maxw: size -= 4
    return F(kind, size, w)
def reveal(fr, txt, font, fill, x, y, prog, stroke=0, stroke_fill=None):
    if prog <= 0: return
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    dd.text((x, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, anchor='ls')
    bb = dd.textbbox((x, y), txt, font=font, stroke_width=stroke, anchor='ls')
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rectangle((0, bb[3] + 10 - (bb[3] - bb[1] + 20) * prog, W, bb[3] + 10), fill=255)
    L.putalpha(Image.composite(L.getchannel('A'), Image.new('L', (W, H), 0), m))
    fr.alpha_composite(L)
def eyebrow(fr, txt, r, x=80, y=170):
    if r < 0: return
    dd = ImageDraw.Draw(fr); p = ease(r / 0.5)
    dd.line((x, y + 12, x + 60 * p, y + 12), fill=GOLD + (255,), width=2)
    if p > 0.3: tracked(dd, (x + 76, y), txt.upper(), F('IN', 22, 700), GOLD + (int(255 * ease((r - 0.1) / 0.4)),), 6)
def photo(fr, im, box, r, z0=1.04, z1=1.12, dur=6.0, wipe=0.5, grad=True, dim=0):
    if r < 0: return
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    z = z0 + (z1 - z0) * min(1, r / dur)
    Pi = cover(im, w, h, z).convert('RGBA')
    if grad:
        g = Image.new('L', (1, h)); g.putdata([int(235 * max(0, (yy / h - 0.35) / 0.65) ** 1.4) for yy in range(h)])
        Pi = Image.alpha_composite(Pi, Image.merge('RGBA', [Image.new('L', (w, h), BLACK[0])] * 3 + [g.resize((w, h))]))
    if dim: Pi = Image.alpha_composite(Pi, Image.new('RGBA', (w, h), BLACK + (int(dim),)))
    p = ease(r / wipe)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rectangle((0, 0, int(w * p), h), fill=255)
    Pi.putalpha(m); fr.alpha_composite(Pi, (x0, y0))
    if p < 1: ImageDraw.Draw(fr).line((x0 + w * p, y0, x0 + w * p, y1), fill=GOLD + (255,), width=3)
def stamp(fr, txt, r, cx, cy, size=48, rot=-8, c=None):
    if r < 0: return
    c = c or GOLD
    sc = 1.0 + 0.9 * (1 - min(1, r / 0.16))
    f = F('IN', size, 800); tw = tracked_w(txt, f, 6); pad = 26
    S = Image.new('RGBA', (int(tw + 2 * pad + 20), int(size + 2 * pad + 20)), (0, 0, 0, 0)); ds = ImageDraw.Draw(S)
    ds.rectangle((10, 10, S.width - 10, S.height - 10), outline=c + (255,), width=5)
    ds.rectangle((20, 20, S.width - 20, S.height - 20), outline=c + (160,), width=2)
    tracked(ds, (10 + pad, 10 + pad - size * 0.12), txt, f, c + (255,), 6)
    noise = (np.random.default_rng(len(txt)).random((S.height, S.width)) > 0.18)
    S.putalpha(Image.fromarray((np.array(S.getchannel('A')) * noise).astype(np.uint8)))
    S = S.resize((int(S.width * sc), int(S.height * sc)), Image.BICUBIC).rotate(rot, expand=True, resample=Image.BICUBIC)
    al = min(1, r / 0.06)
    if al < 1: S.putalpha(S.getchannel('A').point(lambda v: int(v * al)))
    fr.alpha_composite(S, (int(cx - S.width / 2), int(cy - S.height / 2)))
def big(fr, txt, t, at, x=76, y=700, size=260, c=None, outline=False, dur=0.4, maxw=930):
    c = c or WHITE; f = fit(txt, 'LG', size, maxw)
    if outline: reveal(fr, txt, f, (0, 0, 0, 0), x, y, ease((t - at) / dur), stroke=4, stroke_fill=c + (255,))
    else: reveal(fr, txt, f, c + (255,), x, y, ease((t - at) / dur))
def serif(fr, txt, t, at, x=80, y=500, size=96, c=None):
    reveal(fr, txt, fit(txt, 'CO', size, 1000 - x, 500), (c or WHITE) + (255,), x, y, ease((t - at) / 0.45))
def slam(fr, txt, t, at, x=76, y=800, size=330, c=None):
    r = t - at
    if r <= 0: return
    sc = 1 + 0.35 * (1 - ease(r / 0.18)); f = fit(txt, 'LG', int(size * sc), 960)
    sh = int(18 * max(0, 1 - r / 0.25) * math.sin(r * 95))
    ImageDraw.Draw(fr).text((x + sh, y), txt, font=f, fill=(c or GOLD) + (255,), anchor='ls')
def small(fr, txt, t, at, x=82, y=840, c=None):
    if t < at: return
    a = int(255 * ease((t - at) / 0.4)); tracked(ImageDraw.Draw(fr), (x, y), txt.upper(), F('IN', 24, 600), (c or DIM) + (a,), 5)
def strikeline(fr, x, y, w, t, at, c=None):
    r = t - at
    if r <= 0: return
    ImageDraw.Draw(fr).line((x, y, x + w * ease(r / 0.25), y), fill=(c or GOLD) + (255,), width=10)

# ---------------- Elemente aus der Spec ----------------
def el(fr, e, t, t0):
    k = e['type']; at = T(e['at']) if 'at' in e else t0
    if k == 'eyebrow': eyebrow(fr, e['text'], t - at - 0.1, e.get('x', 80), e.get('y', 190))
    elif k == 'serif': serif(fr, e['text'], t, at, e.get('x', 80), e['y'], e.get('size', 96), col(e.get('color')))
    elif k == 'big': big(fr, e['text'], t, at, e.get('x', 76), e['y'], e.get('size', 230), col(e.get('color')), e.get('outline', False))
    elif k == 'slam': slam(fr, e['text'], t, at, e.get('x', 76), e['y'], e.get('size', 250), col(e.get('color'), GOLD))
    elif k == 'small': small(fr, e['text'], t, at, e.get('x', 82), e['y'], col(e.get('color')))
    elif k == 'stamp': stamp(fr, e['text'], t - at, e.get('x', 800), e.get('y', 400), e.get('size', 44), e.get('rot', -8))
    elif k == 'photo':
        z = e.get('zoom', [1.0, 1.1])
        photo(fr, IMGS[e['image']], tuple(e.get('box', (40, 140, 1040, 880))), t - at, z[0], z[1], 7, 0.5, dim=e.get('dim', 0))
    elif k == 'tiles':
        for i, it in enumerate(e['items'][:2]):
            r = t - T(it['at']) + 0.15
            if r < 0: continue
            x0 = 60 + i * 490; box = (x0, 210, x0 + 470, 820); isd = it.get('dull', False)
            photo(fr, dull(IMGS[it['image']]) if isd else IMGS[it['image']], box, r, 1.05, 1.12, 5, 0.45)
            if r > 0.3:
                dd = ImageDraw.Draw(fr); a = int(255 * ease((r - 0.25) / 0.3))
                dd.text((x0 + 26, 760), it['label'], font=fit(it['label'], 'LG', 110, 420), fill=(DIM if isd else WHITE) + (a,), anchor='ls')
                tracked(dd, (x0 + 28, 780), it.get('sub', '').upper(), F('IN', 18, 700), GOLD + (a,), 4)
                dd.text((x0 + 440, 246), '0%d' % (i + 1), font=F('IN', 22, 700), fill=GOLD + (a,), anchor='rs')
    elif k == 'ranking':
        y0 = e.get('y', 470); step = e.get('step', 210); size = e.get('size', 220)
        for i, it in enumerate(e['items']):
            y = y0 + i * step; a_ = T(it['at']); out = T(it['out']) if 'out' in it else 1e9
            dead = t >= out
            big(fr, it['text'], t, a_, 76, y, size, DIM if dead else WHITE, outline=dead)
            if dead: strikeline(fr, 70, y - int(size * 0.36), fit(it['text'], 'LG', size, 930).getlength(it['text']) + 20, t, out)
            elif t >= a_ and e.get('badge'): stamp(fr, e['badge'], t - a_ - 0.25, 860, y - 90, 40, -9)
    elif k == 'checklist':
        y0 = e.get('y', 490); step = e.get('step', 92); size = e.get('size', 72)
        for i, it in enumerate(e['items']):
            y = y0 + i * step; a_ = T(it['at'])
            if t >= a_:
                a = int(255 * ease((t - a_) / 0.3)); dd = ImageDraw.Draw(fr)
                dd.rectangle((82, y + 8, 112, y + 38), outline=GOLD + (a,), width=3)
                if t >= a_ + 0.25: dd.line((88, y + 22, 96, y + 32, 108, y + 12), fill=GOLD + (a,), width=4)
            serif(fr, it['text'], t, a_, 140, y + 40, size)
    elif k == 'strike':
        y = e['y']; x = e.get('x', 210); size = e.get('size', 110)
        if e.get('label') and t >= at: reveal(fr, e['label'].upper(), F('IN', 26, 800), DIM + (255,), 82, y - 5, ease((t - at) / 0.3))
        big(fr, e['text'], t, at, x, y, size, DIM)
        if 'out' in e: strikeline(fr, x - 5, y - int(size * 0.32), fit(e['text'], 'LG', size, 1000 - x).getlength(e['text']) + 15, t, T(e['out']))
    else: raise SystemExit('Unbekannter Element-Typ: %s' % k)

SC = sorted(SPEC['scenes'], key=lambda s: s.get('from', 0))
SCENES = []
for i, s in enumerate(SC):
    t0 = 0.0 if i == 0 else T(s['from']); t1 = DUR + 1 if i == len(SC) - 1 else T(SC[i + 1]['from'])
    SCENES.append((t0, t1, s['elements']))
def run(sc, fr, t):
    for e in sc[2]: el(fr, e, t, sc[0])

# ---------------- Untertitel ----------------
tr = SPEC['transcript']; tr = tr if isinstance(tr, list) else [tr]
allw = []
for p_ in tr:
    d = json.load(open(P(p_)))
    allw += [(w['w'], w['s'], w['e']) for s in d['segments'] for w in s['words']]
fix = SPEC.get('fixes', {})
ws = []
for w, s, e in sorted(allw, key=lambda x: x[1]):
    if any(a - 0.02 <= s <= b for a, b in PIECES):
        w = fix.get(w, w)
        if w is None: continue
        if w.startswith('-') and ws: ws[-1][0] += w; continue
        ws.append([w, T(s)])
chunks, cur = [], []
for w in ws:
    cur.append(w)
    if w[0][-1] in ',.?!' or len(cur) >= 4 or len(' '.join(x[0] for x in cur)) > 24:
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
subs = [(c[0][1], chunks[i + 1][0][1] if i + 1 < len(chunks) else VDUR + 0.3, ' '.join(x[0] for x in c)) for i, c in enumerate(chunks)]
keyset = {k.strip(',.?!-').lower() for k in SPEC.get('keywords', [])}

# ---------------- Hintergrund ----------------
BG = Image.new('RGB', (W, H), BLACK); d = ImageDraw.Draw(BG)
hd = SPEC.get('header', {})
tracked(d, (60, 58), hd.get('left', '').upper(), F('IN', 24, 700), WHITE, 5)
rt = hd.get('right', '').upper(); tracked(d, (W - 60 - tracked_w(rt, F('IN', 22, 500), 5), 60), rt, F('IN', 22, 500), GOLD, 5)
d.line((60, 104, W - 60, 104), fill=tuple(min(255, c + 30) for c in BLACK), width=1)
VX, VY, VW, VH = 40, 1060, 1000, 562
d.rectangle((VX - 2, VY - 2, VX + VW + 1, VY + VH + 1), outline=tuple(int(c * 0.52) for c in GOLD), width=2)
yy, xx = np.mgrid[0:H, 0:W]
dd_ = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = np.clip(1 - 0.5 * np.clip(dd_ - 0.5, 0, 1) ** 1.4, 0, 1)[..., None].astype(np.float32)
LEAKC = np.array([c * 0.16 for c in GOLD], np.float32)
def leak(t):
    cx = 300 + 400 * math.sin(t * 0.25); cy = 420 + 120 * math.cos(t * 0.31)
    g = np.exp(-(((xx - cx) / 520) ** 2 + ((yy - cy) / 380) ** 2))
    return (g[..., None] * LEAKC).astype(np.float32)
rng = np.random.default_rng(3); LEAKS = {}

# ---------------- Schnitt + Ausgabe ----------------
src_w, src_h = map(int, subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x', SRC]).decode().strip().split('x'))
cw, ch = int(src_w / 1.12) // 2 * 2, int(src_h / 1.12) // 2 * 2
PUNCH = f'crop={cw}:{ch}:{(src_w - cw) // 2}:0,' if SPEC.get('punch_in', True) else ''
vin, vfc, afc, ain = [], [], [], []
for i, (a, b) in enumerate(PIECES):
    vin += ['-ss', f'{a}', '-t', f'{b - a}', '-i', SRC]
    ain += ['-ss', f'{a}', '-t', f'{b - a}', '-i', ASRC]
    vfc.append(f'[{i}:v]fps={FPS},setpts=PTS-STARTPTS,' + (PUNCH if i % 2 else '') +
               f'scale={VW}:{VH}:force_original_aspect_ratio=increase:flags=lanczos,crop={VW}:{VH},setsar=1[v{i}]')
    afc.append(f'[{i}:a]asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.04}:d=0.04[a{i}]')
n = len(PIECES)
vfc.append(''.join(f'[v{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0[vv]')
afc.append(''.join(f'[a{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,apad=whole_dur={DUR},loudnorm=I=-14:TP=-1.5,alimiter=limit=0.8:attack=3:release=50:level=false,afade=t=out:st={DUR - 0.6}:d=0.6[aa]')
OUT = P(SPEC.get('out', 'editorial_reel.mp4')); os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
AUD = os.path.splitext(OUT)[0] + '_ton.m4a'
subprocess.run(['ffmpeg', '-y', '-v', 'error'] + ain + ['-filter_complex', ';'.join(afc), '-map', '[aa]', '-c:a', 'aac', '-b:a', '192k', AUD], check=True)
p_in = subprocess.Popen(['ffmpeg', '-v', 'error'] + vin + ['-filter_complex', ';'.join(vfc), '-map', '[vv]', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
p_out = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', AUD,
                          '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-b:v', '14M', '-maxrate', '16M', '-bufsize', '28M', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-t', f'{DUR}', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
last = None
for i in range(N):
    t = i / FPS
    raw = p_in.stdout.read(VW * VH * 3)
    if len(raw) == VW * VH * 3: last = Image.frombuffer('RGB', (VW, VH), raw)
    fr = BG.copy()
    if last is not None: fr.paste(last, (VX, VY))
    fr = fr.convert('RGBA')
    k = next(j for j, s in enumerate(SCENES) if s[0] <= t < s[1]); st = SCENES[k]
    if k > 0 and t - st[0] < 0.22:
        Pp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); run(SCENES[k - 1], Pp, t)
        a = 1 - (t - st[0]) / 0.22; Pp.putalpha(Pp.getchannel('A').point(lambda v: int(v * a)))
        fr.alpha_composite(Pp.crop((0, 120, W, 900)), (0, 120))
    S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); run(st, S, t); fr.alpha_composite(S)
    sub = next((s for s in subs if s[0] <= t < s[1]), None)
    if sub:
        dd = ImageDraw.Draw(fr); f = F('IN', 48, 700); parts = sub[2].split(' ')
        while f.size > 30 and sum(f.getlength(p_) for p_ in parts) + f.getlength(' ') * (len(parts) - 1) > 0.9 * W: f = F('IN', f.size - 4, 700)
        widths = [f.getlength(p_) for p_ in parts]; sp = f.getlength(' ')
        x = (W - (sum(widths) + sp * (len(parts) - 1))) / 2; a = int(255 * ease((t - sub[0]) / 0.12))
        for p_, w_ in zip(parts, widths):
            c = GOLD if p_.strip(',.?!-').lower() in keyset else WHITE
            dd.text((x, 960), p_, font=f, fill=c + (a,), anchor='ls'); x += w_ + sp
    arr = np.asarray(fr.convert('RGB')).astype(np.float32)
    key = int(t * 5)
    if key not in LEAKS: LEAKS = {key: leak(t)}
    arr += LEAKS[key]; arr *= VIG
    if GRAIN > 0: arr += rng.normal(0, GRAIN, (H, W, 1)).astype(np.float32)
    if t > DUR - 0.6: arr *= max(0.0, (DUR - t) / 0.6)
    p_out.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
p_out.stdin.close(); p_out.wait(); p_in.kill()
os.remove(AUD)
print('Fertig:', OUT)
