---
title: "Cellpose-SAM (Cellpose defaults)"
description: "Cell segmentation with Cellpose-SAM, set up to match the Cellpose Python package"
category: pipeline
file: /downloads/templates/pipeline_templates/evanalyzer/cellpose_sam.evapipe
fileSize: "3.0 KB"
---

Segments cells with a Cellpose-SAM model (select the exported .pt file in the Cellpose step; the model must be exported with --channels 3, see docs/convert_cellpose.py). The steps reproduce what the Cellpose Python package does: the image is stretched so the 1st percentile becomes 0 and the 99th becomes 1 (Enhance Contrast, saturated pixels 2 % = 1 % per side; computed per analysis tile, Cellpose uses the whole image), the gray image goes into all three model channels, objects are built from the flows like Cellpose (seed-based masks), holes inside each object are filled (Fill Object Holes), and objects whose shape does not match the predicted flows are removed (flow threshold 0.4). For RGB images, add a Color Filter step first to get a gray image. The Cellpose web demo additionally shrinks images to 1000 px (set 'max resize' to 1000) and uses 250 iterations. The disabled last step removes very large objects (Cellpose removes objects above 40 % of the image); set its maximum area for your images and enable it if needed.

**Contributed by:** Joachim Danmayr (University of Salzburg)
