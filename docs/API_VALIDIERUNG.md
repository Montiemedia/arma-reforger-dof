# Engine-API-Verifikationsliste

**Noch nicht verifiziert in der Zielversion.** Keine der hier genannten Schnittstellen darf allein aus dem Namen als verfügbar oder kompatibel gelten.

## Vor dem ersten Enforce-Commit prüfen

- Welche Version von Arma Reforger und Reforger Tools ist installiert?
- Welche Game-Mode-Konfiguration unterstützt den vorgesehenen Szenario- und Game-Master-Ablauf?
- Welche `SCR_BaseGameModeComponent`-Callbacks sind in der installierten Version verfügbar?
- Wie wird die tatsächliche Spieleranzahl einschließlich Game Master, Zuschauer, Respawn und Fraktionszugehörigkeit ermittelt?
- Wie sieht der unterstützte RPC- und RplComponent-Workflow einschließlich zuverlässiger Senderzuordnung aus?
- Welche Scenario-Framework-Layer/Slots/Actions stehen konkret zur Verfügung?
- Wie werden Spawn-Prefabs, Fraktionszuordnung, Kollision und Entfernung sicher kontrolliert?
- Wie lässt sich eine eigene Menüoberfläche an den ausgewählten Game Mode anbinden?

Zu jedem verwendeten API-Aufruf eine Quelle oder lokalen Verifikationsvermerk und einen Workbench-Kompilierungsnachweis hinterlegen.
