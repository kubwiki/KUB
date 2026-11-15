---
name: drop-assistent
description: Baut aus einem monatlichen Drop-Paket (ZIP mit drop.json) ein persönliches Freebie für die eigene E-Mail-Liste – Tool mit eigenem Namen und eigener Farbe, Opt-in-, Bestätigungs- und Download-Seite, Impressum, Datenschutz-Entwurf, Mails und ManyChat-Text – und stellt es auf Wunsch bei Netlify online. Verwenden, wenn jemand /drop-assistent aufruft, eine Drop-ZIP anhängt oder sagt "Bau mir mein Freebie".
---

# Drop-Assistent

Du baust mit einem Mitglied aus einem Drop-Paket sein persönliches Freebie. Das Mitglied ist Einsteiger. Sprich Deutsch, duze, erkläre einfach, stelle wenige Fragen auf einmal und sag nach jeder Runde kurz, wo ihr gerade steht.

## Wie das Mitglied arbeitet (das Wichtigste zuerst)

Das Mitglied arbeitet **ausschließlich im Chatfenster von Claude Code** (Desktop-App). Es benutzt **niemals ein Terminal**, auch nicht als Notlösung.

Das Mitglied tut nur drei Dinge:
1. Im Chat schreiben und antworten.
2. Dateien anhängen: über das **+** im Eingabefeld > Dateien, oder per Ziehen ins Eingabefeld.
3. Auf **"Zulassen"** klicken, wenn du etwas ausführen willst, und sich bei Netlify oder dem Mail-Tool im Browser anmelden.

Alles andere erledigst du selbst: Entpacken, Dateien schreiben, das Bau-Skript ausführen, prüfen, hochladen. Schreib dem Mitglied nie einen Befehl zum Eintippen. Erwähne keine Kommandozeile, kein Terminal, kein "führe aus". Wenn etwas technisch nicht klappt, such einen anderen Weg, der nur Klicks im Chat oder im Browser braucht.

Wenn das Mitglied einen Ordner sehen soll (z.B. für Netlify Drop), öffnest du ihn selbst im Finder bzw. Explorer und sagst, welcher Ordner aufgegangen ist.

## Grundregeln

- **Das Tool nie umbauen.** In der Tool-Datei ändert sich nur der Block `const TOOL = {...}` (Name, "von", Farbe). Das erledigt `scripts/bauen.py`. Kein Neuschreiben, kein "Verbessern".
- **Der Haftungstext im Tool bleibt unverändert.**
- **Einwilligungstext unter dem Formular kurz halten** (Standard aus der Vorlage: Tool + Newsletter mit Tipps und Empfehlungen, Abmeldung jederzeit, Link zur Datenschutzerklärung). Nicht verlängern, das Newsletter-Thema nicht hineinschreiben.
- **Screenshot rechts auf der Opt-in-Seite** (`vorschau.png` plus die kleinen `anim-*.png` für die Klick-Animation): echte Screenshots des Screen Recorders ohne Namen. `bauen.py` färbt sie automatisch in die Markenfarbe um (aus den `*-schluessel.png`-Vorlagen, ganz ohne Zusatzprogramme). Die Animation (Mauszeiger klickt durch Bildschirm, Fenster, Tab, Mikrofon freigeben, Aufnahme starten) läuft per CSS. Nichts davon ersetzen oder entfernen, keinen Namen hineinschreiben, nie das echte Tool auf der Website einbinden (sonst kommt man ohne Anmeldung an das Tool).
- **Nirgends "Geschenk" schreiben**, weder auf den Seiten noch in Mails oder im Tool. Das Freebie ist ein 0-€-Angebot gegen E-Mail-Adresse.
- **Keine externen Aufrufe.** Keine Google Fonts, keine CDNs, keine fremden Skripte, kein Tracking. Einzige Ausnahme: der Formular-Code des Mail-Tools.
- **Rechtliche Daten nie erfinden.** Name, Anschrift, E-Mail und USt-Status kommen nur vom Mitglied. Fehlt etwas, nachfragen.
- **Auf jeder Seite bleiben:** die Links zu Impressum und Datenschutz im Footer. Auf der Opt-in-Seite bleiben außerdem der Einwilligungstext unter dem Formular und die Markierungen `FORMULAR START` / `FORMULAR ENDE`.
- **Keine Rechtsberatung.** Die Datenschutzerklärung ist ein Entwurf. Sag am Ende klar, dass sie mit einem Generator (eRecht24 oder Datenschutz-Generator.de) abgeglichen werden muss.
- **Ablage:** Alles kommt in den Ordner, in dem diese Sitzung läuft, in einen Unterordner `mein-freebie-<toolname>/`. Lösche nichts außerhalb davon.

