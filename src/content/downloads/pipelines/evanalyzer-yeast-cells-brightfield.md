---
title: "Yeast cells brightfield"
description: "Yeast cells brightfield"
category: pipeline
file: /downloads/templates/pipeline_templates/evanalyzer/yeast_cells_brightfield.evapipe
fileSize: "2.2 KB"
---

Segments yeast cells from a brightfield image using contrast enhancement, Gaussian blur, Canny edge detection, manual thresholding and a Voronoi tessellation around detected cell centers. The output object class can be remapped after import (default class id used during conversion: 4). Approximation notes: Voronoi centers reference 'M01' (a Hough-transform output label) which has no equivalent class; centers set to UNSET and should be remapped manually $houghTransform has no equivalent in the new schema and was approximated with ConnectedComponents

**Contributed by:** Melanie Schuerz (University of Salzburg)
