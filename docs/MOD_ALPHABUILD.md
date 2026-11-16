# DOF – vom GitHub-Entwurf zum installierbaren Arma-Reforger-Mod

**Aktueller Stand (16.11.2026): Projektdatei angelegt, weiterhin nicht installierbar und nicht spielbar.** Die Missionsbibliothek ist JSON-Erzählmaterial. Der vorhandene Enforce-Code ist nicht in einer echten Workbench kompiliert oder eingebunden. GitHub Actions testet bislang nur Python. Dieses Dokument ist eine **konkrete Build-/Releaseanleitung**, kein Nachweis eines Mods.

## Release-Ziel: DOF v0.1 Playable Alpha

Ein kleinstes eigenständiges Reforger-Add-on mit **genau einem** lokal und im Multiplayer geprüften Vanilla-Koop-Referenzszenario auf Arland. Spieler erfüllen einen Annäherungs-, Säuberungs- und Verteidigungsauftrag. Das Szenario muss mit seiner eigenen generierten Mission-Header-Konfiguration in der Scenario-Liste erscheinen.

Keine anderen Pflichtmods, keine Behauptung von 800 spielbaren Missionen, keine Host-Menüs oder dynamischen Verstärkungen in der Alpha, solange die tatsächliche Engine-Integration nicht existiert. Auch „alle Fraktionen“ bleibt im v0.1-Kern eine weitere Abnahmeanforderung. Keine unangekündigten Fraktionswechsel zur Laufzeit.

## Die notwendige einmalige Arbeit am PC

1. **Arma Reforger** und **Arma Reforger Tools** über Steam installieren. Beide müssen derselben stabilen Spiel-/Tools-Generation entsprechen (Experimental nur als bewusst getrennte Umgebung).
2. In der **Enfusion Workbench Launcher**-Projektauswahl bei Bedarf das Basisprojekt `<Reforger installation>/addons/data/ArmaReforger.gproj` über **Add Existing** registrieren.
3. Dieses GitHub-Repository lokal klonen (z. B. außerhalb von OneDrive und `Program Files`).
4. **Erledigt:** Nutzer hat mit dem Workbench Launcher ein Projekt `DOF_DynamicOperations` unter `D:/ArmaReforgerMods` erstellt. Das reale `addon.gproj` aus der hochgeladenen ZIP-Datei wurde unverändert unter `addon/DOF_DynamicOperations/addon.gproj` versioniert. Die auf dem PC vorhandene Projektdatei **beibehalten und keinesfalls ein neues Projekt mit anderer GUID anlegen**. Die lokale Datei und die GitHub-Version sind derselbe Projektursprung.
5. **Erledigt und als Original aus der zweiten Workbench-ZIP versioniert:** Arland-Subscene `worlds/DOF_Arland/DOF_Arland.ent` mit `.meta` (Ressourcenkennung `{C44343EE652CEF8A}`) und zunächst leerem `DOF_Arland_Layers/default.layer`. Die `.ent` verweist auf die Vanilla-Arland-Welt. **Keine neue Subscene anlegen**, sondern genau diese im World Editor öffnen.
6. **Plugins → Game Mode Setup** mit **`ScenarioFramework.conf`** öffnen; **Create entities** und **Create header** benutzen, sodass die für das Szenario notwendigen Runtime-Entities und die echte Missionskonfiguration unter `Missions/` angelegt werden.
7. Die drei Aufträge, den Spieler-Spawn sowie den kontrollierten KI-Ansatz **in Workbench** gemäß [WORKBENCH_SZENARIO_0_1.md](WORKBENCH_SZENARIO_0_1.md) anlegen.
8. **Zunächst keine ungetesteten Enforce-DOF-Kernskripte in dieses Add-on kopieren.** Die Dateien im separaten Repository-Ordner `Scripts/Game/DOF/Core` sind Kandidaten, keine kompilierten, funktionsfähigen Module. Das 0.1-Alpha-Szenario nutzt zuerst ausschließlich vorhandene Vanilla-Scenario-Framework-Bausteine.
9. Im Workbench-Play-Modus (`F5`) prüfen: Spawn, Auftragsanzeige, sämtliche drei Phasen, Erfolg, Fehlschlag, erneuter Start. Build-/Test-Log sichern.
10. Einen Listen-Server mit mindestens zwei Spielern und anschließend einen Dedicated Server **tatsächlich** testen, einschließlich Join-in-Progress und Missionsabschluss. Verwendete Versionen, Mods, Logs und Fehler protokollieren.
11. Von Workbench erzeugtes **`.gproj`, `.ent`, zugehöriges `.meta`, Mission-Header-`.conf` und zugehöriges `.meta`** in GitHub committen. **Keine** erfundenen Resource-GUIDs oder händisch erfundenen Engine-Dateien verwenden.

