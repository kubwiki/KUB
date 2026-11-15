# START HIER: Dein Willis Screen Recorder als Freebie

Alles in diesem Ordner ist schon mit deinem Namen, deiner Farbe und deinen Daten ausgefüllt. Geh die Schritte der Reihe nach durch. Was Claude schon erledigt hat, ist abgehakt (☑).

Hängst du irgendwo? Schreib Claude einfach im Chat, was du siehst. Du brauchst dafür nichts anderes als das Chatfenster und deinen Browser.

## ☐ Schritt 1: Selbst testen (2 Minuten)
Doppelklick auf `willis-screen-recorder.html` hier im Ordner. Öffnet sie sich nicht in Chrome, mach einen Rechtsklick, wähl "Öffnen mit" und dann "Google Chrome". Mach eine kurze Testaufnahme, dann weißt du, wie es sich für deine Abonnenten anfühlt.

## ☐ Schritt 2: Datenschutzerklärung prüfen (10 Minuten)
`website/datenschutz.html` ist ein **Entwurf**, passend zu den Diensten, die du nutzt (Netlify und Quentn). Gleich ihn mit einem Generator ab, z.B. eRecht24 oder Datenschutz-Generator.de, oder lass ihn prüfen. An fehlerhaften Datenschutzerklärungen können Abmahnungen hängen.
Möchtest du etwas ändern? Kopier den Text aus dem Generator in den Chat und sag Claude: "Übernimm das in meine Datenschutzerklärung."

## ☑ Schritt 3: Anmeldeformular
Dein Formular aus Quentn (Formular 6894) ist schon in deine Opt-in-Seite eingebaut.

## ☑ Schritt 4: Seite online stellen
Deine Seite ist online unter **https://willis-screen-recorder.netlify.app**

Später etwas geändert? Sag Claude "Lade meine Seite neu hoch". Jedes Hochladen heißt bei Netlify "Deploy" und kostet im kostenlosen Plan 15 von 300 Credits im Monat. Ein- bis zweimal im Monat ist völlig okay. Lade keine Videos oder großen Bilder hoch.

## ☐ Schritt 5: Weiterleitungen in Quentn eintragen
In Quentn bei deinem Formular eintragen:
- **Seite nach der Anmeldung:** `https://willis-screen-recorder.netlify.app/bestaetigung.html`
- **Seite nach der Bestätigung (Double-Opt-in):** `https://willis-screen-recorder.netlify.app/download-9b80af54.html`
- So findest du die Stelle in Quentn: Öffne dein Formular bzw. die Opt-in-Einstellungen und trag dort die Danke-Seite (nach der Anmeldung) und die Seite nach der Bestätigung ein. Die Menü-Bezeichnungen können leicht abweichen.

Der Name der Download-Seite ist absichtlich schwer zu erraten, damit niemand am Formular vorbei an den Download kommt. Teile diesen Link nirgends öffentlich.

## ☐ Schritt 6: Mails einrichten
Leg in Quentn eine Automatisierung an, die startet, sobald jemand bestätigt hat. Die fertigen Texte stehen in `mails.md`:
- Mail 1 sofort, Mail 2 nach 2 Tagen, Mail 3 nach 4 Tagen, Mail 4 nach 6 Tagen.
- Der Download-Link in Mail 1 ist schon eingesetzt: `https://willis-screen-recorder.netlify.app/willis-screen-recorder.zip`
- `{{Vorname}}` in den Mails ersetzt du in Quentn über die Platzhalter-Funktion durch das Feld Vorname.
- Impressum und Abmeldelink stehen bei den meisten Mail-Tools automatisch im Footer. Prüf das einmal.

## ☐ Schritt 7: Komplett-Test
Trag dich mit einer zweiten E-Mail-Adresse selbst ein, bestätige, lade das Tool herunter und öffne es. Kommt alles an, ist dein Freebie live. 🎉
