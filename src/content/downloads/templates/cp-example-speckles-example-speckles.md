---
title: "Example Speckles"
description: "Ported from CellProfiler ExampleSpeckles pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_speckles/example_speckles.evatemplate
fileSize: "10 KB"
bundleFile: /downloads/templates/project_templates/cp_example_speckles/example_speckles-with-images.zip
bundleSize: "2.54 MB"
tags: ["speckles", "foci", "h2ax", "2-channel", "cellprofiler"]
---

H2AX foci (speckles) per nucleus, ported from the CellProfiler ExampleSpeckles.cppipe example. Channel 0 = Hoechst (1-162hrhoe2.tif), channel 1 = H2AX (1-162hrh2ax2.tif), merged into one 2-channel TIFF (images/) with Fiji. Nuclei: Gaussian sigma 1 + Otsu (threshold computed on the raw image, like CP), fill holes, distance-map watershed (tolerance 2), area for 120-300 px diameter, edge objects dropped. Foci: CP's EnhanceOrSuppressFeatures 'Speckles' (size 10) is a white top-hat with a radius-5 disk - built here as Image Cache + grayscale Open (11 px ellipse) + Image Math subtract. Then Robust Background threshold, intensity-seeded watershed (min distance 4), and Object Math AND with the nuclei to keep only the part of each focus inside a nucleus (CP's MaskImage + RelateObjects). Known difference: CP masks the image to the nuclei before thresholding, so its Robust Background statistics only see nuclear pixels; evanalyzer cannot mask an image by objects, so the statistics see the whole image. To compensate, deviations above average was raised from CP's 2.0 to 4.8 (reproduces CP's threshold on this image; will need re-checking on other images). Result vs CP: nuclei 6/6, areas within 1%; foci 157 vs 152, median area 56 vs 54.5 px, per-nucleus foci counts within +-2.

## About the example data

This pipeline shows how to identify smaller objects (foci) within larger objects (nuclei) and how to relate the two, e.g. to count the foci per nucleus.

About these images:

From the CellProfiler example ExampleSpeckles. The two CellProfiler input files (`1-162hrhoe2.tif` = Hoechst, `1-162hrh2ax2.tif` = H2AX) are merged into one 2-channel TIFF: channel 0 = Hoechst, channel 1 = H2AX.
