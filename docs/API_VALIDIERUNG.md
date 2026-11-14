# Engine-/API-Verifikation für DOF

Stand: **14.11.2026**. Dieser Stand basiert auf **öffentlich abrufbarer Bohemia-Dokumentation**, **nicht** auf einer lokalen Enfusion-Workbench-Installation. Die installierte Reforger-Version ist noch unbekannt. Jede Kompilierungs- und Multiplayer-Aussage bleibt bis zu einem Test **OFFEN**.

## Statuslegende

- **DOKUMENTIERT:** In einer offiziell veröffentlichten Anleitung oder API-Referenz gefunden.
- **LOKAL OFFEN:** In der tatsächlich installierten Spiel-/Workbench-Version noch nicht geprüft.
- **INTEGRATION OFFEN:** Komponenten sind einzeln dokumentiert, aber ihr gemeinsamer Einsatz wurde nicht nachgewiesen.

## Verifizierte Dokumentationsgrundlage

| Sachverhalt | Quellenstand | Konsequenz für DOF |
| --- | --- | --- |
| `SCR_BaseGameMode` und `SCR_BaseGameModeComponent` für komponierbare Spielmodi | DOKUMENTIERT, LOKAL OFFEN | Eignet sich als spätere Erweiterungsbasis, API-Signaturen lokal vergleichen |
| In einer Welt nur **eine** Game-Mode-Instanz | DOKUMENTIERT, LOKAL OFFEN | Nicht zwei komplette Game Modes platzieren |
| `ScenarioFramework.conf` über `Plugins > Game Mode Setup` | DOKUMENTIERT, LOKAL OFFEN | Vanilla-Referenzszenario mit Setup-Assistent anlegen |
| `GameModeSF.et` und `SCR_GameModeSFManager` | DOKUMENTIERT, LOKAL OFFEN | Scenario Framework zunächst unverändert erproben |
| `LayerTaskMove`, `SlotMoveTo`, `LayerTaskClearArea`, `SlotClearArea`, `LayerTaskDefend`, `SlotDefend` | DOKUMENTIERT, LOKAL OFFEN | Drei Phasen im Editor ohne erfundene Engine-API möglich |
| `SCR_ScenarioFrameworkActionSpawnObjects` und Aktivierung `ON_TRIGGER_ACTIVATION` | DOKUMENTIERT, LOKAL OFFEN | Folgeaufträge über vorhandene Framework-Actions verkettbar |
| `SlotClearArea` verwendet TriggerDominance und Fraktionsprüfung | DOKUMENTIERT, LOKAL OFFEN | FactionKey/Trigger-Einstellungen gezielt testen |
| `LayerTaskDefend` kennt `Defend Time` und Verteidigeranteil | DOKUMENTIERT, LOKAL OFFEN | Referenz-Test 60 Sekunden / 0.51 möglich |
| Game Master ermöglicht Live-Verwaltung von KI, Fahrzeugen und Prefabs | DOKUMENTIERT, LOKAL OFFEN | Eigene UI nicht unnötig duplizieren; Integration aber gesondert prüfen |
| Replikation: `RplComponent`, `RplRpc`, `RplRcver`-Routing | DOKUMENTIERT, LOKAL OFFEN | Befehle serverautoritär auslegen; Sender-/Owner-Validierung zwingend |
| Client-`RplRcver.Server`-Aufrufe ohne Ownership können verworfen werden | DOKUMENTIERT, LOKAL OFFEN | Kein willkürliches Global-RPC-Objekt für administrative Clientaktionen |

## Architekturgabel: Scenario Framework + Game Master

**Noch nicht belegt:** Dass das Vanilla-Scenario-Framework-Game-Mode-Prefab und die vollständige Game-Master-Runtime ohne weitere Anpassungen gemeinsam nutzbar sind.

Es gibt drei Entwicklungsoptionen:

