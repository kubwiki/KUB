#!/usr/bin/env python3
"""Kontaktbogen: viele Bilder eines Videos auf einem Blatt - zum SELBST ANSCHAUEN vor der Abgabe.

  contact_sheet.py video.mp4 out.jpg [--n 24] [--cols 6] [--times 1.0 5.5 ...] [--width 270]
"""
import argparse, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--n", type=int, default=24); ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--times", type=float, nargs="*"); ap.add_argument("--width", type=int, default=270)
    a = ap.parse_args()
    d = dur(a.video)
    times = a.times or [d * (i + 0.5) / a.n for i in range(a.n)]
    tmp = tempfile.mkdtemp(prefix="hcsheet_")
    tiles = []
    for i, t in enumerate(times):
        p = os.path.join(tmp, "f%03d.png" % i)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % t, "-i", a.video, "-frames:v", "1",
                        "-vf", "scale=%d:-2" % a.width, p], check=True)
        if os.path.exists(p): tiles.append((t, Image.open(p).convert("RGB")))
    w, h = tiles[0][1].size
    cols = min(a.cols, len(tiles)); rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 6) + 6, rows * (h + 6) + 6), (30, 30, 30))
    dr = ImageDraw.Draw(sheet)
    try: f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except Exception: f = ImageFont.load_default()
    for i, (t, im) in enumerate(tiles):
        x = 6 + (i % cols) * (w + 6); y = 6 + (i // cols) * (h + 6)
        sheet.paste(im, (x, y))
        dr.rectangle([x, y, x + 58, y + 18], fill=(0, 0, 0)); dr.text((x + 4, y + 2), "%.1fs" % t, fill=(255, 255, 255), font=f)
    sheet.save(a.out, quality=90)
    print("Kontaktbogen:", a.out, "(%d Bilder)" % len(tiles))

if __name__ == "__main__":
    main()