Projektanlage **und Subscene mit Resource-Metadaten sind erledigt**. **Aktueller Blocker:** Der von Workbench erzeugte Mission Header `Missions/DOF_Arland.conf` (GUID `{854AF38C5722D963}`) liegt samt `.meta` aus der dritten ZIP vor. Er enthält noch Platzhalter für Namen, Autor und Beschreibung. `default.layer` ist weiterhin **leer**; Game-Mode-Entities sind nicht im hochgeladenen Projekt gespeichert. Nach Klärung dieser Entities folgen US-Spielerspawn, echte Aufgaben, Tests und Veröffentlichungsbundle. **Nicht erneut blind `Create header` ausführen, um keine Dopplung zu erzeugen.** Nach jedem Editor-Schritt die neuen Dateien aus `D:/ArmaReforgerMods/DOF_DynamicOperations/` erneut als ZIP übermitteln oder kontrolliert ins GitHub-Checkout synchronisieren.

## Release-Preflight (nur Dateien und dokumentierte Testresultate)

Eine Vorlage steht unter [qa-evidence.example.json](../release/qa-evidence.example.json). Nach tatsächlich durchgeführten Prüfungen eine ausgefüllte Kopie unter `addon/DOF_DynamicOperations/release/qa-evidence.json` speichern. Nur durchgeführte Tests als `passed: true` kennzeichnen und Logs/Berichte referenzieren.

Im GitHub-Checkout:

```sh
python3 tools/check_mod_release.py --stage local-alpha
python3 tools/check_mod_release.py --stage publish-candidate
```

Der erste Modus verlangt Workbench-Projekt, Szenario-Assets, Metadaten sowie protokollierte Kompilierung und lokalen Playtest. Der zweite verlangt zusätzlich Listen-/Dedicated-Server-Test und eine erfolgreiche Workbench-Bundle-Erstellung.

**Grenze:** Die Kontrolle prüft nur Existenz und *angegebene* Testresultate. Sie interpretiert keine Enfusion-Assets, kompiliert keinen Code und kann unzutreffende Angaben nicht erkennen. Auch ein grüner Release-Preflight ersetzt **keinen** realen Spieltest.

## Workshop-Publishing

1. In Workbench das **wirklich funktionsfähige und gebündelte** Add-on öffnen.
2. Bohemia Account mit Workbench über **Workbench → Link** verknüpfen.
3. **Workbench → Publish Project**, notwendige Angaben und Bilder eintragen, Bundle erzeugen/prüfen.
4. Ersten Build als **Private** oder **Test** veröffentlichen. Durch normales Reforger-Spielmenü den Download aktivieren, Szenario auswählen und lokal sowie auf Server verifizieren.
5. Erst dann Sichtbarkeit **Public** setzen bzw. die freigegebene Version öffentlich veröffentlichen. Workshop-ID im Projekt dokumentieren; sie darf nicht erfunden werden.

Nach dem Upload muss der Host über **Workshop** die Mod beziehen. Für Dedicated Server den tatsächlichen `modId` in `game.mods` und den vom Spiel mittels `-listScenarios` ermittelten **`game.scenarioId`** in die Server-Konfiguration übernehmen. Kein Placeholder als angeblich startfähige Konfiguration benutzen.

Bohemia empfiehlt für öffentliche Server `fastValidation: true` und begrenzte Server-FPS (z. B. `-maxFPS 60`). Netzwerkfreigaben und Admin-Berechtigungen müssen nach dem realen Hosting geklärt werden.

## Was **nicht** automatisch passiert

- Die 800 Story-JSONs werden nicht von Reforger als Missionen geladen.
- Der bisherige DOF Task Director hat noch keine validierte Engine-Bridge und keinen vertrauenswürdigen RPC-Transport.
- Das bestehende Game-Master- und Scenario-Framework-Game-Mode-Prefab darf nicht als zwei unabhängige Game Modes in einer Welt platziert werden.
- Die reale `addon.gproj` ist bereits vorhanden. **Weitere** Asset-GUIDs, Mission Header, Bundles und die Workshop-ID dürfen nicht aus Fantasiewerten erstellt werden.

## Offizielle Quellen

- [Mod Project Setup](https://community.bistudio.com/wiki/Arma_Reforger:Mod_Project_Setup)
- [Scenario Framework Setup Tutorial](https://community.bistudio.com/wiki/Arma_Reforger:Scenario_Framework_Setup_Tutorial)
- [Mod Publishing Process](https://community.bistudio.com/wiki/Arma_Reforger:Mod_Publishing_Process)
- [Server Hosting](https://community.bistudio.com/wiki/Arma_Reforger:Server_Hosting)
- [Server Config](https://community.bistudio.com/wiki/Arma_Reforger:Server_Config)
