---
title: "Example Illumination Correction 2"
description: "Ported from CellProfiler ExampleIlluminationCorrection_Example2 pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_illumination_correction_2/example_illumination_correction_2.evatemplate
fileSize: "14 KB"
bundleFile: /downloads/templates/project_templates/cp_example_illumination_correction_2/example_illumination_correction_2-with-images.zip
bundleSize: "1.59 MB"
tags: ["illumination-correction", "nuclei", "cellprofiler"]
---

Nuclei (mCherry) found three times: on the raw image, after a too-small background correction (block 8) and after a suitable one (block 20, then Li/Minimum Cross-Entropy threshold). Ported from CellProfiler ExampleIlluminationCorrection_Example2.cppipe. CP's threshold is calculated on the unsmoothed image and applied to a sigma-1 blurred copy (Image Cache + value source). Its 'Intensity' declumping is Watershed with intensity seeds, 14 px maxima suppression (CP's low-res value); seed smoothing sigma 2.85 instead of CP's 5.7 was chosen empirically, it splits touching nuclei closer to CP. evanalyzer's Subtract keeps the image mean while CP subtracts the whole background and clips at 0, and its median smoothing works on the block grid (radius 1 block) instead of CP's full-resolution disk. Result vs CP: uncorrected 40 vs 42 objects, small block 9 vs 21 (CP's extra objects are fragments of 2-53 px), large block 24 vs 30 (objects > 50 px: 23 vs 26, mean area 839 vs 844 px). The example's point - only the large block correction yields proper nuclei - is reproduced.

## About the example data

Illumination correction is often important for both accurate segmentation and for intensity measurements. This example shows how the CorrectIlluminationCalculate and CorrectIlluminationApply modules are used to compensate for the non-uniformities in illumination often present in microscopy images.

This part finds nuclei three times - on the raw image, after a too small and after a suitable background correction - to show how the correction affects segmentation.

About these images:

The image of the CellProfiler example ExampleIlluminationCorrection prefixed with "--W00001--".
