# DOF – eigenständiger Auftragskern

**Status:** Enforce-Quelltext als **unverifizierter Workbench-Kompilierungskandidat** und getrennt davon ein durch Python testbares Referenzmodell. **Nicht spielbar, nicht an einen Game Mode angebunden, nicht repliziert.**

## Neu angelegte Enforce-Script-Dateien

- `Scripts/Game/DOF/Core/DOF_TaskState.c`: geordnete Aufgaben- und Ergebnis-Enums.
- `Scripts/Game/DOF/Core/DOF_TaskRecord.c`: einzelne Auftragszustandsmaschine mit optimistischem Revisionsschutz.
- `Scripts/Game/DOF/Core/DOF_TaskDirectorCore.c`: begrenztes Register mit maximal 64 Aufträgen, maximal 16 Vorgängern pro Auftrag, Vorbedingungen und automatischem Freischalten nach Erfolg.

Die Bezeichner sind **eigene Projektklassen**. Es werden bewusst **keine** vermuteten Engine-Methoden, UI-APIs, RPCs oder Spawn-Funktionen verwendet. Die Syntax orientiert sich an Bohemias [Scripting Keywords](https://community.bistudio.com/wiki/Arma_Reforger:Scripting:_Keywords), [Scripting Values](https://community.bistudio.com/wiki/Arma_Reforger:Scripting:_Values), [Reference Counting](https://community.bistudio.com/wiki/Arma_Reforger:Scripting:_Automatic_Reference_Counting) und [Scripting First Steps](https://community.bistudio.com/wiki/Arma_Reforger:Scripting_First_Steps).

## Zustandsmodell

```text
PLANNED -> AVAILABLE -> ACTIVE -> SUCCEEDED
    |          |          |-----> FAILED
    |          |          |-----> PAUSED -> ACTIVE
    |          |          |
    +----------+----------+-----> CANCELLED
```

Abschließende Zustände `SUCCEEDED`, `FAILED`, `CANCELLED` werden nicht reaktiviert. Jeder **angewendete** Übergang erhöht die Revision genau einmal. Abgewiesene Änderungen erhöhen sie nicht.

`RequestState(taskId, next, expectedRevision)` gibt unterschiedliche Rückgabecodes für durchgeführte, doppelte, veraltete, unzulässige oder wegen nicht erfüllter Vorgänger blockierte Aktionen zurück.

Die Registrierung von Aufgaben ist absichtlich **topologisch**: Ein Vorgänger muss bereits registriert sein. Dadurch sind Zyklen ausgeschlossen und das Prüfen einer Auftragsverkettung bleibt klein und deterministisch.

## Sicherheitsgrenze

**Diese Klassen besitzen keine eigene Serverautorität und keine Rollenprüfung!** Es handelt sich um Zustandsdaten. Ein späterer serverseitiger Adapter muss jede Änderung auf der Authority-Instanz nach autorisierter RPC-Absenderprüfung ausführen. Dieser Adapter darf die internen `DOF_TaskRecord`-Referenzen nicht ungeschützt an Clients weitergeben.

Für das erste Szenario bleibt das vorhandene Scenario Framework zuständig; der DOF-Kern übernimmt noch **keine** Game-Mode-Aufgaben. Eine Doppelzuständigkeit wäre ein Fehler.

## Referenzmodell und ausführbare Tests

Die Python-Datei `tools/dof_task_reference.py` bildet dieselbe **beabsichtigte** Übergangspolitik nach. Es ist **kein Enforce-Interpreter**. Die Python-Tests prüfen ausschließlich diese Referenzimplementierung; sie beweisen **nicht**, dass der Enforce-Quellcode kompiliert, zur Laufzeit dieselben Ergebnisse liefert oder Multiplayer-sicher ist.

```sh
python3 -m unittest discover -s tests -v
python3 tools/simulate_reference_mission.py scenarios/reference_arland/mission.json
```

Die Simulation spielt die komplette Folge `approach -> clear -> defend` durch, ohne Spielwelt oder KI.

## Workbench-Abnahme (weiterhin offen)

1. Enfusion Workbench in der installierten Version starten.
2. Skripte im Add-on `DOF_DynamicOperations` unter `Scripts/Game/DOF/Core/` speichern.
3. `Shift + F7` / vollständige Skriptkompilierung auslösen. **Kompilierfehler nicht kaschieren**, sondern korrigieren.
4. Einen lokalen **testweisen Aufruf aus einer eigenen Workbench-Testumgebung** erstellen; die ausgewählten Hook-APIs erst nach Prüfung implementieren.
5. Registrieren: `approach`, `clear` mit Vorgänger `approach`, `defend` mit Vorgänger `clear`.
6. Mission starten; nur `approach` muss zunächst `AVAILABLE` sein.
7. `approach` aktivieren und erfolgreich abschließen; nur dann wird `clear` verfügbar. Dasselbe für `defend`.
8. Doppelte, veraltete und unzulässige Zustandswechsel sowie Fehlschlag/Abbruch testen.
9. Erst danach einen autoritativen Game-Mode-Adapter entwickeln und Listen-/Dedicated-Server sowie Join-in-Progress prüfen.

**Issue #4 ist mit diesem PR noch nicht abgeschlossen.** Die Core-Skripte müssen in Workbench kompiliert und gegen dieselben Übergangsfälle getestet werden. Die sichere RPC-Anbindung folgt separat in Issue #5/#6.

## Risiken

- Enforce-Compiler-/API-Version unbekannt; Syntax und Referenzlebensdauer müssen lokal bestätigt werden.
- Die Python-Implementierung ist nicht automatisch äquivalent zum Enforce-Code.
- Kein globales Event-Journal, keine Persistenz, keine Engine-Replikation.
- Der spätere Director muss berechtigte Befehle serialisieren und Aufgaben von physischen Entities trennen.
