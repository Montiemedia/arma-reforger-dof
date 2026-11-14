# DOF 0.1: Workbench-Referenzszenario

**Status:** Bauanleitung anhand der offiziellen Bohemia-Dokumentation. **Noch nicht in einer installierten Workbench ausgeführt oder im Multiplayer getestet.**

**Voraussetzungen:** Arma Reforger Tools mit Enfusion Workbench, ein neues Add-on, Zugriff auf Vanilla-Ressourcen. Genaue Reforger- und Tools-Version zunächst offen. Referenzwelt Arland nur für den Test; die spätere DOF-Logik soll keine festen Kartenkoordinaten enthalten.

## Integrationsentscheidung für den ersten Test

Wir beginnen mit einem **Scenario-Framework-Szenario ohne vorausgesetzte Game-Master-Funktion**. Der Game Master wird als eigener Integrationspfad untersucht. Eine Arma-Reforger-Welt besitzt nur **eine** Game-Mode-Instanz. Es wäre falsch, `GameModeSF.et` und eine zweite Game-Mode-Entity nebeneinander zu setzen.

Das Experiment muss erst belegen, ob sich die für den späteren Missionsbauer benötigten Game-Master-Funktionen auf der gewählten Grundlage sicher ergänzen lassen. Falls das nicht möglich ist, wird ein eigener Game Mode auf Basis von `SCR_BaseGameMode` mit wiederverwendbaren Szenario-Modulen geprüft. **Bis dahin ist kein Live-Zeus-/GM-Menü garantiert.**

