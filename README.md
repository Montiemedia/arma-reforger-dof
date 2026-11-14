# Dynamic Operations Framework (DOF)

**Arma Reforger | Enfusion / Enforce Script | Multiplayer | Vanilla-first**

DOF ist ein geplantes modulares Framework für dynamische, serverautoritär verwaltete Koop-Missionen. Ein berechtigter Missionsleiter soll über eine verständliche Oberfläche Aufträge, Ziele, Einheiten, Verstärkungen, Zonen und Missionsparameter verwalten können.

> **Projektstand: Planung / Repository-Grundgerüst.** Dieses Repository enthält derzeit **keine lauffähige Mission** und **keinen kompilierten oder multiplayergetesteten Enforce-Code**.

## Projektziele

- Dynamische Aufträge mit Voraussetzungen, Teilzielen, Erfolg, Fehlschlag und Folgewirkungen
- Kontrollierte Anpassung an eingesetzte Spieler und die Missionslage
- Serverautoritärer Missionszustand mit Berechtigungsprüfung jeder administrativen Aktion
- Unabhängigkeit von bestimmter Karte, Fraktion und optionalen Workshop-Mods im Kernsystem
- Unterstützung von Listen- und Dedicated Servern (zu testen)
- Wiederverwendbare Szenario-Konfigurationen und nachvollziehbares Diagnoseprotokoll

## Ausgangsannahmen

| Parameter | Stand |
| --- | --- |
| Reforger-Version | Noch zu ermitteln |
| Zielsystem | PC / Enfusion Workbench, vorbehaltlich Bestätigung |
| Server | Listen- und Dedicated Server |
| Missionsbasis | Noch offen; Game Master und Scenario Framework evaluieren |
| Karte | Referenzkarte für Tests noch festzulegen; Kern soll kartenunabhängig sein |
| Fraktionen | Vanilla zum Testen; weitere Fraktionen optional |
| Pflichtmods | Keine außer Reforger-Basisinhalten im Kern geplant |

## Entwicklungsstufen

1. **0.1 – Fundament:** Editor-Referenzszenario, gesicherter Auftragslebenszyklus, reproduzierbarer Testablauf.
2. **0.2 – Director:** Serverautoritärer Zustandsmanager und replizierte Aufgabeninformationen.
3. **0.3 – Verwaltung:** Rollen, abgesicherte RPCs und Host-Menüs.
4. **0.4 – Dynamik:** KI-/Ressourcenbudget, Verstärkungen, Ereignisse und Auftragsverkettung.
5. **0.5 – Multiplayer-Abnahme:** Lasttests, Join-in-Progress, Fehlertoleranz und Bereinigung.

Siehe [Entwicklungsplan](docs/IMPLEMENTIERUNGSPLAN.md), [Architektur](docs/ARCHITEKTUR.md) und [Testplan](docs/TESTPLAN.md).

## Entwicklung und Test

Die Workbench-Projektdateien, Prefabs und Szenario-Welt müssen mit der tatsächlich installierten Arma-Reforger-Tools-Version angelegt und validiert werden. Keine `.ent`- oder `.conf`-Datei wird als funktionsfähig ausgegeben, solange sie nicht in dieser Umgebung erzeugt und geladen wurde.

**Wichtig:** Die in Workbench erzeugten Ressourcenmetadaten (`.meta`) gehören grundsätzlich zur Versionsverwaltung. Sie dürfen nicht pauschal ignoriert werden.

## Beiträge und Änderungsprozess

Neue Funktionen in `feature/*`-Branches entwickeln, über Pull Requests prüfen und erst danach nach `main` übernehmen. Ungeprüfte Engine-API-Aufrufe als solche dokumentieren. Siehe [GitHub-Workflow](docs/GITHUB_WORKFLOW.md).

## Lizenz

**Noch keine Open-Source-Lizenz vergeben.** Bis eine ausdrückliche Lizenz ausgewählt und hinzugefügt wird, gelten die normalen urheberrechtlichen Beschränkungen. Die öffentliche Sichtbarkeit allein ist keine Nutzungslizenz.
