# DOF – Test- und Abnahmeplan

Alle Testergebnisse sind bis zur Durchführung **OFFEN**. Die folgenden Werte sind Testziele und keine nachgewiesenen Leistungswerte.

| ID | Test | Erwartung | Status |
| --- | --- | --- | --- |
| T01 | Editor-Szenario laden | Keine fehlenden Pflichtressourcen | OFFEN |
| T02 | Skripte kompilieren | Keine Skriptfehler | OFFEN |
| T03 | Bereitstellung | Spieler spawnt korrekt | OFFEN |
| T04 | Auftragskette | Aufgaben erscheinen in korrekter Reihenfolge | OFFEN |
| T05 | Erfolg/Fehlschlag | Genau ein Abschlussereignis | OFFEN |
| T06 | Wiederholter Start | Keine doppelte Director-Initialisierung | OFFEN |
| T07 | Listen-Server | Konsistenter Zustand bei zwei Clients | OFFEN |
| T08 | Dedicated Server | Funktion ohne lokalen Host-Spieler | OFFEN |
| T09 | Join-in-Progress | Nachzügler erhält gültigen aktuellen Zustand | OFFEN |
| T10 | Unberechtigter Verwaltungsbefehl | Serverseitig abgelehnt und protokolliert | OFFEN |
| T11 | Gleichzeitige Änderung | Veraltete Revision abgelehnt | OFFEN |
| T12 | Spawnlimit | Überzählige Anforderungen abgelehnt oder verzögert | OFFEN |
| T13 | Missionsabbruch | Warteschlangen und Registrierungen bereinigt | OFFEN |
| T14 | Hohe Last | Keine ungebremste Objekt-/Ereignisvermehrung | OFFEN |

## Testprotokoll

Für jeden Test dokumentieren: Reforger-Version, Plattform, Karten-/Modliste, Servertyp, Spielerzahl, Zeitpunkt, Serverlog, Clientlog, erwartetes Ergebnis, beobachtetes Ergebnis, Fehlerreferenz.

## Release-Regel

Kein Release als „spielbar“ vor bestandenem T01–T05. Kein Release als „multiplayerfähig“ vor dokumentierten T07–T09. Sicherheit der Administrationsbefehle nur nach T10–T11 bewerten.
