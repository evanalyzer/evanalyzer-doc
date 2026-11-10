"""Synthetic neurons for the Trees and Profile (Sholl) screenshots, and their project.

Two fields (A01_01, A02_01), 768 x 768 px of 0.325 µm, two channels: DAPI
(the nuclei - the somata) and MAP2 (soma and branching dendrites). The
project finds the somata in DAPI, thresholds and skeletonizes the dendrites
in MAP2, traces each neuron from its soma (Trace Filaments) and measures the
trees (Measure Filament Tree) and their Sholl profile (Measure Object Sholl).

    python3 make_neurons.py /data/ev_neurons
"""
import json
import math
import os
import sys

import numpy as np
import tifffile
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
N, XY = 768, 0.325                     # px, µm
SS = 2                                 # drawn at twice the size, then binned


def branch(draw, rng, x, y, angle, width, length, depth):
    """A dendrite: a gently curving line that tapers, forking into two."""
    steps = int(length / 4)
    for _ in range(steps):
        angle += rng.normal(0, 0.12)
        nx, ny = x + 4 * math.cos(angle), y + 4 * math.sin(angle)
        draw.line([(x * SS, y * SS), (nx * SS, ny * SS)], fill=255, width=max(2, int(width * SS)))
        x, y = nx, ny
        width = max(1.6, width * 0.985)
        if not (10 < x < N - 10 and 10 < y < N - 10):
            return
    if depth > 0:
        spread = rng.uniform(0.45, 0.8)
        for side in (-1, 1):
            branch(draw, rng, x, y, angle + side * spread, width * 0.8,
                   length * rng.uniform(0.55, 0.85), depth - 1 - (rng.random() < 0.3))


def field(seed, somata):
    rng = np.random.default_rng(seed)
    neur = Image.new("L", (N * SS, N * SS), 0)
    nucl = Image.new("L", (N * SS, N * SS), 0)
    dn, dc = ImageDraw.Draw(neur), ImageDraw.Draw(nucl)
    for cx, cy in somata:
        r = rng.uniform(13, 17)
        dn.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=255)
        rn = r * 0.6
        dc.ellipse([(cx - rn) * SS, (cy - rn) * SS, (cx + rn) * SS, (cy + rn) * SS], fill=255)
        n_primary = int(rng.integers(4, 7))
        start = rng.uniform(0, 2 * math.pi)
        for k in range(n_primary):
            a = start + 2 * math.pi * k / n_primary + rng.normal(0, 0.25)
            branch(dn, rng, cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a), a,
                   rng.uniform(3.2, 4.2), rng.uniform(45, 70), int(rng.integers(2, 4)))

    def binned(img):
        a = np.asarray(img, np.float32) / 255.0
        return a.reshape(N, SS, N, SS).mean(axis=(1, 3))

    map2 = gaussian_filter(binned(neur), 1.0) * 2600
    dapi = gaussian_filter(binned(nucl), 1.5) * 3200
    # A little out-of-focus haze and some debris, so it isn't too clean.
    map2 += gaussian_filter(rng.random((N, N)).astype(np.float32), 25) * 400
    stack = np.stack([dapi, map2]) + 150                       # C, Y, X
    data = rng.poisson(stack).astype(np.float32) + rng.normal(0, 12, stack.shape)
    return np.clip(data, 0, 65535).astype(np.uint16)


FIELDS = {
    "A01_01": (11, [(190, 200), (560, 230), (250, 560), (590, 580)]),
    "A02_01": (12, [(220, 250), (540, 200), (400, 560)]),
}
for name, (seed, somata) in FIELDS.items():
    tifffile.imwrite(
        os.path.join(out, f"{name}.ome.tif"), field(seed, somata), photometric="minisblack",
        metadata={"axes": "CYX", "PhysicalSizeX": XY, "PhysicalSizeXUnit": "µm",
                  "PhysicalSizeY": XY, "PhysicalSizeYUnit": "µm",
                  "Channel": {"Name": ["DAPI", "MAP2"], "EmissionWavelength": [461.0, 520.0]}},
    )

big = 2147483600.0


def classify(cls, min_size):
    return {"type": "CLASSIFY_OBJECTS", "originSegmentation": [], "inputClasses": [{"GLOBAL": cls}],
            "matchHandling": "REMOVE_ALL_CLASSES_IF_NOT_MATCH", "outputClass": "UNSET", "overlappingWith": "UNSET",
            "minIntersectionSize": 0.0, "sizeUnit": "PIXELS", "minSize": min_size, "maxSize": big,
            "minCircularity": 0.0, "maxCircularity": 1.0, "minSolidity": 0.0, "maxSolidity": 1.0,
            "minAspectRatio": 0.0, "maxAspectRatio": big, "minEccentricity": 0.0, "maxEccentricity": 1.0,
            "minFeret": 0.0, "maxFeret": big, "allowEdgeTouching": True, "intensityFilters": []}


