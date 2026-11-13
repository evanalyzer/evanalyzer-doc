---
title: "Spot detection"
description: "Spots as local maxima (Imaris-style)"
category: module
file: /downloads/templates/module_templates/evanalyzer/spot_detection.evamodule
fileSize: "5.8 KB"
tags: ["spot", "maxima", "imaris"]
---

Detects small, roughly round spots (EVs, vesicles, smFISH dots, foci) like Imaris "Spots": a strongly blurred copy of the image (background) is subtracted from a copy smoothed at the spot size (difference of Gaussians), every local maximum within the spot radius becomes one spot, maxima at or below the quality cut-off are dropped, and each spot is drawn as a circle of fixed diameter. Unlike threshold-based detection, touching spots stay separate and the result doesn't depend on a per-image threshold. The class the spots get is the module's "Spots" parameter. The sigmas, radius and diameter don't follow each other automatically - when spots are larger, raise all of them together (spot diameter d in px: small sigma about 0.35 x d, large sigma about 1.6 x small sigma, radius about d/2). With quality cut-off Otsu, "Min quality" stays the lowest cut-off, so empty images don't produce spots.

**Contributed by:** Joachim Danmayr
