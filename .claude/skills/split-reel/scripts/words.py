#!/usr/bin/env python3
"""Zeigt die Woerter mit genauen Zeiten in einem Ausschnitt - zum Setzen von Schnitten und Text-Slams.

  words.py transcript.json 266.5 275.1
"""
import json, sys
t = json.load(open(sys.argv[1], encoding="utf-8")); a = float(sys.argv[2]); b = float(sys.argv[3])
for s in t["segments"]:
    for w in s["words"]:
        if w["e"] >= a and w["s"] <= b:
            print("%8.2f - %8.2f  %s" % (w["s"], w["e"], w["w"]))
