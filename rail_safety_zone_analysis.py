"""
Rail Safety Zone Analysis (QGIS / PyQGIS)
==========================================

Automates a spatial safety-buffer analysis around railway lines using
OpenStreetMap data, fully reproducing a manual QGIS workflow as a
repeatable, headless script.

Pipeline:
    1. Load raw OSM line data from a GeoPackage (extracted via BBBike/Overpass)
    2. Filter to keep only railway=rail features
    3. Reproject to a metric CRS (ETRS89 / UTM zone 32N) for accurate distances
    4. Buffer the railway lines by a configurable safety distance (dissolved)
    5. Load building polygons from the same source
    6. Fix invalid geometries (common in OSM building footprints)
    7. Select buildings that intersect/overlap the safety buffer
    8. Export the at-risk buildings to a new GeoPackage

Requirements:
    - QGIS installed (tested on QGIS 3.44 "Solothurn")
    - Run with the Python interpreter bundled with QGIS (OSGeo4W shell on
      Windows, or QGIS's own Python on macOS/Linux), e.g.:

        C:\\PROGRA~1\\QGIS3~1.44\\bin\\python-qgis.bat rail_safety_zone_analysis.py

    - Input: a GeoPackage containing "lines" and "multipolygons" layers,
      as produced by an OSM extract (e.g. from https://extract.bbbike.org/
      or the Overpass API), with standard OSM tag fields (railway, etc.)

Data source:
    OpenStreetMap contributors, https://www.openstreetmap.org/copyright

Author: Konstantinos Chantzis
"""

import argparse
import sys

from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext,
    QgsVectorFileWriter,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Identify buildings within a safety buffer of railway lines."
    )
    parser.add_argument(
        "input_gpkg",
        help="Path to the input GeoPackage (must contain 'lines' and "
             "'multipolygons' layers with OSM tags).",
    )
    parser.add_argument(
        "output_gpkg",
        help="Path where the resulting 'buildings at risk' GeoPackage "
             "will be written.",
    )
    parser.add_argument(
        "--buffer-distance",
        type=float,
        default=50.0,
        help="Safety buffer distance around railway lines, in metres "
             "(default: 50.0).",
    )
    parser.add_argument(
        "--target-crs",
        default="EPSG:25832",
        help="Metric CRS to reproject into before buffering "
             "(default: EPSG:25832, ETRS89 / UTM zone 32N).",
    )
    parser.add_argument(
        "--qgis-prefix-path",
        default=None,
        help="Optional QGIS installation prefix path, only needed if "
             "QgsApplication cannot auto-detect it.",
    )
    return parser.parse_args()


def init_qgis(prefix_path=None):
    """Start a headless QGIS application instance and the Processing framework."""
    qgs = QgsApplication([], False)
    if prefix_path:
        qgs.setPrefixPath(prefix_path, True)
    qgs.initQgis()

    # Processing algorithms (buffer, extract by attribute, etc.) require
    # the Processing plugin to be initialized explicitly in headless mode.
    sys.path.append(qgs.pkgDataPath() + "/python/plugins")
    import processing  # noqa: E402  (import must happen after initQgis)
    from processing.core.Processing import Processing

    Processing.initialize()
    return qgs, processing


def run_analysis(processing, input_gpkg, output_gpkg, buffer_distance, target_crs):
    # --- Step 1: load raw railway line data -------------------------------
    lines_layer = QgsVectorLayer(f"{input_gpkg}|layername=lines", "lines_raw", "ogr")
    if not lines_layer.isValid():
        raise RuntimeError(f"Could not load 'lines' layer from {input_gpkg}")

    # --- Step 2: keep only railway = rail ----------------------------------
    railway_only = processing.run(
        "native:extractbyattribute",
        {
            "INPUT": lines_layer,
            "FIELD": "railway",
            "OPERATOR": 0,  # equals
            "VALUE": "rail",
            "OUTPUT": "memory:",
        },
    )["OUTPUT"]
    print(f"[1/6] Railway segments found: {railway_only.featureCount()}")

    # --- Step 3: reproject to a metric CRS ---------------------------------
    railway_utm = processing.run(
        "native:reprojectlayer",
        {
            "INPUT": railway_only,
            "TARGET_CRS": QgsCoordinateReferenceSystem(target_crs),
            "OUTPUT": "memory:",
        },
    )["OUTPUT"]
    print(f"[2/6] Reprojected to: {railway_utm.crs().authid()}")

    # --- Step 4: buffer (safety zone), dissolved into one polygon ----------
    buffer_layer = processing.run(
        "native:buffer",
        {
            "INPUT": railway_utm,
            "DISTANCE": buffer_distance,
            "SEGMENTS": 5,
            "END_CAP_STYLE": 0,
            "JOIN_STYLE": 0,
            "MITER_LIMIT": 2,
            "DISSOLVE": True,
            "OUTPUT": "memory:",
        },
    )["OUTPUT"]
    print(f"[3/6] Buffer created at {buffer_distance} m "
          f"({buffer_layer.featureCount()} dissolved feature(s))")

    # --- Step 5: load building footprints ----------------------------------
    buildings_layer = QgsVectorLayer(
        f"{input_gpkg}|layername=multipolygons", "buildings_raw", "ogr"
    )
    if not buildings_layer.isValid():
        raise RuntimeError(f"Could not load 'multipolygons' layer from {input_gpkg}")
    print(f"[4/6] Buildings loaded: {buildings_layer.featureCount()}")

    # --- Step 6: fix invalid geometries (common in OSM building data) -----
    buildings_fixed = processing.run(
        "native:fixgeometries", {"INPUT": buildings_layer, "OUTPUT": "memory:"}
    )["OUTPUT"]

    # --- Step 7: select buildings intersecting/overlapping the buffer ------
    buildings_at_risk = processing.run(
        "native:extractbylocation",
        {
            "INPUT": buildings_fixed,
            "PREDICATE": [0, 4],  # intersects, overlaps
            "INTERSECT": buffer_layer,
            "OUTPUT": "memory:",
        },
    )["OUTPUT"]
    print(f"[5/6] Buildings within the safety zone: {buildings_at_risk.featureCount()}")

    # --- Step 8: export result ----------------------------------------------
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "GPKG"
    save_options.fileEncoding = "UTF-8"

    write_result = QgsVectorFileWriter.writeAsVectorFormatV3(
        buildings_at_risk,
        output_gpkg,
        QgsCoordinateTransformContext(),
        save_options,
    )
    error_code = write_result[0]
    error_message = write_result[1]
    if error_code != QgsVectorFileWriter.NoError:
        raise RuntimeError(f"Failed to write output: {error_message}")
    print(f"[6/6] Result written to: {output_gpkg}")


def main():
    args = parse_args()
    qgs, processing = init_qgis(args.qgis_prefix_path)
    try:
        run_analysis(
            processing,
            args.input_gpkg,
            args.output_gpkg,
            args.buffer_distance,
            args.target_crs,
        )
    finally:
        qgs.exitQgis()


if __name__ == "__main__":
    main()