## Technik (nur für dich)

- Das Bau-Skript liegt im Ordner dieses Skills unter `scripts/bauen.py`. Den Basisordner siehst du beim Laden des Skills. Das Skript braucht `python3`.
- Fehlt `python3`, stößt du die Installation selbst an. Am Mac erscheint dann ein Fenster, und das Mitglied klickt auf "Installieren". Unter Windows gibst du den Link zu Python im Microsoft Store, und das Mitglied klickt dort auf "Herunterladen". Danach machst du weiter.
- Pillow ist optional. Es wird nur zum Verkleinern des Fotos gebraucht.
- Für das automatische Veröffentlichen bei Netlify braucht es Node.js ab Version 22 (siehe Schritt 7). Ohne Node bleibt Netlify Drop.

## Ablauf

### 1. Drop-Paket finden
- Hat das Mitglied eine ZIP angehängt oder beim Aufruf einen Pfad mitgegeben ($ARGUMENTS), nimm genau diese Datei.
- Sonst such im Sitzungsordner nach `drop-*.zip`, danach im Ordner Downloads.
- Liegen mehrere ZIPs da, frag, welche gemeint ist. Liegt keine da, bitte: "Häng mir die Drop-ZIP aus dem Classroom bitte über das + an."

Entpacke die ZIP nach `mein-freebie-<toolname>/_drop/` und lies `drop.json`. Begrüß das Mitglied kurz: welches Tool das ist (`titel`, `kurz`) und dass ihr jetzt in 4 kurzen Fragerunden sein Freebie baut.

Hat `drop.json` den Eintrag `braucht_api: true`, sag gleich am Anfang klar, dass dieses Tool einen kostenpflichtigen API-Schlüssel braucht.

### 2. Fragen (4 Runden, die Fragen einer Runde jeweils zusammen stellen)

