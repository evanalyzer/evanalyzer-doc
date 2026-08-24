---
title: "Example Comet Assay"
description: "Ported from CellProfiler ExampleCometAssay pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_comet_assay/example_comet_assay.evapt
fileSize: "9.1 KB"
bundleFile: /downloads/templates/project_templates/cp_example_comet_assay/example_comet_assay-with-images.zip
bundleSize: "359 KB"
tags: ["assay", "comet-assay", "cellprofiler"]
---

Single-channel comet assay (DNA damage electrophoresis). Ported from the CellProfiler ExampleCometAssay.cppipe example. Comet = whole cell blob (head+tail), CometHead = dense head sub-region, CometTail = Comet minus CometHead. CP masks the image to Comet before re-thresholding for CometHead (MaskImage) and has no direct evanalyzer equivalent for image-level masking by object class; approximated here with an intersection filter (classifyObjects overlappingWith comet@whole) instead, applied after thresholding the full image. CP's 'Robust Background' threshold method also has no evanalyzer equivalent; approximated with Otsu. Illumination correction's median-smoothing radius needed a much larger value (20 block-grid units) than a naive unit conversion from CP's settings suggested, otherwise residual block-boundary noise fragmented each comet into many tiny pieces instead of one blob. Result: CometTails.tif matches CP exactly (6/6/6 whole/head/tail); NoTails.tif is close but not exact (5/5/5 vs CP's 6/4/6) - one faint comet isn't detected, and because head-detection here runs on the full image rather than a CP-style pre-masked one, all 5 found comets get a head where CP only assigned heads to 4 of its 6.

**Contributed by:** Scott Floyd, Michael Pacold, Jorge Ernesto González (Centro de Protección e Higiene de Las Radiaciones)

## About the example data

The fluorescent comet images were donated by Scott Floyd and Michael Pacold. 

The silver-stained comets were contributed by Jorge Ernesto González from the Centro de Protección e Higiene de Las Radiaciones (CPHR).
