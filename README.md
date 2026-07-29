# Railway Safety Zone Analysis (QGIS / PyQGIS)

[English](#english) | [Deutsch](#deutsch)

---

## English

Automates a spatial safety-buffer analysis around railway lines using OpenStreetMap data, fully reproducing a manual QGIS workflow as a repeatable, headless script.

### Pipeline

1. Load raw OSM line data from a GeoPackage (extracted via BBBike/Overpass)
2. Filter to keep only `railway=rail` features
3. Reproject to a metric CRS (ETRS89 / UTM zone 32N) for accurate distances
4. Buffer the railway lines by a configurable safety distance (dissolved)
5. Load building polygons from the same source
6. Fix invalid geometries (common in OSM building footprints)
7. Select buildings that intersect/overlap the safety buffer
8. Export the at-risk buildings to a new GeoPackage

### Requirements

- QGIS installed (tested on QGIS 3.44 "Solothurn")
- Run with the Python interpreter bundled with QGIS (OSGeo4W shell on Windows, or the QGIS Python environment on Linux/macOS)

### Usage

```bash
python rail_safety_zone_analysis.py
```

Adjust the input GeoPackage path and buffer distance at the top of the script to match your data and safety-distance requirements.

### Output

A new GeoPackage containing only the buildings that fall within the configured safety buffer around the railway lines.

---

## Deutsch

Automatisiert eine räumliche Sicherheitsabstands-Analyse entlang von Bahnstrecken auf Basis von OpenStreetMap-Daten und bildet einen manuellen QGIS-Workflow als wiederholbares, headless-Skript ab.

### Ablauf

1. Laden der rohen OSM-Liniendaten aus einem GeoPackage (extrahiert via BBBike/Overpass)
2. Filterung auf ausschließlich `railway=rail`-Features
3. Umprojektion in ein metrisches Koordinatensystem (ETRS89 / UTM Zone 32N) für exakte Distanzberechnungen
4. Pufferung der Bahnlinien um einen konfigurierbaren Sicherheitsabstand (aufgelöst/dissolved)
5. Laden der Gebäudepolygone aus derselben Quelle
6. Korrektur ungültiger Geometrien (häufig bei OSM-Gebäudeumrissen)
7. Auswahl der Gebäude, die den Sicherheitspuffer schneiden/überlappen
8. Export der betroffenen Gebäude in ein neues GeoPackage

### Voraussetzungen

- Installiertes QGIS (getestet mit QGIS 3.44 "Solothurn")
- Ausführung mit dem in QGIS enthaltenen Python-Interpreter (OSGeo4W-Shell unter Windows bzw. die QGIS-Python-Umgebung unter Linux/macOS)

### Verwendung

```bash
python rail_safety_zone_analysis.py
```

Passe den Pfad zum Eingabe-GeoPackage und den Pufferabstand am Anfang des Skripts an deine Daten und Sicherheitsanforderungen an.

### Ausgabe

Ein neues GeoPackage, das nur die Gebäude enthält, die innerhalb des konfigurierten Sicherheitspuffers um die Bahnlinien liegen.