Quellen:
- [General Game Mode Setup](https://community.bistudio.com/wiki/Arma_Reforger:General_Game_Mode_Setup)
- [Scenario Framework](https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework)
- [Game Master](https://community.bistudio.com/wiki/Arma_Reforger:Game_Master)

## 1. Add-on und Subscene anlegen

1. Neues Add-on `DOF_DynamicOperations` über Workbench erstellen.
2. World Editor starten, **Arland** als bestehende Welt laden.
3. `File > New World > Sub-scene (of current world)` wählen.
4. Unter einem eigenen Pfad wie `worlds/DOF_Arland/DOF_Arland.ent` speichern. Der Pfad ist ein Namensvorschlag; die echte Datei in Workbench erzeugen.
5. `Plugins > Game Mode Setup` öffnen.
6. Template **`ScenarioFramework.conf`** auswählen; bei sauberer Subscene `World Scan` überspringen; `Create entities` und `Create header` verwenden.
7. Ergebnis auf fehlende Entities/Abhängigkeiten kontrollieren und die Subscene speichern.

Die Dokumentation nennt in der Standardkonfiguration u. a. `GameModeSF.et`, `SCR_AIWorld.et`, `FactionManager_USxUSSR.et`, `LoadoutManager_USxUSSR.et`, `RadioManager.et`, `PerceptionManager.et` und `ScriptedChatEntity.et`. Nicht manuell doppelt anlegen, wenn der Setup-Assistent die benötigten Entities bereits erzeugt hat.

Quelle: [Scenario Framework Setup Tutorial](https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework_Setup_Tutorial).

## 2. Spielerbereitstellung

1. In der Subscene eine organisatorische Ebene `DOF_Start` anlegen.
2. Aus `ArmaReforger/Prefabs/Systems/ScenarioFramework/Components` eine `Area.et` platzieren.
3. Unter der Area eine `Layer` und darunter einen normalen `Slot` anlegen.
4. In der `SCR_ScenarioFrameworkSlotBase`-Komponente `Object To Spawn = SpawnPoint_US.et` zuweisen.
5. Optional: Zweiten Slot mit `ArsenalBox_US.et` anlegen.
6. Welt speichern; mit Workbench Play (`F5`) den Spawn prüfen.

Die zwei Prefabs gelten nur für den Vanilla-Referenztest und werden später durch Fraktionsprofile ersetzt.

## 3. Phase A: Annäherung

1. Neue Area `DOF_Approach` erstellen.
2. `LayerTaskMove.et` unter die Area ziehen.
3. `SlotMoveTo.et` als Kind hinzufügen und an der gewünschten Zielposition platzieren.
4. Trigger-Radius in der installierten Workbench überprüfen; als Testbereich klein und eindeutig halten.
5. Die Aufgabe in Play mit Karten-/Auftragsanzeige prüfen. Das Betreten der Zone muss den Auftrag abschließen.

## 4. Phase B: Zielbereich säubern

1. Area `DOF_Clear` anlegen, darunter `LayerTaskClearArea`.
2. Darunter einen Layer mit `SlotClearArea` und einen zweiten Layer mit drei `SlotAI` erstellen.
3. `SlotClearArea` erzeugt einen Dominanz-Trigger. Den **FactionKey der auftragsempfangenden Fraktion** für die Trigger-Aktivierung und die Erkennung der Akteure überprüfen.
4. Für den reinen Funktionsnachweis drei einzelne Vanilla-USSR-Soldaten einsetzen. Die tatsächlichen Prefabs in der installierten Ressourcendatenbank auswählen.
5. Im LayerTask unter `Activation Type` **`ON_TRIGGER_ACTIVATION`** setzen.
6. Im Annäherungsauftrag unter `OnTaskFinished` die Action `SCR_ScenarioFrameworkActionSpawnObjects` hinzufügen und als Ziel den **exakten Entity-Namen** des Säuberungs-LayerTask angeben.
7. Zunächst ohne dynamisches Despawning und ohne wiederholte KI-Spawns prüfen.

Hinweis: `SlotClearArea` benötigt eine passende Trigger-Konfiguration; eine bloße Namensgleichheit ersetzt nicht die Fraktions- und Dominanzprüfung. Die offiziellen Beispiel-Szenarien `TaskClearArea` dienen als Vorlage.

## 5. Phase C: Stellung verteidigen

1. Area `DOF_Hold` mit `LayerTaskDefend` anlegen.
2. Zwei Unterlayer für Angreifer und Verteidiger erstellen, den Angreifer-Layer mit zwei kleinen `SlotAI`-Einträgen ausstatten.
3. Im Verteidiger-Layer `SlotTrigger` und `SlotDefend` hinzufügen. Die Zuordnung des Trigger-Namens im `LayerTaskDefend` und die Zonenlage **in Workbench** prüfen.
4. `Faction Settings` korrekt auf US-Verteidiger und USSR-Angreifer setzen.
5. Testparameter: `Defend Time = 60` Sekunden; `Min Defender Percentage Ratio = 0.51` (Mehrheit der Verteidiger zum Auswertungszeitpunkt).
6. `Attacker Layer Names` muss dem tatsächlichen Unterlayer-Namen entsprechen.
7. `Activation Type = ON_TRIGGER_ACTIVATION` für diesen Auftragslayer setzen.
8. `OnTaskFinished` des Säuberungsauftrags: `SCR_ScenarioFrameworkActionSpawnObjects` auf den Verteidigungs-LayerTask.
9. `OnTaskFinished` der Verteidigungsaufgabe: `EndMission`-Action passend zur gewünschten Erfolgsanzeige konfigurieren.
10. Den Fehlschlagszweig über die verfügbaren `Actions On Failed` / Game-Over-Einstellungen gesondert einrichten und prüfen; **nicht** pauschal denselben Erfolgspfad verwenden.

Die offiziellen `TaskDefendArea`-Samples dokumentieren einen 60-Sekunden-Verteidigungsauftrag mit Ratio 0.51. Die Standard-Samples können wiederholte Angreifer-Spawns verwenden; für unsere erste Abnahme bleiben diese **ausgeschaltet**, damit keine Wellen unbeabsichtigt eskalieren.

## 6. Testfälle vor dem ersten Playable-Commit

- **S01:** Subscene lädt ohne fehlende Prefab- oder Script-Ressourcen.
- **S02:** US-Spieler spawnt mit nutzbarer Auftragsanzeige.
- **S03:** Annäherung beendet sich beim Betreten der Zielzone genau einmal.
- **S04:** Säuberungsauftrag existiert erst nach S03; Trigger erkennt die gegnerische Präsenz.
- **S05:** Säuberung startet Verteidigungsphase genau einmal.
- **S06:** Verteidigung schließt nach 60 Sekunden bei erfüllter Bedingung erfolgreich.
- **S07:** Fehlende Kontrolle führt zu definiertem Fehlschlag, nicht zu Erfolg.
- **S08:** Neu laden / erneuter Missionsstart erzeugt keine Duplikate.
- **S09:** Zwei Spieler auf Listen-Server sehen dieselben Aufträge.
- **S10:** Dedicated-Server-Test ohne lokale Host-Spielerfigur; JIP gesondert prüfen.

Pro Test Reforger-Version, Workbench-Version, Karte, Fraktionen, Spielerzahl, Servertyp, Logs und Ergebnis dokumentieren. **Aktueller Status aller S01–S10: OFFEN.**

## 7. Explizite Grenzen

- Noch keine Host-Menüs, Berechtigungs-RPCs oder automatische Skalierung des DOF-Directors.
- Scenario-Framework-Debugfunktionen nicht als produktives Multiplayer-Administrationsmenü behandeln; die offizielle Dokumentation beschreibt sie als Szenariobauer-/Debug-Hilfe und nicht als Live-Multiplayer-Steuerung.
- Laufzeit-Spawns, Replikation, Host- vs. Dedicated-Server-Details und Game-Master-Zugriff bleiben getrennte Integrationsprüfungen.
- Hier werden keine künstlich erzeugten `.ent`, `.conf`, `.meta` oder angeblich kompilierten Enforce-Skripte geliefert.

## Quellen

- https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework_Setup_Tutorial
- https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework
- https://community.bistudio.com/wiki/Arma_Reforger:General_Game_Mode_Setup
- https://community.bistudio.com/wiki/Arma_Reforger:Game_Master
