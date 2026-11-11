# AuTeiZu – Condoo-Version

Aufbereitete Fassung des Exports in `auteizu-website/` für den Condoo-Website-Builder (GrapesJS).

- `pages/*.html` – Body-HTML je Seite (aus der gerenderten React-App, Design-Klassen erhalten). Dateiname = Condoo-Pfad, `__` steht für `/`.
- `meta.json` – Seitenname, Pfad, SEO-Titel und -Beschreibung je Seite.
- `head.html` – globaler Kopfbereich: komplettes CSS als `<style>`, Favicon, Theme-Farbe.
- `site.css` – dasselbe CSS als Datei.
- `site.js` – globales JS: Mobilmenü, Suche, Ratgeber-Filter, Reifen-Check, Einbindung der Condoo-Formulare (Newsletter / Kontakt).
- Bilder liegen in der Condoo-Mediathek (`auteizu-image-1..5.webp`).
