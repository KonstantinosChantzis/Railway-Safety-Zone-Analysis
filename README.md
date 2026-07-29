# Bahnstrecken-Sicherheitszone (QGIS + PyQGIS)

Automatisierte räumliche Analyse zur Identifikation von Gebäuden innerhalb
einer Sicherheitszone entlang von Bahnstrecken, auf Basis von
OpenStreetMap-Daten.

## Pipeline

1. Import von OSM-Liniendaten (Bahnstrecken) aus einem GeoPackage
2. Filterung auf `railway = rail`
3. Reprojektion in ein metrisches Koordinatensystem (ETRS89 / UTM Zone 32N)
4. Pufferbildung (konfigurierbare Sicherheitsdistanz, z. B. 50 m), dissolved
5. Import von Gebäude-Polygonen aus derselben Quelle
6. Geometriekorrektur (häufig bei OSM-Gebäudedaten notwendig)
7. Räumliche Selektion: Gebäude, die den Sicherheitspuffer schneiden/überlappen
8. Export der betroffenen Gebäude als neues GeoPackage

## Verwendung

```bash
python-qgis rail_safety_zone_analysis.py input.gpkg output.gpkg --buffer-distance 50
```

Das Eingabe-GeoPackage muss die Layer `lines` und `multipolygons` mit
Standard-OSM-Tags enthalten (z. B. erzeugt über einen Extract von
https://extract.bbbike.org/ oder die Overpass API).

## Technologien

Python (PyQGIS, QGIS Processing Framework), QGIS 3.44, OpenStreetMap-Daten

## Hintergrund

Dieses Projekt entstand als praktisches Lernprojekt zur Vertiefung von
QGIS-Grundlagen (Datenimport, CRS, Pufferanalyse, räumliche Selektion) und
deren Automatisierung mittels PyQGIS – analog zum Ansatz der anderen
Projekte in diesem Portfolio (Python + PostGIS QA-Pipelines).

Datenquelle: © OpenStreetMap-Mitwirkende (https://www.openstreetmap.org/copyright)
