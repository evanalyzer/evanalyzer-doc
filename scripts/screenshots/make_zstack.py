"""Synthetic z-stack for the orthogonal-views and 3D-view screenshots.

One field, 48 planes 0.4 µm apart, 512 x 512 px of 0.2 µm, two channels:
round cells (DAPI-like nuclei, CY5-like cytoplasm rim) at different depths,
and a tilted fibre crossing the volume - so the XZ / YZ views and the 3D
view have something with depth to show. Plus a project of just that folder.

    python3 make_zstack.py /data/ev_zstack
"""
import json
import os
import sys

import numpy as np
import tifffile

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
Z, N = 48, 512
XY, DZ = 0.2, 0.4                      # µm
rng = np.random.default_rng(7)
zz, yy, xx = np.mgrid[0:Z, 0:N, 0:N].astype(np.float32)
zz_um, yy_um, xx_um = zz * DZ, yy * XY, xx * XY

nuc = np.zeros((Z, N, N), np.float32)
cyto = np.zeros((Z, N, N), np.float32)
for _ in range(16):
    cx, cy = rng.uniform(8, N * XY - 8, 2)
    cz = rng.uniform(5, Z * DZ - 5)
    r = rng.uniform(2.4, 3.4)
    d = np.sqrt((xx_um - cx) ** 2 + (yy_um - cy) ** 2 + ((zz_um - cz) * 1.3) ** 2)
    nuc += rng.uniform(2500, 4000) / (1 + np.exp(np.minimum((d - r) / 0.35, 50)))
    rim = np.exp(-((d - 1.8 * r) ** 2) / (2 * 0.9 ** 2))
    cyto += rng.uniform(1200, 2000) * rim

# A fibre from one corner, rising through the stack.
p0, p1 = np.array([5.0, 10.0, 2.0]), np.array([N * XY - 5, N * XY - 20, Z * DZ - 2])
v = (p1 - p0) / np.linalg.norm(p1 - p0)
rel = np.stack([xx_um - p0[0], yy_um - p0[1], zz_um - p0[2]])
along = np.tensordot(v, rel, axes=1)
perp = np.sqrt(np.maximum((rel ** 2).sum(0) - along ** 2, 0))
cyto += 2600 * np.exp(-(perp ** 2) / (2 * 0.6 ** 2))

stack = np.stack([nuc, cyto], axis=1) + 120        # Z, C, Y, X
data = rng.poisson(stack).astype(np.float32) + rng.normal(0, 4, stack.shape)
data = np.clip(data, 0, 65535).astype(np.uint16)
tifffile.imwrite(
    os.path.join(out, "cells_z.ome.tif"), data, photometric="minisblack",
    metadata={"axes": "ZCYX", "PhysicalSizeX": XY, "PhysicalSizeXUnit": "µm",
              "PhysicalSizeY": XY, "PhysicalSizeYUnit": "µm",
              "PhysicalSizeZ": DZ, "PhysicalSizeZUnit": "µm",
              "Channel": {"Name": ["DAPI", "CY5"], "EmissionWavelength": [461.0, 670.0]}},
)

# A display range per channel (as make_project.py), so the background is black.
MAX_U16 = 65535.0
RANGE = {0: (300, 3000), 1: (250, 3200)}
channels = {str(c): {"name": n, "emissionWaveLength": w, "visible": True,
                     "histogram": {"min": RANGE[c][0] / MAX_U16, "max": RANGE[c][1] / MAX_U16,
                                   "minLimit": 0.0, "maxLimit": 4500 / MAX_U16}}
            for c, (n, w) in enumerate([("DAPI", 461.0), ("CY5", 670.0)])}
rel = "cells_z.ome.tif"
images = {rel: {"relPath": rel, "fileSize": os.path.getsize(os.path.join(out, rel)), "selectedSeries": 0,
                "series": {"0": {"selectedChannel": None, "channels": channels, "imageWidth": N, "imageHeight": N,
                                 "pixelSizes": {"x": XY * 1000, "y": XY * 1000, "z": DZ * 1000},
                                 "zStack": None, "tStack": None, "objects": []}}}}

project = {
    "schemaVersion": 4,
    "meta": {"name": "Z-stack", "shortDescription": "", "description": "",
             "authors": [{"fullName": "EVAnalyzer Team", "organization": "evanalyzer.org"}],
             "creationTime": "2026-11-10T00:00:00Z", "category": "", "tags": [], "appVersion": "1.1.0"},
    "classification": {"classes": [{"id": 0, "color": "#97978f", "name": "Background", "notes": ""}]},
    "plate": {"groupingMode": "AUTO", "groupingRegex": "", "plateSize": "AUTO", "wellLayout": "AUTO",
              "wellImageOrder": []},
    "tileMerge": {"enabled": True, "classesToNotMerge": [], "connectivity": "EIGHT_CONNECTED",
                  "maxFragmentsPerGroup": 10000},
    "images": {"root": out, "list": images,
               "settings": {"selectedSeries": None, "grayscale": False, "selectedChannel": None, "channels": {},
                            "pixelSizes": None, "zStack": None, "tStack": None}},
    "pipelines": [],
    "modules": [],
}
with open(os.path.join(out, "ev_zstack.evaproj"), "w") as f:
    json.dump(project, f, indent=2)
print(os.path.join(out, "ev_zstack.evaproj"))