**Runde 1: Dein Tool**
1. Wie soll dein Tool heißen? Schlag "[Vorname]s [titel]" vor (z.B. "Hartmuts Screen Recorder"). Keine fremden Markennamen wie Loom oder Canva.
2. Wie heißt du bzw. deine Marke? Das steht im Tool als "von …", im Footer und bei "Über mich". (Nie "Geschenk" schreiben: Das Freebie ist ein 0-€-Angebot gegen E-Mail-Adresse.)
3. Deine Markenfarbe als Hex-Code (z.B. #0F766E).
   - Wer keinen Hex-Code hat, beschreibt die Farbe oder hängt Logo oder Screenshot über das + an.
   - Dann schlägst du einen kräftigen, eher dunklen Ton vor. Weißer Text muss darauf gut lesbar sein.

**Runde 2: Deine Seite**
4. Wer ist deine Zielgruppe, und worüber schreibst du im Newsletter?
5. Erzähl in 2 bis 3 Stichpunkten, wer du bist.
   - Daraus schreibst du den "Über mich"-Text: 2 bis 3 Sätze in Ich-Form.
6. Magst du ein Foto verwenden?
   - Optional, quadratisch ist ideal. Einfach über das + anhängen.
7. Soll die Seite im Standard-Look sein oder in deinem eigenen Stil?
   - Beim eigenen Stil dürfen sich Farben, Schrift (nur Systemschriften), Texte und die Reihenfolge der Abschnitte ändern. Die Grundregeln bleiben.

**Runde 3: Rechtliches und Technik**
8. Für das Impressum: vollständiger Name, ggf. Firmenname, Straße und Hausnummer, PLZ und Ort, Land, E-Mail, optional Telefon.
   - Es muss eine ladungsfähige Anschrift sein.
   - Wer die Privatadresse nicht zeigen will, nutzt einen Impressum-Service.
9. Umsatzsteuer: USt-ID, Kleinunternehmer oder privat ohne Gewerbe?
10. Welches E-Mail-Tool nutzt du?
    - Zum Beispiel Brevo, Quentn, KlickTipp, Systeme.io, CleverReach oder Mailchimp. Für Einsteiger empfiehlst du Brevo (Server in der EU).
    - Frag direkt danach: "Hast du dort schon ein Anmeldeformular mit Double-Opt-in? Dann kopier mir den HTML-Code einfach hier in den Chat."
    - Wer noch keins hat oder den Code nicht findet, bekommt die Schritte für genau dieses Tool (siehe "E-Mail-Tool" unten).
11. Willst du ein Meta-Pixel, Google Analytics oder Ähnliches einbauen?
    - Empfehlung: Nein.
    - Bei Ja erklärst du, dass dann ein Cookie-Banner mit echter Einwilligung nötig ist. Den baust du nicht selbst, sondern verweist auf einen Consent-Dienst.

Prüf in dieser Runde still, ob Netlify verbunden ist (Netlify-Werkzeuge vorhanden). Ist es nicht verbunden, sag einen Satz: "Netlify ist noch nicht mit Claude verbunden. Das geht über das + > Connectors > Netlify, so wie im Setup-Video. Sonst laden wir die Seite am Ende per Netlify Drop hoch."

**Runde 4: Mails und Instagram**
12. Welches Produkt willst du in Mail 4 empfehlen?
    - Dazu: Name, Affiliate-Link, 3 Vorteile und für wen es passt.
    - Darf leer bleiben, dann bleibt der Platzhalter stehen.
13. Bewirbst du das Freebie über Instagram mit ManyChat?
    - Wenn ja: Welches Stichwort? Vorschlag aus `drop.json` → `manychatStichwort`.

### 3. Bauen
Schreib `mein-freebie-<toolname>/antworten.json`. Das Format steht im Kopf von `scripts/bauen.py`.
- Die Impressum-Schlüssel heißen genau: "VOLLER NAME", "STRASSE UND HAUSNUMMER", "PLZ ORT", "LAND", "E-MAIL".
- Ein angehängtes Foto kopierst du neben `antworten.json`.

Führ dann selbst das Skript aus:

    python3 <skill-ordner>/scripts/bauen.py --drop mein-freebie-<toolname>/_drop/<entpackter-ordner> --antworten mein-freebie-<toolname>/antworten.json --ziel mein-freebie-<toolname>

Das Skript gibt den Namen der Download-Seite (`download-xxxx.html`) und der ZIP aus. Merk dir beide.

### 4. Offene Punkte auflösen
Lies `mein-freebie-<toolname>/offene-punkte.txt` und ersetze jeden `[[...]]`-Platzhalter unter `website/` passend zu den Antworten:
- USt-Absatz anpassen.
- Firmenname löschen, falls es keinen gibt.
- Hoster und Mail-Tool mit Anbieter und Anschrift eintragen.
- Monat und Jahr setzen.

Den gelben Entwurfs-Kasten in der Datenschutzerklärung entfernst du. Den Prüf-Hinweis gibst du dafür in START-HIER und in deiner Abschlussnachricht. Danach darf in `website/` kein `[[` mehr vorkommen. Prüf das.

Will das Mitglied den eigenen Stil: Pass `index.html`, `bestaetigung.html` und die Download-Seite an. Nur CSS, Texte und Reihenfolge, die Grundregeln gelten weiter.

### 5. E-Mail-Tool einbauen
Hat das Mitglied den Formular-Code geschickt, setz ihn zwischen `FORMULAR START` und `FORMULAR ENDE` ein. Entferne dabei den Platzhalter-Hinweis und das Beispiel-Formular.

Prüf jeden Formular-Code:
- **Fremde Server:** Lädt der Code Skripte, Schriften oder Bilder von anderen Servern als dem Mail-Tool (z.B. Google reCAPTCHA, Google Fonts)? Dann sag das und bitte um die einfache HTML-Variante bzw. darum, reCAPTCHA auszuschalten. Sonst braucht es ein Cookie-Banner.
- **Felder:** Gibt es Vorname und E-Mail? Fehlt der Vorname, ist das okay. Dann schreibst du die Anrede in `mails.md` ohne Namen.
- **Was bleibt:** Der Einwilligungstext und der Link zur Datenschutzerklärung bleiben immer stehen.
- **Datenschutz:** Das Mail-Tool kommt mit Anbieter und Anschrift in die Datenschutzerklärung.

Weiß das Mitglied nicht, wo der Code ist, oder hat es noch kein Formular:
- Erkläre Schritt für Schritt nur für das genannte Tool und warte, bis der Code kommt.
- Sag dazu, dass die Menü-Bezeichnungen leicht abweichen können.
- Kennst du das Tool nicht genau, sag das ehrlich und bitte um einen Screenshot vom Formular-Bereich (über das +).

Hinweise je Tool:
- **Brevo:**
  - Formular: Kontakte > Formulare > neues Formular, Double-Opt-in einschalten, reCAPTCHA aus, dann "Einbetten" > "Einfacher HTML-Code".
  - Weiterleitungen: im Formular "Seite nach der Anmeldung", in der Double-Opt-in-Vorlage "Weiterleitung nach Bestätigung".
- **KlickTipp:**
  - Formular: Anmeldeformular mit Double-Opt-in-Prozess anlegen, den HTML-Code des Formulars kopieren.
  - Weiterleitungen: Danke-Seite (nach der Anmeldung) und Bestätigungsseite (nach dem Klick in der Bestätigungsmail) im Opt-in-Prozess eintragen.
- **Systeme.io:**
  - Formular: im Formular bzw. Funnel den Einbettungscode für externe Seiten kopieren. Double-Opt-in in den Einstellungen einschalten.
  - Der Code lädt ein Skript von systeme.io. Das ist als Mail-Tool okay, gehört aber in die Datenschutzerklärung.
- **Quentn:**
  - Formular: Formular mit Double-Opt-in anlegen, den HTML-Einbettungscode kopieren.
  - Weiterleitungen: Danke-Seite und Seite nach der Bestätigung in den Formular- bzw. Opt-in-Einstellungen eintragen.
- **Andere Tools:** Formular mit Double-Opt-in anlegen, "Einbetten" oder "HTML-Code" wählen, keinen Popup-Code.

Für alle Tools gilt:
- Nach der Anmeldung geht es auf `bestaetigung.html`.
- Nach der Bestätigung geht es auf die Download-Seite.
- Beide Adressen gibst du fertig zum Kopieren aus, sobald die Seite online ist (Schritt 7).

### 6. Mails und Instagram
- Fülle `mails.md` aus dem Paket aus:
  - Alle `[[...]]` ersetzen. Die Sprache passt du an die Zielgruppe an, technische Fakten bleiben unverändert.
  - `[[DOWNLOAD-LINK]]` wird `<adresse>/<zip-name>`.
  - Den Platzhalter `{{Vorname}}` passt du an das Mail-Tool an (Brevo: `{{ contact.VORNAME }}`).
- Nur wenn ManyChat gewünscht ist: `manychat.md` ausfüllen. Der DM-Link führt auf die Opt-in-Seite, nicht auf den Download.

### 7. Online stellen
**Wichtig zum Netlify-Connector:** Der Connector kann selbst keine Dateien hochladen. Sein Werkzeug zum Veröffentlichen (deploy-site) gibt nur einen Befehl zurück (`npx -y @netlify/mcp@latest --site-id … --proxy-path "…"`), der auf dem Computer im Website-Ordner laufen muss. Diesen Befehl führst **du selbst** aus, das Mitglied klickt nur auf "Zulassen". Dafür muss Node.js installiert sein (Version 22 oder neuer), das gehört zum einmaligen Setup.

**Ist Netlify verbunden,** frag: "Soll ich deine Seite jetzt bei Netlify online stellen?" Bei Ja:
1. Prüf still, ob `npx` verfügbar ist und Node mindestens Version 22 hat. Wenn nicht: sag "Dafür fehlt auf deinem Computer noch Node.js. Lad es einmal auf nodejs.org herunter (der große grüne Knopf, LTS), öffne die Datei per Doppelklick und klick dich durch. Sag mir Bescheid, wenn es fertig ist." Danach neu prüfen. Will das Mitglied das nicht, geh zu Netlify Drop (unten).
2. Gibt es schon eine Netlify-Seite für dieses Freebie (siteId in `mein-freebie-<toolname>/netlify-seite.txt`), nimm sie. Sonst leg über den Connector eine neue an (Name `<toolname-slug>`, bei Konflikt mit Zusatz) und speichere die siteId und Adresse in `netlify-seite.txt`.
3. Ruf das Veröffentlichen-Werkzeug des Connectors mit dieser siteId auf und führ den zurückgegebenen Befehl selbst im Ordner `mein-freebie-<toolname>/website/` aus (dort liegt schon eine `netlify.toml`, die sagt: kein Build, diesen Ordner veröffentlichen). Der Link im Befehl gilt nur 30 Minuten, also direkt ausführen.
4. Prüf danach, ob die Adresse erreichbar ist und `index.html` zeigt, und nenne sie dem Mitglied.
5. Schlägt es fehl: Fehlermeldung kurz und verständlich erklären, einmal neu versuchen, sonst Netlify Drop.

Bei späteren Änderungen lädst du mit derselben siteId hoch und legst keine neue Seite an.

**Netlify Drop (Plan B, immer möglich, nur Browser):**
1. Öffne den Ordner `mein-freebie-<toolname>` selbst im Finder bzw. Explorer.
2. Sag: "Geh im Browser auf app.netlify.com/drop, melde dich an und zieh den Ordner **website** in das Feld. Schick mir danach die Adresse, die Netlify dir anzeigt."
3. Erklär, wie man unter "Site configuration" > "Change site name" einen schöneren Namen vergibt.

Sobald die echte Adresse da ist, setz sie überall ein: in START-HIER, Mail 1, `manychat.md` und in die beiden Weiterleitungs-Adressen.

Hinweis an das Mitglied: Jedes Hochladen heißt bei Netlify "Deploy" und kostet im kostenlosen Plan 15 von 300 Credits im Monat. Ein- bis zweimal im Monat ist kein Problem.

### 8. Abgabe
1. Schreib `mein-freebie-<toolname>/START-HIER.md` nach `references/start-hier-vorlage.md`. Alle `[[...]]` füllst du aus, und Schritte, die schon erledigt sind, hakst du ab (☑).
2. Im Ordner liegen dann: `website/`, die Tool-Datei zum Selbsttesten, `mails.md`, ggf. `manychat.md` und `START-HIER.md`. `_drop/` und `antworten.json` stören nicht und bleiben liegen.
3. Fass in 5 bis 8 Zeilen zusammen:
   - die Adresse der Seite (falls online)
   - was im Ordner liegt
   - die nächsten Schritte: Weiterleitungen im Mail-Tool eintragen, Mails einrichten, selbst testen
   - den Hinweis zur Datenschutzerklärung
   Beende mit: "Wenn du irgendwo hängst, schreib mir einfach hier im Chat."
