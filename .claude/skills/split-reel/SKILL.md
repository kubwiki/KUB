---
name: split-reel
description: "Split-Reel - macht aus einem Querformat-Video, in dem jemand etwas erklaert, ein Hochformat-Reel (9:16) im Magazin-Look: das Video unten als Karte, Untertitel in der Mitte, oben grosse Typografie, Fotos mit Gold-Wischkante und Stempel, die genau beim gesprochenen Wort erscheinen. Filmkorn und Vignette. Komplett lokal und kostenlos (ffmpeg, Python, Whisper - keine KI-Generierung, 0 Credits). Erklaert auch selbst, was es kann. Trigger: 'Split-Reel', 'mach ein Split-Reel', 'mach aus dem Querformat ein Reel mit Grafiken oben', 'Video unten, Grafiken oben', 'Reel mit Visualisierung oben', 'was kann Split-Reel', 'turn this landscape video into a split reel'."
---

# Split-Reel

Macht aus einem Querformat-Redevideo ein Hochformat-Reel im Magazin-Look: oben grosse Typografie, Fotos und Stempel zum Gesagten, in der Mitte die Untertitel, unten das Video als Karte. Alles laeuft auf dem Rechner des Nutzers mit kostenlosen Werkzeugen, ohne KI-Generierung, ohne Credits, ohne Upload. Du sprichst mit dem Nutzer in Alltagssprache (Deutsch, per Du, kurz, keine Fachbegriffe).

```
SR=.claude/skills/split-reel               # Ordner dieses Skills (im Projekt; bei globaler Installation ~/.claude/skills/split-reel)
PY=~/.hollywood-cut/venv/bin/python        # Python-Umgebung (legt setup.sh an; geteilt mit dem Skill Hollywood Cut, falls vorhanden)
```

## Wenn jemand fragt, was Split-Reel kann

Nichts installieren, nichts starten, nur kurz antworten, ungefaehr so:

> Schick mir ein Querformat-Video, in dem du etwas erklaerst. Ich mache daraus ein Hochformat-Reel im Magazin-Look: dein Video unten, Untertitel in der Mitte und oben grosse Worte, Fotos und Stempel, die genau dann erscheinen, wenn du das Wort sagst. Unten bleibt Platz fuer die Instagram-Texte. Kostet nichts und laeuft auf deinem Rechner.

## Vorbereitung (immer zuerst)

1. `bash $SR/scripts/setup.sh --check` - zeigt, was fehlt.
2. Fehlt etwas: in einem Satz sagen, was passiert ("Ich installiere einmalig ein paar kostenlose Werkzeuge"), dann `bash $SR/scripts/setup.sh`. Fehlt Homebrew, den einen Befehl von https://brew.sh nennen.
3. Nur wenn das Video Hintergrundmusik hat: `bash $SR/scripts/setup.sh --voice` und Stimme isolieren (`bash $SR/scripts/isolate_voice.sh <video> <ordner>`), dann `voice_src` in der Spec setzen. Musik-Check: Pegel in einer Sprechpause messen (`ffmpeg -ss <s> -t 0.5 -i <video> -af volumedetect -f null -`); unter ca. -50 dB = keine Musik.

Arbeitsordner: neuer Ordner, z.B. `~/Desktop/Split-Reel-Arbeit/<projektname>/` (nie vorhandene Ordner anfassen). YouTube-Link: `bash $SR/scripts/download.sh <link> <ordner>`.

## Ablauf

Layout 1080x1920: Kopfzeile (Name links, Rubrik rechts in Gold) | OBEN der Grafikbereich, ca. y 150-900 | MITTE Untertitel (Grundlinie y 960, max. ~4 Woerter, Schluesselwoerter in Gold) | UNTEN das 16:9-Video als Karte (y 1060-1622, duenne Goldlinie) | darunter frei. Ueber allem: Gold-Lichtschimmer, Vignette, Filmkorn.

### 1. Transkribieren und zuschneiden

`$PY $SR/scripts/transcribe.py <video> <ordner>` (bei langen Videos nur den Bereich mit `--start/--end`). Wortzeiten ansehen: `$PY $SR/scripts/words.py <ordner>/transcript.json <von> <bis>`.

