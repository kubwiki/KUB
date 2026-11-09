#!/usr/bin/env python3
"""Transkribiert ein Video/Audio mit faster-whisper (laeuft lokal, kostenlos) - mit Zeitstempel pro Wort.

  transcribe.py video.mp4 out_dir [--lang de] [--model small] [--start 0] [--end 180]

Schreibt in out_dir:
  transcript.json  (segments + words mit Sekunden-Zeiten der ORIGINAL-Datei)
  transcript.txt   (lesbar: [von-bis] Satz)
"""
import argparse, json, os, subprocess, sys, tempfile

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("out_dir")
    ap.add_argument("--lang", default=None, help="z.B. de, en (leer = automatisch erkennen)")
    ap.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3 (small ist guter Kompromiss)")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    wav = os.path.join(tempfile.mkdtemp(prefix="hc_"), "a.wav")
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(a.start)]
    if a.end: cmd += ["-t", str(a.end - a.start)]
    cmd += ["-i", a.video, "-vn", "-ac", "1", "-ar", "16000", wav]
    subprocess.run(cmd, check=True)
    from faster_whisper import WhisperModel
    print("Lade Spracherkennung (%s) - beim ersten Mal wird das Modell einmalig geladen ..." % a.model, flush=True)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, info = model.transcribe(wav, language=a.lang, word_timestamps=True, vad_filter=True,
                                  vad_parameters=dict(min_silence_duration_ms=300))
    out = {"language": info.language, "segments": []}
    lines = []
    for s in segs:
        words = [{"w": w.word.strip(), "s": round(w.start + a.start, 3), "e": round(w.end + a.start, 3)}
                 for w in (s.words or [])]
        out["segments"].append({"s": round(s.start + a.start, 3), "e": round(s.end + a.start, 3),
                                "text": s.text.strip(), "words": words})
        lines.append("[%7.2f-%7.2f]  %s" % (s.start + a.start, s.end + a.start, s.text.strip()))
        print(lines[-1], flush=True)
    with open(os.path.join(a.out_dir, "transcript.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out_dir, "transcript.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Fertig:", os.path.join(a.out_dir, "transcript.txt"))

if __name__ == "__main__":
    main()
