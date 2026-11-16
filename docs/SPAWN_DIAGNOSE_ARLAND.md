# DOF Arland – Spawn-Diagnose (16.11.2026)

**Status:** Konfigurationsänderung als Hypothesentest. **F5-Ergebnis noch OFFEN.** Kein bestätigter Fix, kein abgenommener spielbarer Mod.

## Beobachtungen und Quellen

Die ZIP `DOF_DynamicOperations(4).zip` aus dem lokalen Enfusion Workbench-Projekt wurde geprüft. Sie enthält die echte Projektdatei, Arland-Subscene, Mission Header und die beiden gespeicherten Editor-Layer.

`worlds/DOF_Arland/DOF_Arland_Layers/default.layer`:
- `GameModeSF` verwendet `SCR_AutoSpawnLogic`.
- `m_sForcedFaction "US"` ist bereits gesetzt und wurde bytegenau aus dem ZIP importiert.
- Keine weiteren Änderungen gegenüber dem hochgeladenen Stand.

`worlds/DOF_Arland/DOF_Arland_Layers/Start.layer`:
- `Area1` hatte `SCR_ScenarioFrameworkArea.m_bDynamicDespawn 1`.
- `Layer1` hatte `m_bExcludeFromDynamicDespawn 1`.
- `Slot1` hat bereits `SpawnPoint_US.et` als `m_sObjectToSpawn`.

Der übermittelte Laufzeitlog bestätigt den Game Mode, PlayerController und Beitritt zu US, **nicht** aber einen tatsächlich gespawnten Charakter. Die Meldung `Available tasks are empty` ist ohne Aufträge erwartbar.

## Mögliche Erklärung

Laut der offiziellen Scenario-Framework-Dokumentation werden Areas bei aktiviertem Dynamic Spawn/Despawn abhängig vom Abstand zu Spielerfiguren instanziiert. Bei einer Area, die **den allerersten Spieler-Spawnpunkt** enthält, kann dies problematisch sein. `Exclude From Dynamic Despawn` auf `Layer1` schützt bereits erzeugte Children, garantiert aber nicht die **erste** Erzeugung eines noch nicht vorhandenen Spawnpunktes.

Dieses Verhalten ist eine **plausible Hypothese**, kein bestätigter Workbench-Fehler. Die konkrete Game-Mode-Globalaktivierung des Dynamic-Despawn-Systems wurde noch nicht separat nachgewiesen.

## Einzige gezielte Testkorrektur

In `Start.layer` wurde ausschließlich

```diff
-   m_bDynamicDespawn 1
+   m_bDynamicDespawn 0
```

geändert. Der Rest von `Start.layer` ist bytegenau unverändert.

## Abnahmetest

1. Arbeitsverzeichnis sichern, dann korrigierten `Start.layer`-Stand einspielen.
2. Projekt in **Enfusion Workbench 1.9.0.37** öffnen, `DOF_Arland.ent` laden und Game Mode / US-Spielerzuordnung kontrollieren.
3. F5 starten und prüfen, ob **ein US-Spielercharakter** tatsächlich an der `Slot1`-Position auf Arland erscheint.
4. Wenn erfolgreich, Runtime-Log sowie Ergebnis dokumentieren und wiederholten Start testen.
5. Wenn weiterhin Schwarzbild: vollständige Log Console nach `SpawnPoint`, `Respawn`, `Spawn`, `ScenarioFramework` und Fehlern durchsuchen; die nächste Diagnose darf **nicht** aus dem Fehlen einer Meldung allein eine Ursache ableiten.

## Grenzen

Dies ist **kein Enforce-Compiler-Test** und keine Aussage zur Spielbarkeit der 800 Story-Katalogeinträge. Es wurden keine erfundenen .meta-IDs oder andere nicht verifizierte Ressourcen erzeugt.

Offizielle Erklärung:
- https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework
- https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework_Setup_Tutorial
