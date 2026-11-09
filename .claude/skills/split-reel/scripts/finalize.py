#!/usr/bin/env python3
"""Abgabe: fertiges Video auf den Schreibtisch - EINE Datei.

  finalize.py fertig.mp4 [--name "Mein-Edit"] [--dest ~/Desktop] [--handy] [--max-mb 28]

Legt <dest>/<name>.mp4 (volle Qualitaet) an. Nur mit --handy zusaetzlich <name>-handy.mp4 (klein, unter 30 MB).
Ueberschreibt NIE eine vorhandene Datei - bei gleichem Namen wird -2, -3 ... angehaengt.
"""
import argparse, os, shutil, subprocess

def uniq(path):
    base, ext = os.path.splitext(path); n = 2; p = path
    while os.path.exists(p):
        p = "%s-%d%s" % (base, n, ext); n += 1
    return p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--name"); ap.add_argument("--dest", default="~/Desktop")
    ap.add_argument("--max-mb", type=float, default=28.0); ap.add_argument("--handy", action="store_true")
    a = ap.parse_args()
    dest = os.path.expanduser(a.dest); os.makedirs(dest, exist_ok=True)
    name = a.name or os.path.splitext(os.path.basename(a.video))[0]
    full = uniq(os.path.join(dest, name + ".mp4")); shutil.copy2(a.video, full)
    if not a.handy:
        print("Fertig:\n  %s" % full); return
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video]))
    w, h = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", a.video]).decode().strip().split("x"))
    audio_k = 128
    vk = min(int((a.max_mb * 8192 / dur) - audio_k) - 40, 5000)   # kbit/s fuer Video: Luft zur Grenze, aber nie unnoetig gross
    scale = "scale=720:-2" if h > w else "scale=1280:-2"
    small = uniq(os.path.join(dest, name + "-handy.mp4"))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-vf", scale, "-c:v", "libx264", "-preset", "medium",
                    "-b:v", "%dk" % vk, "-maxrate", "%dk" % int(vk * 1.4), "-bufsize", "%dk" % (vk * 2),
                    "-c:a", "aac", "-b:a", "%dk" % audio_k, "-movflags", "+faststart", small], check=True)
    mb = os.path.getsize(small) / 1048576.0
    print("Fertig:\n  %s\n  %s  (%.1f MB)" % (full, small, mb))
    if mb > 30: print("WARNUNG: Handy-Kopie ueber 30 MB - mit --max-mb 20 nochmal.")

if __name__ == "__main__":
    main()
