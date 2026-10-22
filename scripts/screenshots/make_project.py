"""Writes <data>/ev_plate.evaproj for the plate made by make_plate.py.

Three spot pipelines (CY7, CY5, FITC: Rolling Ball -> Blur -> Blur ->
Threshold -> Connected Components -> Watershed -> Extract Objects ->
Classify Objects) and a colocalization pipeline (CY5 x FITC). Every image
gets a display range and shows CY5 + FITC only, so the screenshots look like
real single-EV imaging instead of auto-scaled noise.

The JSON follows the project format of the ai-plugin branch (schema 4,
`components`); if the app changes the format, adapt `step()` below.

    python3 make_project.py /data/ev_plate
"""
import glob
import json
import os
import sys

data = sys.argv[1]

CLASSES = [
    (0, "#97978f", "Background"), (1, "#ff4d4d", "cy7@spot"), (2, "#ff33ff", "cy5@spot"),
    (3, "#33ff66", "fitc@spot"), (4, "#ffd200", "coloc@cy5_fitc"), (5, "#33cfff", "tetraspeck@bead"),
]
CHANNELS = ["CY7", "CY5", "FITC", "Tetraspeck"]
EMISSION = [773.0, 670.0, 520.0, 590.0]
# Display range per channel, in 16 bit values.
RANGE = {0: (380, 1500), 1: (450, 1700), 2: (520, 1900), 3: (560, 9000)}
MAX_U16 = 65535.0


def spot_steps(cls, threshold):
    big = 2147483600.0
    commands = [
        {"type": "ROLLING_BALL", "radius": 4.0, "ballType": "PARABOLOID", "preSmooth": False},
        {"type": "BLUR", "kernelSize": 3},
        {"type": "BLUR", "kernelSize": 3},
        {"type": "THRESHOLD", "thresholds": [{
            "method": {"type": "MANUAL"}, "minThreshold": threshold, "maxThreshold": 65535.0,
            "unit": "BIT", "segmentationClass": cls, "valueSource": "ACTUAL_IMAGE"}]},
        {"type": "CONNECTED_COMPONENTS", "minSize": 0},
        {"type": "WATERSHED", "maximumFinderTolerance": 0.5, "smoothingSigma": 0.0,
         "minObjectSize": 0, "seedSource": "DISTANCE_MAP"},
        {"type": "EXTRACT_OBJECTS", "maxObjectsBeforeFail": 100000, "classMapping": []},
        {"type": "CLASSIFY_OBJECTS", "originSegmentation": [], "inputClasses": [{"GLOBAL": cls}],
         "matchHandling": "REMOVE_ALL_CLASSES_IF_NOT_MATCH", "outputClass": "UNSET",
         "overlappingWith": "UNSET", "minIntersectionArea": 0.0, "sizeUnit": "PIXELS",
         "minArea": 5.0, "maxArea": big, "minCircularity": 0.0, "maxCircularity": 1.0,
         "minSolidity": 0.0, "maxSolidity": 1.0, "minAspectRatio": 0.0, "maxAspectRatio": big,
         "minEccentricity": 0.0, "maxEccentricity": 1.0, "minFeret": 0.0, "maxFeret": big,
         "allowEdgeTouching": True, "intensityFilters": []},
    ]
    return [{"id": i + 1, "enabled": True, "command": c} for i, c in enumerate(commands)]


def spot_pipeline(pid, name, channel, cls):
    return {"id": pid, "name": name, "description": "", "imageSource": {"channel": channel},
            "enabled": True, "steps": spot_steps(cls, 250.0)}


coloc = {
    "id": 4, "name": "Coloc CY5 + FITC", "description": "", "imageSource": "SCRATCHPAD", "enabled": True,
    "steps": [{"id": 1, "enabled": True, "command": {
        "type": "COLOCALIZATION", "classesToColoc": [{"GLOBAL": 2}, {"GLOBAL": 3}], "filterClasses": [],
        "classForOverlappingAreas": {"GLOBAL": 4}, "multiplicity": "MANY_TO_MANY",
        "sizeUnit": "PIXELS", "minColocArea": 0.0, "excludeClasses": []}}],
}

images = {}
for path in sorted(glob.glob(os.path.join(data, "*.ome.tif"))):
    rel = os.path.basename(path)
    channels = {}
    for c, name in enumerate(CHANNELS):
        lo, hi = RANGE[c]
        channels[str(c)] = {
            "name": name, "emissionWaveLength": EMISSION[c], "visible": c in (1, 2),
            "histogram": {"min": lo / MAX_U16, "max": hi / MAX_U16, "minLimit": 0.0, "maxLimit": 3000 / MAX_U16},
        }
    images[rel] = {
        "relPath": rel, "fileSize": os.path.getsize(path), "selectedSeries": 0,
        "series": {"0": {"selectedChannel": None, "channels": channels, "imageWidth": 768, "imageHeight": 768,
                         "pixelSizes": {"x": 108.0, "y": 108.0, "z": 0.0}, "zStack": None, "tStack": None,
                         "objects": []}},
    }

project = {
    "schemaVersion": 4,
    "meta": {"name": "EV plate", "shortDescription": "", "description": "",
             "authors": [{"fullName": "EVAnalyzer Team", "organization": "evanalyzer.org"}],
             "creationTime": "2026-10-21T00:00:00Z", "category": "", "tags": [], "appVersion": "0.1.0"},
    "classification": {"classes": [{"id": i, "color": c, "name": n, "notes": ""} for i, c, n in CLASSES]},
    "plate": {"groupingMode": "AUTO", "groupingRegex": "", "plateSize": "AUTO", "wellLayout": "AUTO",
              "wellImageOrder": []},
    "tileMerge": {"enabled": True, "classesToNotMerge": [], "connectivity": "EIGHT_CONNECTED",
                  "maxFragmentsPerGroup": 10000},
    "images": {"root": data, "list": images,
               "settings": {"selectedSeries": None, "grayscale": False, "selectedChannel": None, "channels": {},
                            "pixelSizes": None, "zStack": None, "tStack": None}},
    "pipelines": [spot_pipeline(1, "CY7 spots", 0, 1), spot_pipeline(2, "CY5 spots", 1, 2),
                  spot_pipeline(3, "FITC spots", 2, 3), coloc],
    "components": [],
}
out = os.path.join(data, "ev_plate.evaproj")
with open(out, "w") as f:
    json.dump(project, f, indent=2)
print(out)
