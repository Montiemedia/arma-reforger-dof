# GitHub-Workflow

- `main`: dokumentierter Stand, keine ungeprüften Behauptungen über Spielbarkeit.
- `feature/*`: voneinander getrennte Arbeiten (z.B. `feature/task-state-machine`).
- `fix/*`: Fehlerkorrekturen.
- Pull Request mit Motivation, Dateiliste, Teststand und bekannten Einschränkungen.
- Issues für Engine-Fragen, Aufgaben, Bugs und Dokumentationsbedarf.
- Tags/Releases erst nach dokumentierter Abnahme.

## Empfohlene erste Issues

1. Reforger-/Workbench-Version und Game-Mode-Kompatibilität bestimmen.
2. Minimalen Szenario-Prototyp mit drei Aufträgen in Workbench anlegen.
3. Auftragszustandsmaschine mit Revisionen implementieren und testen.
4. Listen- und Dedicated-Server-Synchronisierung verifizieren.
5. Administrative Identitäts-/Berechtigungsprüfung konzipieren.

## Dateien

Workbench-Ressourcen und notwendige `.meta`-Dateien versionieren. Lokale Logs, Editor-Caches und persönliche Einstellungen nicht versionieren. Zugangsdaten, Server-Tokens oder private Konfigurationen niemals committen.
