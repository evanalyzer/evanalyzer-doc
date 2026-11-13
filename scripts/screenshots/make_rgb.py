"""Synthetic H&E-like colour image for the colour-image screenshots.

One RGB field (8 bit, 1024 x 768 px of 0.5 µm): pink eosin tissue with
fibres, white gaps, and purple hematoxylin nuclei - so the Image panel shows
"RGB · 3 channels" and Color Filter has a purple range to pick. Plus a
project of that folder with one pipeline: Color Filter on the nuclei'
purple, then Color to Grayscale.

    python3 make_rgb.py /data/ev_rgb
"""
import json
import os
import sys

import numpy as np
import tifffile

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
W, H, XY = 1024, 768, 0.5
rng = np.random.default_rng(11)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def smooth_noise(scale, seed):
    r = np.random.default_rng(seed)
    small = r.random((H // scale + 2, W // scale + 2)).astype(np.float32)
    ys, xs = np.linspace(0, small.shape[0] - 2, H), np.linspace(0, small.shape[1] - 2, W)
    y0, x0 = ys.astype(int), xs.astype(int)
    fy, fx = (ys - y0)[:, None], (xs - x0)[None, :]
    a, b = small[y0][:, x0], small[y0][:, x0 + 1]
    c, d = small[y0 + 1][:, x0], small[y0 + 1][:, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


# Tissue density: eosin where > 0, white gaps (lumen) elsewhere.
tissue = smooth_noise(160, 1) * 0.7 + smooth_noise(40, 2) * 0.3
eosin = np.clip((tissue - 0.32) * 3.0, 0, 1)
eosin *= 0.75 + 0.25 * np.sin((xx * 0.7 + yy * 0.3) / 9.0 + smooth_noise(60, 3) * 6) ** 2  # fibres

hema = np.zeros((H, W), np.float32)
for _ in range(140):
    cx, cy = rng.uniform(10, W - 10), rng.uniform(10, H - 10)
    if eosin[int(cy), int(cx)] < 0.25:
        continue
    a, b = rng.uniform(7, 12), rng.uniform(5, 9)
    t = rng.uniform(0, np.pi)
    dx, dy = xx - cx, yy - cy
    u, v = dx * np.cos(t) + dy * np.sin(t), -dx * np.sin(t) + dy * np.cos(t)
    d = np.sqrt((u / a) ** 2 + (v / b) ** 2)
    hema = np.maximum(hema, rng.uniform(0.75, 1.0) / (1 + np.exp(np.minimum((d - 1) / 0.12, 50))))

# Beer-Lambert with H&E stain vectors (OD of R, G, B).
H_OD, E_OD = np.array([0.65, 0.70, 0.29]) * 1.6, np.array([0.07, 0.99, 0.11]) * 0.55
od = hema[..., None] * H_OD + eosin[..., None] * E_OD
rgb = 245 * np.exp(-od) + rng.normal(0, 3, (H, W, 3))
rgb = np.clip(rgb, 0, 255).astype(np.uint8)
name = "he_section.tif"
tifffile.imwrite(os.path.join(out, name), rgb, photometric="rgb",
                 resolution=(1e4 / XY, 1e4 / XY), resolutionunit="CENTIMETER")

project = {
    "schemaVersion": 4,
    "meta": {"name": "H&E section", "shortDescription": "", "description": "",
             "authors": [{"fullName": "EVAnalyzer Team", "organization": "evanalyzer.org"}],
             "creationTime": "2026-11-11T00:00:00Z", "category": "", "tags": [], "appVersion": "1.1.0"},
    "classification": {"classes": [{"id": 0, "color": "#97978f", "name": "Background", "notes": ""},
                                   {"id": 1, "color": "#7b4bd6", "name": "he@nucleus", "notes": ""}]},
    "plate": {"groupingMode": "AUTO", "groupingRegex": "", "plateSize": "AUTO", "wellLayout": "AUTO",
              "wellImageOrder": []},
    "tileMerge": {"enabled": True, "classesToNotMerge": [], "connectivity": "EIGHT_CONNECTED",
                  "maxFragmentsPerGroup": 10000},
    "images": {"root": out, "list": {},
               "settings": {"selectedSeries": None, "grayscale": False, "selectedChannel": None, "channels": {},
                            "pixelSizes": None, "zStack": None, "tStack": None}},
    "pipelines": [{
        "id": 1, "name": "Nuclei", "description": "", "imageSource": {"channel": 0}, "enabled": True,
        "steps": [
            {"id": 1, "enabled": True, "command": {"type": "COLOR_FILTER_COMMAND", "range": {
                "minH": 250.0, "maxH": 320.0, "minS": 0.25, "maxS": 1.0, "minV": 0.1, "maxV": 1.0}}},
            {"id": 2, "enabled": True, "command": {"type": "COLOR_TO_GRAYSCALE", "method": "BRIGHTNESS"}},
        ]}],
    "modules": [],
}
with open(os.path.join(out, "ev_rgb.evaproj"), "w") as f:
    json.dump(project, f, indent=2)
print(os.path.join(out, "ev_rgb.evaproj"))
