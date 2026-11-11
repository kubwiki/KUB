# AuTeiZu – Umzug von Manus nach Condoo

Dieser Ordner enthält die **komplette Webseite AuTeiZu** als eigenständigen, statischen Export
der Manus-Seite `auteizu-asnthnmr.manus.space` (Stand: 11.11.2026).

Die Seite läuft **ohne Manus**: Alle Manus-Skripte (Editor, Analytics, „Made with Manus“-Badge)
wurden entfernt, Bilder und Artikeldaten liegen lokal. Getestet: alle Seiten laden fehlerfrei,
der Reifen-Check funktioniert, keine externen Verbindungen nötig.

## Inhalt

| Pfad | Seite |
|---|---|
| `/` | Startseite |
| `/ratgeber/` | Ratgeber-Übersicht (mit Suche) |
| `/reifen-raeder/` | Kategorie Reifen & Räder |
| `/zubehoer-nachruestung/` | Kategorie Zubehör & Nachrüstung |
| `/pflege-wartung/` | Kategorie Pflege & Wartung |
| `/reifen-check/` | Interaktiver Reifen-Check |
| `/reifen-raeder/ganzjahresreifen-oder-sommer-und-winterreifen/` | Artikel |
| `/reifen-raeder/reifengroesse-225-45-r17/` | Artikel |
| `/zubehoer-nachruestung/anhaengerkupplung-nachruesten-kosten-und-moeglichkeiten/` | Artikel |
| `/zubehoer-nachruestung/dashcam-kaufen-was-brauche-ich-wirklich/` | Artikel |
| `/pflege-wartung/autopflege-grundausstattung/` | Artikel |
| `/ueber-auteizu/`, `/autor/willi-kilian/` | Über uns / Autor |
| `/kontakt/`, `/impressum/`, `/datenschutz/`, `/affiliate-hinweis/`, `/cookie-einstellungen/` | Rechtliches & Kontakt |

Technik: `assets/` (App-Code + CSS), `images/` (5 Bilder), `api/trpc/content.published`
(Artikeldaten als statische Datei, ersetzt die Manus-Datenbank), `404.html` (Fallback für die Navigation).

## In Condoo übernehmen

Condoo-Seiten werden im Website-/Funnel-Builder angelegt. Für diese Seite gibt es zwei Wege:

### Weg A (empfohlen): Dateien hochladen und Domain verbinden
Wenn Condoo das Hochladen eigener HTML-Dateien bzw. eines ZIP-Archivs erlaubt:
1. `auteizu-website.zip` (bzw. den Inhalt dieses Ordners) hochladen – die Ordnerstruktur muss erhalten bleiben.
2. Unter Domains die eigene Domain (z. B. auteizu.de) verbinden.

Falls Condoo das **nicht** unterstützt, kann der Ordner 1:1 auf jedem statischen Hosting
(z. B. GitHub Pages, Netlify, IONOS/Strato-Webspace per FTP) liegen. Condoo wird dann für
Kontakte, Newsletter und Formulare genutzt (siehe „Nacharbeiten“).

### Weg B: Seiten im Condoo-Builder nachbauen
Texte und Bilder aus diesem Ordner seitenweise in den Condoo-Builder übernehmen
(Bilder liegen in `images/`). Das Design muss dabei mit Condoo-Elementen nachgebaut werden;
der Reifen-Check lässt sich so nur eingeschränkt übernehmen.

## Nacharbeiten nach dem Umzug

- **Newsletter-Formular & Kontaktformular**: speichern aktuell nichts (wie schon bei Manus:
  „Noch kein Versanddienst verbunden“). Am besten durch ein Condoo-Formular ersetzen,
  damit Anmeldungen direkt als Kontakte in Condoo landen.
- **Canonical-/OG-URL**: wurden entfernt, weil sie auf die Manus-Adresse zeigten.
  Nach Festlegung der finalen Domain wieder ergänzen.
- **Manus-Seite** erst abschalten, wenn die neue Seite unter der eigenen Domain läuft.

## Lokal ansehen

```bash
cd auteizu-website && python3 -m http.server 8000
```
Dann http://localhost:8000 im Browser öffnen.