def segment(cls, threshold, min_size):
    return [
        {"type": "BLUR", "kernelSize": 3},
        {"type": "THRESHOLD", "thresholds": [{
            "method": {"type": "MANUAL"}, "minThreshold": threshold, "maxThreshold": 65535.0,
            "unit": "BIT", "segmentationClass": cls, "valueSource": "ACTUAL_IMAGE"}]},
        {"type": "CONNECTED_COMPONENTS", "minSize": 0},
        {"type": "EXTRACT_OBJECTS", "maxObjectsBeforeFail": 100000, "classMapping": []},
        classify(cls, min_size),
    ]


SOMA, NEURITE, SKELETON, END, SEGMENT = 1, 2, 3, 4, 5
neurites = segment(NEURITE, 900.0, 400.0) + [
    {"type": "SKELETONIZE_OBJECTS", "inputClass": {"GLOBAL": NEURITE}, "skeletonClass": {"GLOBAL": SKELETON},
     "endPointClass": {"GLOBAL": END}, "branchPointClass": "UNSET",
     "minBranchLength": 6.0, "lengthUnit": "PIXELS"},
    {"type": "RELATE_OBJECTS", "childClasses": [{"GLOBAL": SKELETON}], "parentClasses": [{"GLOBAL": SOMA}],
     "rule": "LARGEST_OVERLAP", "removeWithoutParent": False},
    {"type": "TRACE_FILAMENTS", "seeds": {"GLOBAL": SOMA}, "targets": {"GLOBAL": END},
     "outputClass": {"GLOBAL": SEGMENT}, "channel": 1, "followFibres": True, "minWidth": 2.0,
     "maxWidth": 8.0, "maxReach": 180.0, "minBranchLength": 6.0, "unit": "PIXELS"},
    {"type": "MEASURE_FILAMENT_TREE", "id": "tree_01", "segments": {"GLOBAL": SEGMENT},
     "somata": {"GLOBAL": SOMA}},
    {"type": "MEASURE_OBJECT_SHOLL", "id": "sholl_01", "objects": {"GLOBAL": SKELETON},
     "centreFrom": {"GLOBAL": SOMA}, "ringStep": 15.0, "firstRadius": 0.0, "lastRadius": 0.0,
     "unit": "PIXELS"},
]


def pipeline(pid, name, channel, commands):
    return {"id": pid, "name": name, "description": "", "imageSource": {"channel": channel}, "enabled": True,
            "steps": [{"id": i + 1, "enabled": True, "command": c} for i, c in enumerate(commands)]}


MAX_U16 = 65535.0
RANGE = {0: (250, 2500), 1: (250, 2400)}
channels = {str(c): {"name": n, "emissionWaveLength": w, "visible": True,
                     "histogram": {"min": RANGE[c][0] / MAX_U16, "max": RANGE[c][1] / MAX_U16,
                                   "minLimit": 0.0, "maxLimit": 4000 / MAX_U16}}
            for c, (n, w) in enumerate([("DAPI", 461.0), ("MAP2", 520.0)])}
images = {}
for name in FIELDS:
    rel = f"{name}.ome.tif"
    images[rel] = {"relPath": rel, "fileSize": os.path.getsize(os.path.join(out, rel)), "selectedSeries": 0,
                   "series": {"0": {"selectedChannel": None, "channels": channels, "imageWidth": N,
                                    "imageHeight": N, "pixelSizes": {"x": XY * 1000, "y": XY * 1000, "z": 0},
                                    "zStack": None, "tStack": None, "objects": []}}}

project = {
    "schemaVersion": 4,
    "meta": {"name": "Neurons", "shortDescription": "", "description": "",
             "authors": [{"fullName": "EVAnalyzer Team", "organization": "evanalyzer.org"}],
             "creationTime": "2026-11-10T00:00:00Z", "category": "", "tags": [], "appVersion": "1.1.0"},
    "classification": {"classes": [
        {"id": 0, "color": "#97978f", "name": "Background", "notes": ""},
        {"id": SOMA, "color": "#3d7bff", "name": "dapi@soma", "notes": ""},
        {"id": NEURITE, "color": "#5f6b73", "name": "map2@neurite", "notes": ""},
        {"id": SKELETON, "color": "#ffd23d", "name": "map2@skeleton", "notes": ""},
        {"id": END, "color": "#ff7a2f", "name": "map2@tip", "notes": ""},
        {"id": SEGMENT, "color": "#33e0a0", "name": "map2@segment", "notes": ""}]},
    "plate": {"groupingMode": "AUTO", "groupingRegex": "", "plateSize": "AUTO", "wellLayout": "AUTO",
              "wellImageOrder": []},
    "tileMerge": {"enabled": True, "classesToNotMerge": [], "connectivity": "EIGHT_CONNECTED",
                  "maxFragmentsPerGroup": 10000},
    "images": {"root": out, "list": images,
               "settings": {"selectedSeries": None, "grayscale": False, "selectedChannel": None, "channels": {},
                            "pixelSizes": None, "zStack": None, "tStack": None}},
    "pipelines": [pipeline(1, "Somata", 0, segment(SOMA, 800.0, 150.0)),
                  pipeline(2, "Neurites", 1, neurites)],
    "modules": [],
}
with open(os.path.join(out, "ev_neurons.evaproj"), "w") as f:
    json.dump(project, f, indent=2)
print(os.path.join(out, "ev_neurons.evaproj"))
