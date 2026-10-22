---
title: "Example Vitra"
description: "Ported from CellProfiler ExampleVitra pipeline (nucleus/cytoplasm protein translocation)"
category: template
file: /downloads/templates/project_templates/cp_example_vitra/example_vitra.evatemplate
fileSize: "13 KB"
bundleFile: /downloads/templates/project_templates/cp_example_vitra/example_vitra-with-images.zip
bundleSize: "2.87 MB"
tags: ["translocation", "nucleus", "cytoplasm", "cellprofiler"]
---

Nucleus/cytoplasm protein translocation assay (BBBC014), ported from CellProfiler's ExampleVitra.cppipe. Input: one 4-channel TIFF per well in images/ (Fiji merge): ch0 = DNA ("Channel 2-*"), ch1 = protein ("Channel 1-*"), ch2 = 1/VitraChannel2ILLUM, ch3 = 1/VitraChannel1ILLUM. CP divides by precomputed illumination functions (.npy, 1.0-2.0 across the field) which evanalyzer cannot load, so the inverse functions are stored as 8-bit extra channels (round(255/f), <0.4 % error) and applied with Image Math MULTIPLY - same correction as CP, not re-estimated.
Nuclei: LI (= CP Minimum Cross-Entropy) threshold computed on the corrected, unsmoothed image (Image Cache + value source) and applied to a sigma-1 Gaussian blur (CP threshold smoothing 1.3488), fill holes, intensity-seeded watershed with CP's automatic values for 5-30 px diameter (maxima suppression 3.33 px, total smoothing sigma 1.43 = 1.0 + 1.02 in quadrature), area 19.6-706.9 px (diameter range), border objects discarded. Threshold mask agrees with CP on 99.7 % of pixels.
Cells (CP Distance-B, 8 px): protein foreground = LI threshold of corrected protein; cell region = (nuclei dilated 8 px AND protein foreground) OR nuclei; Voronoi from the nuclei inside that region. Cytoplasm = cells minus nuclei eroded by 1 px (CP 'shrink smaller object').
Result vs CP: about 22 % fewer nuclei (577/619 vs 744/782). Evanalyzer's watershed (seeds from intensity, flood on the distance map with 1 px lines) leaves 13-15 dense clumps per image unsplit, which then fail the 30 px diameter limit; lower seed tolerances raise the count but cut single nuclei into fragments. Matched nuclei have about the same area (median eva/CP 0.94-0.95). Cells/cytoplasm of isolated nuclei match CP; in crowded areas they are larger because the missing clump nuclei leave room for their neighbours. The CalculateMath ratios (nucleus/cell and cytoplasm/cell mean protein, computed after export) match closely: median 1.16 vs 1.15 and 1.01 vs 1.03 (nucleus/cell), 0.83 vs 0.80 and 1.00 vs 1.01 (cytoplasm/cell). Evanalyzer measures intensities on raw channels; corrected means were approximated as mean(ch1) x mean(ch3).

## About the example data

In this human cytoplasm-nucleus translocation assay, previously calculated illumination correction functions are applied to two channels, the protein content is measured in the nucleus and the cytoplasm, and the ratio is a measure of translocation.

About these images:

More about these images can be found at the [BBBC](https://data.broadinstitute.org/bbbc/BBBC014/) (BBBC014). One 4-channel TIFF per well: channel 0 = DNA (`Channel 2-*`), channel 1 = protein (`Channel 1-*`), channels 2 and 3 = the inverse of CellProfiler's precomputed illumination functions `VitraChannel2ILLUM.npy` and `VitraChannel1ILLUM.npy` as 8-bit images (round(255/f)), since evanalyzer cannot load `.npy` files.
