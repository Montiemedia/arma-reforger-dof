# DOF – Architekturentwurf

Status: Entwurf, nicht implementiert oder getestet.

## Leitprinzipien

1. **Serverautorität:** Nur die autoritative Serverinstanz darf verbindliche Missionszustände, Aufträge und Spawns ändern. Das gilt für Listen- wie Dedicated Server.
2. **Trennung:** Missionsregeln sind unabhängig von Kartenpositionen, Fraktionen, konkreten Prefabs und UI.
3. **Berechtigungen:** Jede administrative Aktion benötigt eine serverseitig bestätigte Identität und Rolle. Vom Client gemeldete Spieler-IDs gelten nicht als Beleg.
4. **Deterministische Zustandsänderung:** Revisionen, Ereignis-IDs und gültige Zustandsübergänge verhindern widersprüchliche Änderungen und doppelte Verarbeitung.
5. **Explizite Limits:** Spawns, Gruppen, Fahrzeuge, aktive Aufträge und Ereignisse unterliegen konfigurierbaren Obergrenzen.

## Geplante Module (PROJEKTNAMEN, KEINE ENGINE-APIs)

| Modul | Aufgabe |
| --- | --- |
| `DOF_MissionDirector` | Serverseitige Koordination und Zustandsverwaltung |
| `DOF_TaskManager` | Aufträge, Teilziele, Voraussetzungen und Abschluss |
| `DOF_ScalePolicy` | Soll-Budget nach Spielerzahl und Missionslage |
| `DOF_SpawnManager` | Spawnprüfung, Objektregistrierung, Aufräumen |
| `DOF_ZoneManager` | Missionsräume und Zonenbedingungen |
| `DOF_EventManager` | Ereignisregeln, Idempotenz, Folgewirkungen |
| `DOF_AccessControl` | Rollen und Befehlsberechtigungen |
| `DOF_AdminUI` | Bedienung; keine eigene Entscheidungsautorität |
| `DOF_Diagnostics` | Strukturierte Meldungen und Fehlercodes |

## Auftragszustände

`PLANNED -> AVAILABLE -> ACTIVE -> SUCCEEDED | FAILED | CANCELLED`

Ein aktiver Auftrag darf außerdem `PAUSED` erreichen und wieder auf `ACTIVE` wechseln. Abschließende Zustände sind irreversibel; Korrekturen erfolgen über eine ausdrücklich definierte neue Revision/einen neuen Auftrag, nicht durch stilles Zurücksetzen.

## Auftragsarten

Sichern, Aufklären, Bergen, Zerstören, Eskortieren, Verteidigen und Evakuieren. Jeder Typ erhält eigene Sensoren beziehungsweise überprüfbare Erfolgsbedingungen; Zustände, Abhängigkeiten und Folgewirkungen bleiben generisch.

## Replikation (zu verifizieren)

Client sendet administrativen Befehl -> autorisierter RPC-Endpunkt -> Prüfung der tatsächlichen Absenderidentität -> Berechtigung -> Parameter -> Objekt-Revision -> Voraussetzungen -> Ressourcen- und Performancegrenzen -> atomare Zustandsänderung -> selektive Replikation und Audit-Eintrag.

Vor Implementierung sind die konkret gewählten Reforger-Komponenten, Ownership-/RPC-Regeln und Game-Mode-Kompatibilität in der installierten Version nachzuprüfen.

## Karten-/Modoffenheit

Der Kern speichert logische Zonen-IDs und referenziert Szenario-Ressourcen über konfigurierbare Adapter. Mod-Prefabs sind optional. Fehlende Add-ons müssen zu verständlichen Fehlern führen und dürfen keine unkontrollierten Spawnversuche auslösen.