- **Kurzes Video (bis ca. 60 s):** komplett nehmen, vom ersten bis zum letzten Wort - auch den Aufruf am Ende ("schreib mir in die Kommentare"). Nichts rausschneiden.
- **Langes Video:** eine in sich geschlossene Kernaussage (ca. 30-45 s), die allein verstaendlich ist. Teile duerfen verbunden werden (z.B. Hook-Frage + Hauptstelle). Lieber ein etwas laengeres, verstaendliches Reel als ein kurzes ohne Kontext.
- **Schnittpunkte:** Start ca. 0,1 s vor dem ersten Wort. Ende ca. 0,3-0,5 s nach dem Wortende aus dem Transkript (die Enden dort sind zu frueh), aber nie in das naechste Wort hinein. Stellen ohne Gesicht oder mit eingeblendeter Grafik meiden.
- **Schluss:** kein Standbild. Der Renderer blendet Bild und Ton in den letzten 0,6 s aus - das letzte Stueck so legen, dass die Ausblendung in der Sprechpause nach dem letzten Wort liegt.

### 2. Szenen planen

Ein Thema = eine Szene (meist 3-10 Szenen, je 3-6 s). Jede Szene hat `from` (Sekunde im Original, ab der sie gilt) und `elements`. Jedes Element hat `at` = die Sekunde, in der das Wort gesprochen wird - **Dinge erscheinen genau beim Wort**, nie vorher. Ohne `at` erscheint ein Element beim Szenenstart.

| Typ | Was es ist | Felder |
|---|---|---|
| `eyebrow` | kleine Gold-Ueberschrift mit Linie (Rubrik der Szene) | `text`, `y` (meist 190) |
| `serif` | elegante Zeile (Cormorant), fuer Saetze | `text`, `at`, `y`, `size` (64-96), `color` |
| `big` | grosse Versalzeile (League Gothic), weiss | `text`, `at`, `y`, `size` (170-260), `outline` (nur Kontur = "weniger wert") |
| `slam` | grosse Zeile, die reinknallt, Gold - das Wort der Szene | `text`, `at`, `y`, `size` (230-340) |
| `small` | kleine Versalzeile, grau | `text`, `at`, `y`, `color` |
| `stamp` | schraeger Stempel ("ZUERST", "SCHRITT 2") | `text`, `at`, `x`, `y`, `size` (36-44), `rot` |
| `photo` | Foto mit Gold-Wischkante, Standard-Box 40,140,1040,880 | `image`, `at`, `box`, `dim` (0-120), `zoom` |
| `tiles` | zwei Fotokacheln nebeneinander | `items[{image,label,sub,at,dull}]` |
| `ranking` | Liste grosser Woerter, Eintrag wird bei `out` durchgestrichen | `items[{text,at,out}]`, `y`, `step`, `size` |
| `checklist` | Haken-Liste | `items[{text,at}]`, `y`, `size` |
| `strike` | Zeile, die bei `out` durchgestrichen wird | `text`, `at`, `out`, `y`, `size`, `label` |

Farben: `ink` (hell), `accent` (Gold), `dim` (grau). `y` ist die Grundlinie der Zeile.

**Platz:** Eyebrow y 190, erste Textzeile ab y ~420, letzte grosse Zeile Grundlinie hoechstens 900. Eine grosse Zeile (`big`/`slam`) braucht nach oben ca. 0,8 x `size` Platz - sonst ueberlappt sie die Zeile darueber. Zeilen duerfen sich beruehren, nie ueberlappen.

**Nie leer:** Jede Szene zeigt ab ihrem Start sofort mindestens eine Zeile. Wenn das Schluesselwort erst nach 2 s faellt, davor eine `serif`-Zeile zum gerade Gesagten setzen.

**Rezepte, die funktionieren:**
- Hook / Frage: `serif` (Anfang des Satzes) + `big` + `slam` (die Pointe in Gold).
- Gegensatz ("Zeit statt Geld"): `slam` Gold fuer das Wichtige, `serif` dim dazwischen, `big` mit `outline` fuer das Unwichtige.
- Aufzaehlung ("Restaurant, Kino, Park"): pro Begriff ein `photo` + `big`-Label, jeweils beim Wort - das naechste Foto wischt ueber das vorherige. Ohne Fotos: `ranking`.
- Schritt-Logik: `stamp` "ZUERST" / "SCHRITT 2" beim passenden Wort.
- Schluss: `serif` + `big` + `slam`. Aufruf am Ende: `serif` (Frage) + `slam` ("IN DIE KOMMENTARE.") + `small`.

`keywords`: 2-4 Woerter, die im Untertitel in Gold stehen (Gross/Klein und Satzzeichen egal). `fixes`: Wort-Korrekturen (`{"Tools": "-Tools"}` haengt an das vorherige Wort an -> "KI-Tools"; `null` loescht ein Wort). `header.left` = Name oder Kanal des Nutzers (aus dem Gespraech, sonst fragen), `header.right` = Rubrik ("Realtalk", "Tipp", ...).

