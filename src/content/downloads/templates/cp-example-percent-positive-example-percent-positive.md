---
title: "Example Percent Positive"
description: "Ported from CellProfiler ExamplePercentPositive pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_percent_positive/example_percent_positive.evatemplate
fileSize: "11 KB"
bundleFile: /downloads/templates/project_templates/cp_example_percent_positive/example_percent_positive-with-images.zip
bundleSize: "184 KB"
tags: ["percent-positive", "mitosis", "2-channel", "cellprofiler"]
---

Two-channel percent-positive assay (HT29 cells, DNA + phospho-histone H3 mitosis marker). Ported from the CellProfiler ExamplePercentPositive.cppipe example. Channel 0 = OrigBlue/DNA (files *d0.tif), channel 1 = OrigGreen/PH3 (files *d1.tif), merged into one 2-channel TIFF per site via Fiji (images/). Mapping: IdentifyPrimaryObjects -> Gaussian blur (sigma 1.0 = CP threshold smoothing scale 1.3488/0.6744/2) + Threshold computed on the raw image (LI = Minimum Cross-Entropy for nuclei; 3-class Otsu, middle class foreground, lower bound 0.05 for PH3) + connected components + watershed (Shape -> distance-map seeds, Intensity -> intensity seeds with CP's maxima-suppression radius min-diameter/1.5 and the effective sigma 2.83 of CP's truncated 10-px smoothing kernel) + fill object holes (CP: after declumping only) + area filter from the typical diameter (pi*d^2/4) with border objects discarded. RelateObjects + FilterObjects(Children_PH3_Count >= 1) -> class ph3_pos_nuclei (nuclei overlapping a ph3 object). ClassifyObjects(MaxIntensity_OrigGreen > 0.2) -> class ph3_pos_by_intensity. CalculateMath (percent positive) has no pipeline equivalent: compute it after export as count(ph3_pos_nuclei) / count(nuclei) * 100. Result vs CP 4.2.8: nuclei 281 vs 280 (median area 115 vs 118.5 px), PH3 19 vs 20 (median 91 vs 94.5 px), PH3-positive nuclei 20 vs 20, percent positive 7.12 % vs 7.14 %, positive by max intensity 7.47 % vs 7.50 %. Remaining deviations: evanalyzer's distance-map watershed (prominence-based) splits a few large nucleus clumps that CP keeps whole (largest nucleus 354 vs 471 px), and splits one large PH3 object CP keeps whole (largest 121 vs 191 px); CP's 3-class Otsu uses a 128-bin histogram.

## About the example data

Percentage of nuclei that are positive for the mitotic marker phospho-histone H3 (PH3) in HT29 cells.

About these images:

Image from Jason's mitotic index experiment (CellProfiler example ExamplePercentPositive). The two CellProfiler input files (`*d0.tif` = DNA, `*d1.tif` = PH3) are merged into one 2-channel TIFF: channel 0 = DNA, channel 1 = PH3.
