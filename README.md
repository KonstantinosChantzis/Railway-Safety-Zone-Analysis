Rail Safety Zone Analysis (QGIS + PyQGIS)
English | Deutsch
---
English
Automated spatial analysis to identify buildings located within a safety
buffer along railway lines, based on OpenStreetMap data.
Pipeline
Import OSM line data (railway lines) from a GeoPackage
Filter for `railway = rail`
Reproject to a metric coordinate system (ETRS89 / UTM zone 32N)
Create a buffer (configurable safety distance, e.g. 50 m), dissolved
Import building polygons from the same source
Fix invalid geometries (common in OSM building data)
Spatial selection: buildings intersecting/overlapping the safety buffer
Export the affected buildings as a new GeoPackage
Usage
```bash
python-qgis rail_safety_zone_analysis.py input.gpkg output.gpkg --buffer-distance 50
```
The input GeoPackage must contain `lines` and `multipolygons` layers with
standard OSM tags (e.g. produced via an extract from
https://extract.bbbike.org/ or the Overpass API).
Technologies
Python (PyQGIS, QGIS Processing Framework), QGIS 3.44, OpenStreetMap data
Background
This project started as a hands-on learning exercise to deepen QGIS
fundamentals (data import, CRS, buffer analysis, spatial selection) and
their automation via PyQGIS — following the same approach as the other
projects in this portfolio (Python + PostGIS QA pipelines).
Data source: © OpenStreetMap contributors (https://www.openstreetmap.org/copyright)
---
Deutsch
Automatisierte räumliche Analyse zur Identifikation von Gebäuden innerhalb
einer Sicherheitszone entlang von Bahnstrecken, auf Basis von
OpenStreetMap-Daten.
Pipeline
Import von OSM-Liniendaten (Bahnstrecken) aus einem GeoPackage
Filterung auf `railway = rail`
Reprojektion in ein metrisches Koordinatensystem (ETRS89 / UTM Zone 32N)
Pufferbildung (konfigurierbare Sicherheitsdistanz, z. B. 50 m), dissolved
Import von Gebäude-Polygonen aus derselben Quelle
Geometriekorrektur (häufig bei OSM-Gebäudedaten notwendig)
Räumliche Selektion: Gebäude, die den Sicherheitspuffer schneiden/überlappen
Export der betroffenen Gebäude als neues GeoPackage
Verwendung
```bash
python-qgis rail_safety_zone_analysis.py input.gpkg output.gpkg --buffer-distance 50
```
Das Eingabe-GeoPackage muss die Layer `lines` und `multipolygons` mit
Standard-OSM-Tags enthalten (z. B. erzeugt über einen Extract von
https://extract.bbbike.org/ oder die Overpass API).
Technologien
Python (PyQGIS, QGIS Processing Framework), QGIS 3.44, OpenStreetMap-Daten
Hintergrund
Dieses Projekt entstand als praktisches Lernprojekt zur Vertiefung von
QGIS-Grundlagen (Datenimport, CRS, Pufferanalyse, räumliche Selektion) und
deren Automatisierung mittels PyQGIS – analog zum Ansatz der anderen
Projekte in diesem Portfolio (Python + PostGIS QA-Pipelines).
Datenquelle: © OpenStreetMap-Mitwirkende (https://www.openstreetmap.org/copyright)
