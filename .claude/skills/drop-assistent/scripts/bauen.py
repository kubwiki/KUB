#!/usr/bin/env python3
"""Baut aus einem Drop-Paket und den Antworten des Mitglieds das fertige, persönliche Freebie.

Aufruf:
  python3 bauen.py --drop <entpackter Drop-Ordner> --antworten antworten.json --ziel <Ausgabeordner>

antworten.json (Beispiel):
{
  "toolName": "Hartmuts Screen Recorder", "deinName": "Hartmut Muster", "farbe": "#0F766E",
  "ueberMich": "...", "newsletterUeber": "Tipps zu Online-Kursen",
  "foto": "foto.jpg",            # optional, Datei liegt neben antworten.json
  "impressum": { "VOLLER NAME": "...", "STRASSE UND HAUSNUMMER": "...", "PLZ ORT": "...", "LAND": "Deutschland", "E-MAIL": "..." },
  "datenschutz": { "HOSTER": "...", "E-MAIL-TOOL": "..." }
}

Ergebnis im Zielordner:
  website/        alles für Netlify (index, bestaetigung, download-xxxx, impressum, datenschutz, ZIP, Foto)
  <Tool>.html     die persönliche Tool-Datei (zum Selbsttesten)
  offene-punkte.txt  Platzhalter, die noch von Hand entschieden werden müssen
"""
import argparse, json, re, secrets, shutil, struct, sys, zipfile, zlib
from pathlib import Path


def js(v):
    return json.dumps(v, ensure_ascii=False)


def set_block(html, const, values):
    """Ersetzt Werte im Konfig-Block `const NAME = { key: 'wert', // Kommentar }` und behält die Kommentare."""
    m = re.search(r'const ' + const + r' = \{\n(.*?)\n\};', html, re.S)
    if not m:
        return html
    lines = []
    for line in m.group(1).split('\n'):
        km = re.match(r"(\s*)(\w+):(\s*)('(?:[^'\\]|\\.)*'),(.*)$", line)
        if km and km.group(2) in values and values[km.group(2)] is not None:
            line = f"{km.group(1)}{km.group(2)}:{km.group(3)}{js(values[km.group(2)])},{km.group(5)}"
        lines.append(line)
    return html[:m.start(1)] + '\n'.join(lines) + html[m.end(1):]


def fill(html, mapping):
    for k, v in mapping.items():
        if v:
            html = html.replace('[[' + k + ']]', v)
    return html


def slug(s):
    s = s.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'tool'


def _png_lesen(data):
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    pos, idat, w = 8, b'', None
    while pos < len(data):
        n, typ = struct.unpack('>I4s', data[pos:pos+8]); body = data[pos+8:pos+8+n]; pos += 12 + n
        if typ == b'IHDR':
            w, h, tiefe, art, _, _, il = struct.unpack('>IIBBBBB', body)
            assert tiefe == 8 and art in (2, 6) and il == 0
            bpp = 3 if art == 2 else 4
        elif typ == b'IDAT': idat += body
    raw = zlib.decompress(idat); stride = w * bpp; out = []; prev = bytearray(stride); i = 0
    for _ in range(h):
        f = raw[i]; line = bytearray(raw[i+1:i+1+stride]); i += 1 + stride
        if f == 1:
            for x in range(bpp, stride): line[x] = (line[x] + line[x-bpp]) & 255
        elif f == 2:
            for x in range(stride): line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride): line[x] = (line[x] + ((line[x-bpp] if x >= bpp else 0) + prev[x]) // 2) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0; b = prev[x]; c = prev[x-bpp] if x >= bpp else 0
                p = a + b - c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out.append(line); prev = line
    return w, h, bpp, out

def _chunk(t, b):
    return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)