### 3. Fotos (optional, aber der Look lebt davon)

Keine KI-Bilder. Drei Quellen, alle kostenlos:
1. Standbilder aus dem Video selbst (`ffmpeg -ss <s> -i <video> -frames:v 1 bild.jpg`) - gut, wenn im Video etwas gezeigt wird.
2. Eigene Bilder des Nutzers.
3. Freie Fotos (CC0, ohne Namensnennung) ueber Openverse, ohne Anmeldung:
   `curl -s -G "https://api.openverse.org/v1/images/" --data-urlencode "q=<suchwort englisch>" --data-urlencode "license=cc0,pdm" --data-urlencode "size=large" --data-urlencode "page_size=10"` - aus dem JSON `url` und `width` lesen, Treffer mit mindestens ~960 px Breite laden (stocksnap/rawpixel liefern ~1000 px, das reicht fuer die Fotobox). Ein paar Kandidaten laden, als Uebersicht ansehen, die staerksten nehmen.

Bilder in `<ordner>/bilder/` ablegen und in der Spec unter `images` eintragen.

### 4. Spec schreiben und rendern

Vorlage: `$SR/examples/editorial_spec_example.json`. Rendern: `$PY $SR/scripts/editorial_reel.py <ordner>/spec.json` (ca. 1-2 Minuten pro 40 s).

Felder: `src`, `out`, `pieces[[a,b],...]`, `transcript` (Pfad oder Liste), `fixes`, `keywords`, `header{left,right}`, `images{name: pfad | {path, crop}}`, `scenes[{from, elements}]`, `colors{bg,accent,ink,dim}`, `grain` (Standard 6), `fps` (25), `punch_in` (jeder zweite Schnitt leicht gezoomt, versteckt Jumpcuts), `voice_src`. Alle Zeiten sind Sekunden der Originaldatei.

### 5. Look

Standard: fast Schwarz #09090A, Gold #E8B04A, Creme #F4F1EA, Grau #78746C, Korn 6. Nutzer duerfen gern eigene Farben waehlen (`colors`) - nicht jedes Reel muss gleich aussehen. Schriften (League Gothic, Cormorant, Inter) liegen im Skill, freie Lizenzen.

## Pflicht-Kontrolle vor der Abgabe (nie ueberspringen)

1. `$PY $SR/scripts/contact_sheet.py <video> <ordner>/sheet.jpg --n 24 --cols 8 --width 240` - das Bild **selbst ansehen**. Den Nutzer nie bitten, selbst zu pruefen. Bei Zweifel einzelne Bilder ziehen: `ffmpeg -ss <s> -i <video> -frames:v 1 -vf scale=300:-1 chk.jpg`.
2. Pruefen: Untertitel passen zum Gesagten und sind richtig geschrieben? Erscheint alles beim Wort? Ueberlappt nichts? Kein Text abgeschnitten? Keine Szene, die lange leer bleibt? Unten frei?
3. Ton: ca. -14 LUFS, True Peak unter -1 dBFS (`ffmpeg -i <video> -af ebur128=peak=true -f null -`).
4. Fehler beheben, neu rendern, nochmal ansehen. Erst dann abgeben.

## Abgabe

`$PY $SR/scripts/finalize.py <ordner>/<fertig>.mp4 --name "<Titel-ohne-Leerzeichen>"` legt **eine** Datei in voller Qualitaet auf `~/Desktop` (ueberschreibt nie; `--handy` macht zusaetzlich eine kleine Kopie, nur wenn der Nutzer das will). Dem Nutzer in 1-2 Zeilen sagen, wo die Datei liegt. Nichts hochladen, nichts posten.

## Regeln (fest)

1. **Untere ~15 % bleiben frei** (Instagram legt dort Text drueber) und **keine grosse Leere in der Mitte** - das Layout ist darauf ausgelegt, nicht verschieben.
2. **Eine Kernaussage**, die allein funktioniert. Kurze Videos komplett, lange auf 30-45 s.
3. **Worte nie abhacken**, kein Standbild am Ende, Ausblenden in der Sprechpause.
4. **Nie zwei Musikstuecke gleichzeitig.** Hat das Video Musik: Stimme isolieren.
5. **Text hoechstens ca. 90 % der Bildbreite** (schrumpft automatisch).
6. **0 Credits:** keine KI-Bilder, kein KI-Video, keine bezahlten Dienste.
7. Quellvideo nie veraendern; Ergebnisse nur in den Arbeitsordner und zum Schluss auf den Schreibtisch.