1. **Prototyp A (empfohlen):** Unverändertes Scenario Framework für die erste dreistufige Mission. Niedriger Integrationsaufwand, aber zunächst keine freie Game-Master-Bearbeitung.
2. **Prototyp B:** Vanilla-Game-Master-Game-Mode im eigenen Szenario testen; Ereignis-/Auftragsmodule nur nach nachgewiesener Kompatibilität anhängen.
3. **Prototyp C:** Eigener Game Mode aus `SCR_BaseGameMode` plus ausgewählten Komponenten; höchster Aufwand, nur bei Bedarf.

**Entscheidung:** A für DOF 0.1, danach B als isolierten Integrationsversuch. Bei Konflikten nicht stillschweigend zwei Game Modes kombinieren. DOF-Kernmodelle bleiben von dieser Wahl unabhängig.

Das Scenario-Framework-Debug-Menü ist laut Dokumentation für Szenarioentwicklung konzipiert und ausdrücklich kein verlässliches administratives Multiplayer-Menü. Nicht als Ersatz für DOF-Berechtigungskontrollen verwenden.

## Vor einem produktiven Enforce-Script-Commit lokal prüfen

- [ ] Spiel-/Tools-Version und Add-on-Abhängigkeiten
- [ ] Vorhandene Prefabs und Pfade in Resource Browser (insbesondere `GameModeSF.et`, Task-Layer und Slots)
- [ ] `SCR_BaseGameModeComponent`-Callbacks und Signaturen, Initialisierungs-/Abbaufolge
- [ ] Echte Teilnehmerzahl: Game Master, Zuschauer, Respawn und Fraktionszugehörigkeit
- [ ] Client-/Server-Rollen und sichere Absenderzuordnung für den konkret gewählten RPC-Endpunkt
- [ ] Join-in-Progress und vollständige Zustandsreplikation
- [ ] Registrieren/Löschen von Spawns, Aufräumen bei Missionsende
- [ ] Task-System-Bridge und Zusammenspiel mit Game Master
- [ ] Berechtigungskontrolle für **jede** administrative Aktion
- [ ] Workbench-Kompilierung und Listen-/Dedicated-Server-Test

Es ist verboten, einen dokumentierten API-Namen ohne Abgleich mit der Zielversion als kompiliert oder getestet zu kennzeichnen.

## Öffentliche Primärquellen

1. [General Game Mode Setup](https://community.bistudio.com/wiki/Arma_Reforger:General_Game_Mode_Setup) – nur eine Game-Mode-Instanz; BaseGameMode und Komponenten.
2. [Scenario Framework](https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework) – Prefabs, Layer/Slots/Actions, Trigger, Debug.
3. [Scenario Framework Setup Tutorial](https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework_Setup_Tutorial) – Subscene, Setup und Auftragsverkettung.
4. [Game Master](https://community.bistudio.com/wiki/Arma_Reforger:Game_Master) – existierende Laufzeitfunktionen und Game-Master-Rollen.
5. [Multiplayer Scripting](https://community.bistudio.com/wiki/Arma_Reforger:Multiplayer_Scripting) – Autorität, Ownership, RplComponent, RPC.
6. [Enfusion Script API: Replication overview](https://community.bistudio.com/wikidata/external-data/arma-reforger/EnfusionScriptAPIPublic/Page_Replication_Overview.html) – Routingtabelle und Client-Ownership.
7. [SCR_GameModeEditor API](https://community.bistudio.com/wikidata/external-data/arma-reforger/ArmaReforgerScriptAPIPublic/interfaceSCR__GameModeEditor.html) – existierende Game-Master-Game-Mode-Klasse.

## Anschließende Arbeiten

- `docs/WORKBENCH_SZENARIO_0_1.md` ist die konkrete Anleitung für den ersten Editor-Prototyp.
- Issue #2 bleibt offen, bis die **lokale Version/Workbench-Kompatibilität** tatsächlich verifiziert ist.
- Issue #3 bleibt offen, bis die echte Editor-Welt erzeugt und ein reproduzierbarer Play-Test protokolliert wurde.
