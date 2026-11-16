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
| Missionsbasis | Scenario Framework für 0.1-Referenztest; Game-Master-Integration separat und noch ungeprüft |
| Karte | Arland-Subscene als Referenz vorhanden; alle anderen Karten noch offen |
| Fraktionen | Vanilla zum Testen; weitere Fraktionen optional |
| Pflichtmods | Keine außer Reforger-Basisinhalten im Kern geplant |

## Entwicklungsstufen

1. **0.1 – Fundament:** Editor-Referenzszenario, gesicherter Auftragslebenszyklus, reproduzierbarer Testablauf.
2. **0.2 – Director:** Serverautoritärer Zustandsmanager und replizierte Aufgabeninformationen.
3. **0.3 – Verwaltung:** Rollen, abgesicherte RPCs und Host-Menüs.
4. **0.4 – Dynamik:** KI-/Ressourcenbudget, Verstärkungen, Ereignisse und Auftragsverkettung.
5. **0.5 – Multiplayer-Abnahme:** Lasttests, Join-in-Progress, Fehlertoleranz und Bereinigung.

Siehe [Entwicklungsplan](docs/IMPLEMENTIERUNGSPLAN.md), [Architektur](docs/ARCHITEKTUR.md), [API-Verifikation](docs/API_VALIDIERUNG.md), [Workbench-Anleitung für DOF 0.1](docs/WORKBENCH_SZENARIO_0_1.md) und [Testplan](docs/TESTPLAN.md).

## Referenzmission (noch nicht spielbar)

Der erste Einsatz ist als [deklaratives Design-Manifest](scenarios/reference_arland/mission.json) mit den Phasen Annäherung, Säuberung und Verteidigung definiert. Das Manifest ist **kein Enfusion-Ressourcenformat**. Es wird über einen [Python-Preflight](docs/MISSIONSFORMAT.md) und GitHub Actions formal geprüft und muss anschließend manuell in Enfusion Workbench als echte Szenariowelt umgesetzt und getestet werden.

## Auftragskern (Entwicklungsstand)

Unter `Scripts/Game/DOF/Core/` liegt jetzt ein **noch nicht in Workbench kompilierter** Enforce-Kandidat für den eigenständigen Auftragslebenszyklus. Ein separates Python-Referenzmodell prüft die geplante Ablaufpolitik und simuliert die drei Aufträge der Referenzmission. **Diese Tests sind kein Nachweis für Reforger-Kompatibilität.** Details: [Auftragskern und Verifikationsplan](docs/TASK_CORE.md).

## Erzählerische Missionsbibliothek (noch nicht spielbar)

Es liegen **800 fiktionale Koop-Missionsentwürfe** vor: 200 je US, USSR, FIA und zivile Einsatzrolle. Die **200 unterschiedlichen Grundhandlungen** wurden in vier Perspektiven mit eigenen benannten Beteiligten, Auftrag, Wendepunkt, zwei Entscheidungswegen und Folgen übertragen.

- [US-Missionskatalog](content/missions/katalog_us.md) / [JSON](content/missions/us.json)
- [UdSSR-Missionskatalog](content/missions/katalog_ussr.md) / [JSON](content/missions/ussr.json)
- [FIA-Missionskatalog](content/missions/katalog_fia.md) / [JSON](content/missions/fia.json)
- [Ziviler Missionskatalog](content/missions/katalog_civ.md) / [JSON](content/missions/civ.json)

Der [Umfang, die Grenzen und die Validierung](docs/MISSIONSBIBLIOTHEK.md) sind dokumentiert. **Keiner der 800 Story-Datensätze besitzt eine fertige Engine-Bridge oder garantierte Spielbarkeit.**

## Mod-Veröffentlichung: Was ist zum Spielen noch nötig?

**Noch kein installierbarer Reforger-Mod vorhanden.** Die 800 Missionen sind narrative JSON-Entwürfe, und der Enforce-Kern ist nicht in Workbench kompiliert. Die echte `addon.gproj` wurde vom Nutzer mit Workbench erzeugt und liegt unter `addon/DOF_DynamicOperations/`. Die originale Arland-Subscene `worlds/DOF_Arland/DOF_Arland.ent` samt `.meta` und noch leerem `default.layer` wurde ebenfalls aus der zweiten Workbench-ZIP übernommen. **Der echte Mission Header `Missions/DOF_Arland.conf` samt `.meta` liegt jetzt vor. In der vierten hochgeladenen Workbench-ZIP wurden die sieben echten Basis-Entities in `default.layer` gespeichert und bytegenau in GitHub übernommen: `GameModeSF`, `SCR_AIWorld`, die US/USSR-Fraktions- und Loadout-Manager, `PerceptionManager`, `RadioManager` und `ScriptedChatEntity`. Spieler-Spawn, Aufgaben und Spieltests fehlen weiterhin.**

Die genaue Anleitung für eine **spielbare Vanilla-Alpha** mit Workbench-Schritten, Tests, Workshop-Publishing und Release-Freigabe befindet sich unter [MOD_ALPHABUILD.md](docs/MOD_ALPHABUILD.md). Der vorgesehene Workbench-Projektordner ist `addon/DOF_DynamicOperations/`.

Die lokale Freigabeprüfung kann mit `python3 tools/check_mod_release.py --stage local-alpha` ausgeführt werden. Solange Engine-Ressourcen und Prüfnachweise fehlen, gibt sie absichtlich **NICHT BEREIT** zurück.

## Entwicklung und Test

Die Workbench-Projektdateien, Prefabs und Szenario-Welt müssen mit der tatsächlich installierten Arma-Reforger-Tools-Version angelegt und validiert werden. Keine `.ent`- oder `.conf`-Datei wird als funktionsfähig ausgegeben, solange sie nicht in dieser Umgebung erzeugt und geladen wurde.

**Wichtig:** Die in Workbench erzeugten Ressourcenmetadaten (`.meta`) gehören grundsätzlich zur Versionsverwaltung. Sie dürfen nicht pauschal ignoriert werden.

## Beiträge und Änderungsprozess

Neue Funktionen in `feature/*`-Branches entwickeln, über Pull Requests prüfen und erst danach nach `main` übernehmen. Ungeprüfte Engine-API-Aufrufe als solche dokumentieren. Siehe [GitHub-Workflow](docs/GITHUB_WORKFLOW.md).

## Lizenz

**Noch keine Open-Source-Lizenz vergeben.** Bis eine ausdrückliche Lizenz ausgewählt und hinzugefügt wird, gelten die normalen urheberrechtlichen Beschränkungen. Die öffentliche Sichtbarkeit allein ist keine Nutzungslizenz.
