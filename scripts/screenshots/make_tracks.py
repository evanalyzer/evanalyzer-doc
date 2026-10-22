"""Synthetic time-lapse for the Tracks screenshots, and its project.

Two fields (A01_01, A02_01), 15 frames 30 s apart, 512 x 512 px, one GFP
channel: vesicles that drift and wander, some leave or enter at the edges.
The project detects them and links them with a Simple Tracker step.

    python3 make_tracks.py /data/ev_tracks
"""
import json
import os
import sys

import numpy as np
import tifffile

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
N, T, SIGMA = 512, 15, 2.2
yy, xx = np.mgrid[0:N, 0:N]


def frame(rng, pts, amps):
    img = np.zeros((N, N), np.float32)
    r = int(4 * SIGMA) + 1
    k = np.arange(-r, r + 1)
    for (x, y), a in zip(pts, amps):
        xi, yi = int(x), int(y)
        if xi < r or yi < r or xi >= N - r or yi >= N - r:
            continue
        gx = np.exp(-((k + xi - x) ** 2) / (2 * SIGMA**2))
        gy = np.exp(-((k + yi - y) ** 2) / (2 * SIGMA**2))
        img[yi - r:yi + r + 1, xi - r:xi + r + 1] += a * np.outer(gy, gx)
    return img


for field, (name, n, drift) in enumerate([("A01_01", 70, (2.5, 1.0)), ("A02_01", 90, (-1.5, 2.0))]):
    rng = np.random.default_rng(100 + field)
    pos = rng.random((n, 2)) * N
    # Each vesicle: directed (fast, straight) or diffusing (slow, wandering).
    directed = rng.random(n) < 0.45
    vel = np.where(directed[:, None], np.array(drift) * rng.uniform(1.5, 3.0, (n, 1)), 0.0)
    amps = rng.lognormal(np.log(2200), 0.35, n)
    frames = []
    for t in range(T):
        frames.append(frame(rng, pos, amps))
        step = rng.normal(0, np.where(directed, 0.8, 2.2)[:, None], (n, 2))
        pos = pos + vel + step
    stack = np.stack(frames)
    bg = 300 + 40 * np.sin(xx / 90.0)
    data = rng.poisson(np.maximum(stack + bg, 0)).astype(np.float32) + rng.normal(0, 15, stack.shape)
    data = np.clip(data, 0, 65535).astype(np.uint16)[:, None]  # T, C, Y, X
    tifffile.imwrite(
        os.path.join(out, f"{name}.ome.tif"), data, photometric="minisblack",
        metadata={"axes": "TCYX", "PhysicalSizeX": 0.108, "PhysicalSizeXUnit": "µm",
                  "PhysicalSizeY": 0.108, "PhysicalSizeYUnit": "µm",
                  "TimeIncrement": 30.0, "TimeIncrementUnit": "s",
                  "Channel": {"Name": ["GFP"], "EmissionWavelength": [520.0]}},
    )

big = 2147483600.0
commands = [
    {"type": "BLUR", "kernelSize": 3},
    {"type": "THRESHOLD", "thresholds": [{
        "method": {"type": "MANUAL"}, "minThreshold": 900.0, "maxThreshold": 65535.0,
        "unit": "BIT", "segmentationClass": 1, "valueSource": "ACTUAL_IMAGE"}]},
    {"type": "CONNECTED_COMPONENTS", "minSize": 0},
    {"type": "EXTRACT_OBJECTS", "maxObjectsBeforeFail": 100000, "classMapping": []},
    {"type": "CLASSIFY_OBJECTS", "originSegmentation": [], "inputClasses": [{"GLOBAL": 1}],
     "matchHandling": "REMOVE_ALL_CLASSES_IF_NOT_MATCH", "outputClass": "UNSET", "overlappingWith": "UNSET",
     "minIntersectionArea": 0.0, "sizeUnit": "PIXELS", "minArea": 8.0, "maxArea": big,
     "minCircularity": 0.0, "maxCircularity": 1.0, "minSolidity": 0.0, "maxSolidity": 1.0,
     "minAspectRatio": 0.0, "maxAspectRatio": big, "minEccentricity": 0.0, "maxEccentricity": 1.0,
     "minFeret": 0.0, "maxFeret": big, "allowEdgeTouching": True, "intensityFilters": []},
    {"type": "SIMPLE_TRACKER", "objectClass": {"GLOBAL": 1}, "unit": "PIXELS", "maxDistance": 12.0},
]
project = {
    "schemaVersion": 4,
    "meta": {"name": "EV tracks", "shortDescription": "", "description": "",
             "authors": [{"fullName": "EVAnalyzer Team", "organization": "evanalyzer.org"}],
             "creationTime": "2026-10-22T00:00:00Z", "category": "", "tags": [], "appVersion": "0.1.0"},
    "classification": {"classes": [
        {"id": 0, "color": "#97978f", "name": "Background", "notes": ""},
        {"id": 1, "color": "#33ff66", "name": "gfp@vesicle", "notes": ""}]},
    "plate": {"groupingMode": "AUTO", "groupingRegex": "", "plateSize": "AUTO", "wellLayout": "AUTO",
              "wellImageOrder": []},
    "tileMerge": {"enabled": True, "classesToNotMerge": [], "connectivity": "EIGHT_CONNECTED",
                  "maxFragmentsPerGroup": 10000},
    "images": {"root": out, "list": {},
               "settings": {"selectedSeries": None, "grayscale": False, "selectedChannel": None, "channels": {},
                            "pixelSizes": None, "zStack": None,
                            # Every frame analysed (the default is one), 30 s apart.
                            "tStack": {"stackHandling": "ALL_STACKS", "playbackSpeed": 2.0, "tStack": 0,
                                       "frameInterval": 30.0}}},
    "pipelines": [{"id": 1, "name": "GFP vesicles", "description": "", "imageSource": {"channel": 0},
                   "enabled": True,
                   "steps": [{"id": i + 1, "enabled": True, "command": c} for i, c in enumerate(commands)]}],
    "modules": [],
}
with open(os.path.join(out, "ev_tracks.evaproj"), "w") as f:
    json.dump(project, f, indent=2)
print(os.path.join(out, "ev_tracks.evaproj"))
