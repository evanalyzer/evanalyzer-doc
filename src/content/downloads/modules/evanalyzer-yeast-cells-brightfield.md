---
title: "Yeast cells brightfield"
description: "Yeast cells brightfield"
category: module
file: /downloads/templates/module_templates/evanalyzer/yeast_cells_brightfield.evamodule
fileSize: "3.9 KB"
---

Segments yeast cells from a brightfield image using contrast enhancement, Gaussian blur, Canny edge detection, manual thresholding and a Voronoi tessellation around detected cell centers. The class the cells get is the module's "Yeast cells" parameter. The Hough-transform cell-center detection of the original pipeline is approximated by Connected Components on the thresholded edges; the detected objects (the component's own class "Cell centers") are used as Voronoi centers.

**Contributed by:** Melanie Schuerz (University of Salzburg)
