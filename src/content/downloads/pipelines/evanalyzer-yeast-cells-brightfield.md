---
title: "Yeast cells brightfield"
description: "Yeast cells brightfield"
category: pipeline
file: /downloads/templates/pipeline_templates/evanalyzer/yeast_cells_brightfield.evapipe
fileSize: "2.3 KB"
---

Segments yeast cells from a brightfield image using contrast enhancement, Gaussian blur, Canny edge detection, manual thresholding and a Voronoi tessellation around detected cell centers. The output object class can be remapped after import (default class id used during conversion: 4). The Hough-transform cell-center detection of the original pipeline is approximated by Connected Components on the thresholded edges; the detected objects (class 1) are used as Voronoi centers.

**Contributed by:** Melanie Schuerz (University of Salzburg)
