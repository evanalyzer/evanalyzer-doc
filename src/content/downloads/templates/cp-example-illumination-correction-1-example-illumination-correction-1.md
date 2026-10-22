---
title: "Example Illumination Correction 1"
description: "Ported from CellProfiler ExampleIlluminationCorrection_Example1_EachMethod pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_illumination_correction_1/example_illumination_correction_1.evatemplate
fileSize: "2.3 KB"
bundleFile: /downloads/templates/project_templates/cp_example_illumination_correction_1/example_illumination_correction_1-with-images.zip
bundleSize: "216 KB"
tags: ["illumination-correction", "transfluor", "cellprofiler"]
---

Illumination correction of one Transfluor GFP image: Regular method, median smoothing, divide. Ported from CellProfiler ExampleIlluminationCorrection_Example1_EachMethod.cppipe. CP's median filter size 40 is a disk of radius 17 px at full resolution; here block size 1 + median radius 17 (square window). The corrected image (Save Image) correlates r=0.99 with CP's. Example1_AllMethod (one function averaged over all 72 images) is not ported: evanalyzer calculates the correction per image.

## About the example data

Illumination correction is often important for both accurate segmentation and for intensity measurements. This example shows how the CorrectIlluminationCalculate and CorrectIlluminationApply modules are used to compensate for the non-uniformities in illumination often present in microscopy images.

This part corrects each image with its own illumination function (Regular method, median smoothing, divide).

About these images:

The GFP channel from the SBS Roche Transfluor image set, available from http://www.broadinstitute.org/bbbc/sbs_roche_transfluor.html.
