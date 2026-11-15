# START HIER: Dein [[TOOLNAME]] als Freebie

Alles in diesem Ordner ist schon mit deinem Namen, deiner Farbe und deinen Daten ausgefüllt. Geh die Schritte der Reihe nach durch. Was Claude schon erledigt hat, ist abgehakt (☑).

Hängst du irgendwo? Schreib Claude einfach im Chat, was du siehst. Du brauchst dafür nichts anderes als das Chatfenster und deinen Browser.

## ☐ Schritt 1: Selbst testen (2 Minuten)
Doppelklick auf `[[TOOLDATEI]]` hier im Ordner. Öffnet sie sich nicht in Chrome, mach einen Rechtsklick, wähl "Öffnen mit" und dann "Google Chrome". Mach eine kurze Testaufnahme, dann weißt du, wie es sich für deine Abonnenten anfühlt.

## ☐ Schritt 2: Datenschutzerklärung prüfen (10 Minuten)
`website/datenschutz.html` ist ein **Entwurf**, passend zu den Diensten, die du nutzt. Gleich ihn mit einem Generator ab, z.B. eRecht24 oder Datenschutz-Generator.de, oder lass ihn prüfen. An fehlerhaften Datenschutzerklärungen können Abmahnungen hängen.
Möchtest du etwas ändern? Kopier den Text aus dem Generator in den Chat und sag Claude: "Übernimm das in meine Datenschutzerklärung."

## ☐ Schritt 3: Anmeldeformular
[[ERLEDIGT ODER OFFEN: Ist dein Formular aus [[E-MAIL-TOOL]] schon eingebaut, ist das hier abgehakt. Wenn nicht: Kopier den Formular-Code aus [[E-MAIL-TOOL]] in den Chat und sag Claude: "Bau das in meine Opt-in-Seite ein." Weißt du nicht, wo der Code ist? Frag Claude, es erklärt es dir für [[E-MAIL-TOOL]].]]

## ☐ Schritt 4: Seite online stellen
[[ERLEDIGT ODER OFFEN: Deine Seite ist online unter [[ADRESSE]]. Wenn nicht: Sag Claude im Chat "Stell meine Seite bei Netlify online." Ist Netlify nicht verbunden, öffnet Claude dir den Ordner, und du ziehst den Ordner **website** auf app.netlify.com/drop.]]

Später etwas geändert? Sag Claude "Lade meine Seite neu hoch". Jedes Hochladen heißt bei Netlify "Deploy" und kostet im kostenlosen Plan 15 von 300 Credits im Monat. Ein- bis zweimal im Monat ist völlig okay. Lade keine Videos oder großen Bilder hoch.

## ☐ Schritt 5: Weiterleitungen im Mail-Tool eintragen
In [[E-MAIL-TOOL]] bei deinem Formular eintragen:
- **Seite nach der Anmeldung:** `[[ADRESSE]]/bestaetigung.html`
- **Seite nach der Bestätigung (Double-Opt-in):** `[[ADRESSE]]/[[DOWNLOADSEITE]]`
- So findest du die Stelle in [[E-MAIL-TOOL]]: [[HINWEIS JE TOOL]]

Der Name der Download-Seite ist absichtlich schwer zu erraten, damit niemand am Formular vorbei an den Download kommt. Teile diesen Link nirgends öffentlich.

## ☐ Schritt 6: Mails einrichten
Leg in [[E-MAIL-TOOL]] eine Automatisierung an, die startet, sobald jemand bestätigt hat. Die fertigen Texte stehen in `mails.md`:
- Mail 1 sofort, Mail 2 nach 2 Tagen, Mail 3 nach 4 Tagen, Mail 4 nach 6 Tagen.
- Der Download-Link in Mail 1 ist schon eingesetzt: `[[ADRESSE]]/[[ZIP]]`
- Impressum und Abmeldelink stehen bei den meisten Mail-Tools automatisch im Footer. Prüf das einmal.

## ☐ Schritt 7: Komplett-Test
Trag dich mit einer zweiten E-Mail-Adresse selbst ein, bestätige, lade das Tool herunter und öffne es. Kommt alles an, ist dein Freebie live. 🎉

[[NUR WENN MANYCHAT: ## ☐ Schritt 8: Instagram
Richte die Automatisierung aus `manychat.md` in ManyChat ein. Der Link in der DM führt auf deine Opt-in-Seite, nicht direkt zum Download. Ergänze deine Datenschutzerklärung um ManyChat und Instagram. Sag dafür Claude einfach: "Ergänze ManyChat in meiner Datenschutzerklärung."]]