def umfaerben(quelle, ziel, hexfarbe):
    """Färbt einen Screenshot, der mit Schlüsselfarbe #00FF00 aufgenommen wurde, in die Markenfarbe um."""
    w, h, bpp, zeilen = _png_lesen(open(quelle, 'rb').read())
    br, bg, bb = (int(hexfarbe[i:i+2], 16) for i in (1, 3, 5))
    tab = {}
    roh = bytearray()
    for line in zeilen:
        neu = bytearray(w * 3)
        for x in range(w):
            o = x * bpp; r, g, b = line[o], line[o+1], line[o+2]
            key = (r, g, b)
            v = tab.get(key)
            if v is None:
                grau = r if r > b else b
                k = g - grau
                if k <= 4: v = key
                else:
                    k = k / 255
                    v = (min(255, round(grau + k*br)), min(255, round(grau + k*bg)), min(255, round(grau + k*bb)))
                tab[key] = v
            neu[x*3:x*3+3] = bytes(v)
        roh += b'\x00' + neu
    png = b'\x89PNG\r\n\x1a\n' + _chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + _chunk(b'IDAT', zlib.compress(bytes(roh), 9)) + _chunk(b'IEND', b'')
    open(ziel, 'wb').write(png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--drop', required=True); ap.add_argument('--antworten', required=True); ap.add_argument('--ziel', required=True)
    a = ap.parse_args()
    drop, ziel = Path(a.drop), Path(a.ziel)
    antw_pfad = Path(a.antworten)
    A = json.loads(antw_pfad.read_text(encoding='utf-8'))
    meta = json.loads((drop / 'drop.json').read_text(encoding='utf-8'))
    farbe = A.get('farbe', '#2563EB')
    if not re.fullmatch(r'#[0-9A-Fa-f]{6}', farbe):
        sys.exit('Farbe bitte als Hex-Code wie #0F766E angeben.')

    web = ziel / 'website'
    if web.exists():
        shutil.rmtree(web)
    web.mkdir(parents=True)

    # 1. Tool personalisieren
    tool_src = (drop / 'tool' / meta['toolDatei']).read_text(encoding='utf-8')
    tool = set_block(tool_src, 'TOOL', {'name': A['toolName'], 'von': A['deinName'], 'farbe': farbe})
    tool_datei = slug(A['toolName']) + '.html'
    (ziel / tool_datei).write_text(tool, encoding='utf-8')

    # Netlify: statische Seite, kein Build, dieser Ordner wird veröffentlicht
    (web / 'netlify.toml').write_text('[build]\n  publish = "."\n  command = ""\n', encoding='utf-8')

    # 2. ZIP für die Abonnenten: Tool + Kurzanleitung
    zip_name = slug(A['toolName']) + '.zip'
    start = (drop / 'tool' / 'SO-STARTEST-DU.txt').read_text(encoding='utf-8')
    start = fill(start, {'TOOLNAME': A['toolName'], 'DEIN NAME': A['deinName'], 'TOOLDATEI': tool_datei})
    with zipfile.ZipFile(web / zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{slug(A['toolName'])}/{tool_datei}", tool)
        z.writestr(f"{slug(A['toolName'])}/SO STARTEST DU.txt", start)

    # 3. Seiten
    dl_name = 'download-' + secrets.token_hex(4) + '.html'   # schwer zu erraten
    seite = {'farbe': farbe, 'toolName': A['toolName'], 'deinName': A['deinName'],
             'ueberMich': A.get('ueberMich'), 'newsletterUeber': A.get('newsletterUeber'),
             'foto': A.get('foto') or '', 'impressum': 'impressum.html', 'datenschutz': 'datenschutz.html',
             'downloadLink': zip_name}
    platz = {'TOOLNAME': A['toolName'], 'NEWSLETTER-THEMA': A.get('newsletterUeber', '')}
    platz.update(A.get('impressum', {})); platz.update(A.get('datenschutz', {}))
    for f in sorted((drop / 'seiten').glob('*.html')):
        h = set_block(f.read_text(encoding='utf-8'), 'SEITE', seite)
        h = fill(h, platz)
        name = dl_name if f.name == 'download.html' else f.name
        (web / name).write_text(h, encoding='utf-8')
    # Screenshot und Animations-Bilder des Tools in der Markenfarbe
    # (Vorlagen *-schluessel.png wurden mit der Schlüsselfarbe #00FF00 aufgenommen)
    for vorlage in sorted((drop / 'seiten').glob('*-schluessel.png')):
        umfaerben(vorlage, web / vorlage.name.replace('-schluessel', ''), farbe)

    if A.get('foto'):
        fp = antw_pfad.parent / A['foto']
        if fp.exists():
            ziel_foto = web / Path(A['foto']).name
            try:   # Foto klein halten (Netlify-Volumen, Ladezeit)
                from PIL import Image
                im = Image.open(fp); im.thumbnail((600, 600))
                if im.mode not in ('RGB', 'L'):
                    im = im.convert('RGB')
                ziel_foto = ziel_foto.with_suffix('.jpg')
                im.save(ziel_foto, 'JPEG', quality=82, optimize=True)
                if ziel_foto.name != Path(A['foto']).name:
                    for h in web.glob('*.html'):
                        h.write_text(h.read_text(encoding='utf-8').replace(js(A['foto']), js(ziel_foto.name)), encoding='utf-8')
            except Exception:
                shutil.copy(fp, ziel_foto)
            if ziel_foto.stat().st_size > 300_000:
                print('WARNUNG: Foto ist größer als 300 KB, bitte verkleinern.')

    # 4. offene Platzhalter melden
    offen = []
    for f in sorted(web.glob('*.html')):
        for i, line in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
            for m in re.findall(r'\[\[[^\]]+\]\]', line):
                offen.append(f'{f.name}:{i}: {m}')
    (ziel / 'offene-punkte.txt').write_text('\n'.join(offen) + '\n', encoding='utf-8')
    print(json.dumps({'tool': str(ziel / tool_datei), 'website': str(web), 'zip': zip_name,
                      'downloadSeite': dl_name, 'offenePunkte': len(offen)}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
