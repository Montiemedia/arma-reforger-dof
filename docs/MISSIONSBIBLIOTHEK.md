# DOF Missionsbibliothek: 800 fiktionale Szenarien

**Stand: narrative Entwürfe. Keine dieser Missionen ist bisher im Spiel spielbar.**

## Lesbare GitHub-Kataloge

[USA](../content/missions/katalog_us.md) · [UdSSR](../content/missions/katalog_ussr.md) · [FIA](../content/missions/katalog_fia.md) · [Zivile Missionen](../content/missions/katalog_civ.md)

## Fraktionen und Inhalt

| Katalog | Umfang | Figuren | Konzept |
| --- | ---: | ---: | --- |
| `content/missions/us.json` | 200 | 400 | US-Einsatzführung, Sicherung, humanitäre Zusammenarbeit |
| `content/missions/ussr.json` | 200 | 400 | Sowjetische Einsatzführung, Lagekontrolle, Versorgung |
| `content/missions/fia.json` | 200 | 400 | Irreguläre FIA, lokale Unterstützer und Widerstand |
| `content/missions/civ.json` | 200 | 400 | Rein ziviler Koop: Rettung, Verwaltung, Infrastruktur, Versorgung |

**Gesamt:** 800 einzelne Datensätze, 1.600 benannte fiktionale Figuren, 20 Erzählbereiche, mindestens 12 Auftragsarten. Die 200 **unterschiedlichen Grundhandlungen** werden jeweils aus vier Fraktionsperspektiven mit eigenen Figuren und jeweiligen Handlungsfolgen erzählt. Sie sind somit **innerhalb jeder Fraktion verschieden**, teilen aber absichtlich den strukturellen Kern derselben 200 Fälle.

Die Titel, Handlungen, Figuren und Ereignisse sind **fiktiv**. Es handelt sich um eine vom Kalten Krieg inspirierte alternative Inselregion ohne Anspruch auf historische Tatsachen.

## Inhalt jedes Datensatzes

- Eigenständige Missions-ID `dof_{faction}_{001..200}`, gemeinsame Grundhandlungs-ID `plot_{001..200}`
- Fiktive Personen mit Namen, Rollen und persönlichen Interessen
- Ausgangslage, persönliche Geschichte, Briefing, Wendepunkt, menschliches Risiko
- Primär- und Nebenauftrag, Komplikation, Erfolg und Fehlschlag
- Zwei Entscheidungswege mit eigenen Konsequenzen
- Zwei dynamische Ereignisse (Trigger-**Ideen**, keine Engine-Trigger)
- Drei optionale Elemente für ziviles Leben
- Faction-Alias-Plan, Balance-Entwurfswerte und ehrliche Implementierungskennzeichnung

## Editor und Fraktionen

Vanilla-Tests basieren auf US, USSR, FIA; zusätzlich ist **CIV ein logisches Szenario-Profil**, dessen Spielbarkeit/Spawn-Konfiguration im gewählten Game Mode und in der Workbench geprüft werden muss. Die Bohemia-Dokumentation nennt eine zivile Fraktion im Game Master und FIA als spielbare Fraktion in neueren Conflict-Versionen. Das bedeutet **nicht**, dass das DOF bereits alle vier Fraktionen unmittelbar als Spieler-Slots unterstützt.

- `DOF_FRIENDLY` und `DOF_OPPOSING` sind **vorgeschlagene logische Alias-Namen**, keine bereits konfigurierte Game-Mode-Entität.
- Der konkrete Faction Key, Prefab-Katalog, Spawnpunkt und Loadout müssen in der **installierten** Reforger-Version verifiziert werden.
- Bei `CIV` gibt es **keine Pflichtbewaffnung oder militärische Gegnerfraktion**. Gegnerisches Verhalten, falls vorgesehen, darf nicht automatisch jeden Zivilauftrag in ein Gefecht verwandeln.
- Zusätzliche Mod-Fraktionen sind **nicht** stillschweigend abgedeckt. Sie benötigen eigene validierte Fraktionsprofile; die 200 Grundhandlungen können über eine spätere Engine-Bridge wiederverwendet werden.
- Nur **Koop**, keine Fraktionskämpfe mit Spielern gegeneinander. Pro Session ein gemeinsam spielbares Team; weitere Seiten sind KI-gesteuert.

## Struktur und Qualität

Die 200 von Hand formulierten [Grundhandlungen](../content/story_seeds_v1.txt) sind nach 20 Themengebieten geordnet (Kommunikation, Versorgung, Medizin, Evakuierung, Infrastruktur, Nachrichtendienst, Aufklärung, Konvois, Küste, Luftfahrt, Verhandlungen, Untergrund, Verwaltung, Wetter, Vermisste, Industrie, Kulturerbe, Landwirtschaft, Energienetze und öffentliche Ordnung).

Die vier Kataloge setzen sie als fraktionsbezogene Narrative um. Formulierungen der Fraktionsrahmen wiederholen sich bewusst als Stilrichtlinie; die **auslösenden Vorfälle, Aufgaben, Wendungen und Entscheidungsgegenstände** sind die 200 unterschiedlichen Grundhandlungen.

**Redaktionelle Grenze:** Die 800 Katalogeinträge wurden durch strukturierte Kombination von 200 individuell formulierten Handlungen und fraktionsspezifischen Erzählrahmen erstellt. Sie sind keine 800 unabhängig voneinander handgeschriebenen Drehbücher. Vollständige Funkdialoge, Stimmen, verzweigte Szenen und Engine-Trigger bleiben zukünftige Implementierungsarbeit.

## Automatische Prüfung

```sh
python3 tools/validate_mission_library.py content/missions
python3 -m unittest discover -s tests -v
```

Der Prüfer kontrolliert unter anderem 200 Fälle pro Katalog, 800 IDs, Story-Vollständigkeit, NPC-Namen, zwei echte Entscheidungswege, Themenvielfalt, Zivil-Schutzvorgaben und die deklarierte fehlende Engine-Integration.

Er prüft **weder** erzählerische Qualität noch tatsächliche Spielbarkeit, Fraktions-Prefabs, Performance, Mehrspieler-Replikation oder Host-Rechte. Diese Bereiche benötigen Editor-, Skript- und Multiplayer-Tests.

## Nächste Umsetzung

1. Ein einziges Referenzszenario im World Editor mit echten Prefabs erstellen und erfolgreich spielen.
2. Ein generisches `MissionDefinition -> ScenarioFramework`-Mapping mit nachgewiesenen Enfusion-APIs entwickeln.
3. Faction Alias, Loadout/Spawn-Profile und CIV-Sonderfälle technisch validieren.
4. Für einzelne Storytypen echte Trigger- und Aktionsmodule implementieren (z. B. `rescue`, `repair`, `negotiate`).
5. Den Missionsleiter mit einem Rechte geprüften Editor verbinden.
6. Danach die 800 Storys **schrittweise** als tatsächlich spielbare Missionen freigeben.
