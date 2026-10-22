---
title: "Example Illumination Correction 3"
description: "Ported from CellProfiler ExampleIlluminationCorrection_Example3 pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_illumination_correction_3/example_illumination_correction_3.evatemplate
fileSize: "6.6 KB"
bundleFile: /downloads/templates/project_templates/cp_example_illumination_correction_3/example_illumination_correction_3-with-images.zip
bundleSize: "323 KB"
tags: ["illumination-correction", "worms", "brightfield", "cellprofiler"]
---

Worms in a well (bright-field, dark worms). Ported from CellProfiler ExampleIlluminationCorrection_Example3.cppipe. The well is found with 3-class Otsu (middle class foreground) and shrunk by 5 px; the inverted image is background-corrected with block 2 + polynomial fit and subtracted. Well area 172121 vs CP 172394 px, shrunken well 164654 vs 163852 px. CP restricts the polynomial fit to the shrunken well (MaskImage); evanalyzer cannot mask an image by objects, so the fit uses the whole image - the corrected image still correlates r=0.96 with CP's inside the well. Not ported: the second correction (Regular + Convex Hull smoothing + divide), evanalyzer has no convex-hull smoothing.

## About the example data

Illumination correction is often important for both accurate segmentation and for intensity measurements. This example shows how the CorrectIlluminationCalculate and CorrectIlluminationApply modules are used to compensate for the non-uniformities in illumination often present in microscopy images.

This part finds the well and corrects the uneven background of a bright-field image of worms inside it.

About these images:

The image of the CellProfiler example ExampleIlluminationCorrection prefixed with "ADSAStaphInfection2_".
