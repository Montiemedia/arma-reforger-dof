# DOF – Implementierungsplan

## Phase 0: Voraussetzungen (offen)

- [ ] Installierte Reforger-Version und Enfusion-Workbench-Version dokumentieren
- [ ] Game-Master-Spielmodus und Scenario-Framework-Bausteine im Projekt prüfen
- [ ] Referenzkarte, Vanilla-Fraktionen und Server-Testumgebungen festlegen
- [ ] Verwendete Engine-Klassen und Callback-Signaturen anhand installierter Skriptquellen verifizieren

## Phase 1: Szenarioprototyp (0.1)

- [ ] Minimale Workbench-Subscene erzeugen
- [ ] Ein funktionierender Spawn-/Bereitstellungsbereich
- [ ] Auftragskette Annähern -> Sichern/Säubern -> Verteidigen
- [ ] Erfolg, Fehlschlag und Abbruch validieren
- [ ] Reproduzierbare lokale Testanleitung dokumentieren

**Abnahme:** Alle Phasen sind spielbar; keine Doppelaktivierung; sauberer Abschluss. Erst nach Workbench-Test als spielbar bezeichnen.

## Phase 2: Zustandsmanager (0.2)

- [ ] Aufträge unabhängig von Engine-Entities modellieren
- [ ] Zustandsübergänge inklusive Revisionen und Ereignis-IDs
- [ ] Serverseitige Zählung tatsächlich eingesetzter Spieler
- [ ] Join-in-Progress-Synchronisierung

**Abnahme:** Mehrere Clients sehen denselben Missionszustand; konkurrierende Änderungsversuche werden zuverlässig behandelt.

## Phase 3: Rollen und Bedienung (0.3)

- [ ] Authentifizierte Rollen Serveradmin, Missionsbauer, Lagedarsteller
- [ ] Gesicherter Befehlsendpunkt mit Absender-/Rechteprüfung
- [ ] Übersicht für Aufträge, Zonen, Einheiten und Ressourcen
- [ ] Änderung, Pause, Aktivierung und kontrolliertes Entfernen

## Phase 4: Dynamik und Performance (0.4)

- [ ] Skalierungs-Hysterese und stabile Teilnehmerzahl
- [ ] Verstärkungsreserve und Spawnwarteschlange
- [ ] Alarm-/Eskalationsstufen
- [ ] Aufräumlogik und Limits
- [ ] Strukturierte Diagnose

## Phase 5: Multiplayer-Abnahme (0.5)

- [ ] Listen-Server und Dedicated Server
- [ ] Join-in-Progress / Reconnect
- [ ] Nicht berechtigte RPC-Aufrufe
- [ ] 1/4/8/16/32 Spieler nur soweit tatsächlich testbar
- [ ] Lastmessung und Regression
