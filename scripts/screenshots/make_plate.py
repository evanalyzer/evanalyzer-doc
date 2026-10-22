"""Synthetic single-EV fluorescence plate for documentation screenshots.

Wells A-D x 1-6, two fields each, 768x768 px, 16 bit, channels CY7 / CY5 /
FITC / Tetraspeck as OME-TIFF. EV density rises across the columns (a
dilution series), the CY5+FITC colocalization fraction rises down the rows.
"""
import sys, os
import numpy as np
import tifffile

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
N = 768
SIGMA = 1.4
names = ["CY7", "CY5", "FITC", "Tetraspeck"]
emission = [773.0, 670.0, 520.0, 590.0]
yy, xx = np.mgrid[0:N, 0:N]
illum = 1.0 - 0.25 * (((xx - N * 0.45) / N) ** 2 + ((yy - N * 0.55) / N) ** 2) * 4


def spot_layer(rng, pts, amps):
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


for ri, row in enumerate("ABCD"):
    for col in range(1, 7):
        for field in (1, 2):
            rng = np.random.default_rng(ri * 100 + col * 10 + field)
            n_ev = int(120 * col * (0.85 + 0.3 * rng.random()))
            coloc = 0.15 + 0.18 * ri
            pts = rng.random((n_ev, 2)) * N
            # which channels each EV is positive in
            in_cy7 = rng.random(n_ev) < 0.55
            in_cy5 = rng.random(n_ev) < 0.6
            in_fitc = np.where(in_cy5, rng.random(n_ev) < coloc + 0.3, rng.random(n_ev) < 0.35)
            beads = rng.random((6, 2)) * N
            chans = []
            for c, mask in enumerate([in_cy7, in_cy5, in_fitc, None]):
                bg = (260 + 60 * c) * illum
                if mask is None:
                    sig = spot_layer(rng, beads, rng.uniform(9000, 14000, len(beads)))
                else:
                    sel = pts[mask] + rng.normal(0, 0.6, (mask.sum(), 2))  # chromatic shift
                    amps = rng.lognormal(np.log(1300), 0.45, mask.sum())
                    sig = spot_layer(rng, sel, amps)
                    sig += spot_layer(rng, beads, rng.uniform(4000, 7000, len(beads)))
                img = rng.poisson(np.maximum(bg + sig, 0)).astype(np.float32)
                img += rng.normal(0, 18, img.shape)
                chans.append(np.clip(img, 0, 65535).astype(np.uint16))
            data = np.stack(chans)
            fn = os.path.join(out, f"{row}{col:02d}_{field:02d}.ome.tif")
            tifffile.imwrite(
                fn, data, photometric="minisblack",
                metadata={
                    "axes": "CYX",
                    "PhysicalSizeX": 0.108, "PhysicalSizeXUnit": "µm",
                    "PhysicalSizeY": 0.108, "PhysicalSizeYUnit": "µm",
                    "Channel": {"Name": names, "EmissionWavelength": emission},
                },
            )
            print(fn, n_ev)
