# Missionsdefinition v1: deklaratives DOF-Format

Die Datei [reference_arland/mission.json](../scenarios/reference_arland/mission.json) beschreibt den ersten Referenzeinsatz **als Daten**, nicht als native Arma-Reforger-Ressource.

**Kein Editor-Import, keine Enforce-Integration und keine garantierte Spielbarkeit.** Die Werte müssen in der installierten Workbench in echte Scenario-Framework-Entities übertragen werden. Sie ersetzen keine `.ent`, `.conf` oder `.meta`-Dateien.

## Warum zusätzlich ein Manifest?

Das Framework soll Aufgaben-Logik, Abhängigkeiten und Balancewerte unabhängig von einer bestimmten Karte oder einem Workshop-Mod halten. Später kann eine verifizierte Engine-Bridge diese logische Konfiguration mit den realen Editor-Entities verknüpfen.

Bis dahin ist das Manifest ein **prüfbarer Bau- und Testvertrag**: eindeutige Namen, Reihenfolge, Auftragsarten und Limits.

## Felder

- `format_version`: gegenwärtig ausschließlich `1`
- `status`: zwingend `design_only` bis eine tatsächlich getestete Engine-Bridge existiert
- `mission_id`: stabile logische Missions-ID, snake_case
- `reference_map`: Testwelt; **keine** Koordinatenabhängigkeit des DOF-Kerns
- `integration`: für den ersten Workbench-Prototyp `scenario_framework`
- `factions`: Test-Fraktionszuordnung, später durch konfigurierbare Fraktionsprofile zu ersetzen
- `limits.max_scripted_ai`: konservatives Design-Limit, **keine Engine-Garantie**
- `limits.allow_repeat_spawns`: in v1 bewusst `false`
- `stages`: Auftragsfolge; jedes Element hat eine logische ID, einen Auftrags-Typ, den erwarteten Layer- und Slot-Namen, Vorgänger und Aktivierungsbedingung

Die aktuell erlaubten `task_type`-Werte sind `move`, `clear` und `defend`. Das beschreibt nur die Referenzmission, nicht alle später geplanten generischen Aufträge.

Beim Typ `defend` definieren `hold_seconds` und `min_defender_ratio` die Zielvorgaben; deren echte Engine-Semantik ist in Workbench zu prüfen.

## Referenz-Zuordnung

| Logische ID | Scenario-Framework-Layer | Slot | Aktivierung |
| --- | --- | --- | --- |
| `approach` | `LayerTaskMove_Approach` | `SlotMoveTo_Approach` | Missionsbeginn |
| `clear` | `LayerTaskClearArea_Clear` | `SlotClearArea_Objective` | Nach Erfolg von `approach` |
| `defend` | `LayerTaskDefend_Hold` | `SlotDefend_Hold` | Nach Erfolg von `clear` |

Die Namen sind **unsere beabsichtigten Entity-Namen**, keine angeblich in der Vanilla-Engine vorhandenen Instanzen. In der Szene werden sie manuell vergeben.

Für den tatsächlichen Editoraufbau siehe [WORKBENCH_SZENARIO_0_1.md](WORKBENCH_SZENARIO_0_1.md).

## Preflight-Validierung

Python 3, ausschließlich Standardbibliothek:

```sh
python3 tools/validate_mission_manifest.py scenarios/reference_arland/mission.json
python3 -m unittest discover -s tests -v
```

Der Validator prüft Struktur, eindeutige IDs, erlaubte Auftragsarten, gültige Vorgänger, azyklische Reihenfolge, Ausgangsauftrag, Aktivierungsbedingungen, defensive Zielwerte und ein einfaches KI-Slot-Budget.

**Das ist kein Workbench-Compiler und kein Laufzeittest.** Die CI kann daher nur formale Inkonsistenzen in diesem JSON verhindern. Dies wird in GitHub bewusst als `mission manifest preflight` bezeichnet, nicht als Game-/Multiplayer-Validierung.

## Freigabe für eine echte Mission

Erst wenn die Welt in Workbench gespeichert wurde und ein lokaler Playtest funktioniert, die tatsächlichen `.ent`, `.meta`- und Szenariokonfigurationsdateien einchecken. Anschließend auf Listen- und Dedicated-Servern prüfen. Issues #2 und #3 bleiben bis dahin offen.
