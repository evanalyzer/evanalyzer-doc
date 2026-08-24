---
title: "Example Colocalization"
description: "Ported from CellProfiler ExampleColocalization pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_colocalization/example_colocalization.evapt
fileSize: "8.1 KB"
bundleFile: /downloads/templates/project_templates/cp_example_colocalization/example_colocalization-with-images.zip
bundleSize: "3.67 MB"
tags: ["colocalization", "spots", "2-channel", "cellprofiler"]
---

Two-channel spot colocalization (Cy3-like / Cy5-like nucleosome staining). Ported from the CellProfiler ExampleColocalization.cppipe example. Channel 0 = OrigStain1 (files *_N_R), Channel 1 = OrigStain2 (files *_N_G), merged into one 2-channel TIFF per site via Fiji. Object counts run ~10-15% off CP and coloc% ~5pt high, mainly because evanalyzer's watershed declumping (prominence-based) splits touching spots differently than CP's fixed-radius local-maxima method, and evanalyzer's illumination correction averages over blocks before fitting (more robust to bright spots) instead of fitting the raw pixels directly like CP does.

**Contributed by:** Jeff Reifenberger, Brad Berstein's (Massachusetts General Hospital)

## About the example data

Measuring the colocalization between fluorescently labeled molecules is a widely used approach to measure the degree of spatial coincidence and potential interactions among subcellular species (e.g., proteins). This example shows how the object identifcation and RelateObjects modules are used to measure the degree of overlap between two fluorescent channels.

About these images:

Fluoresecent images of a histone-modified nucleosome that is labeled with a Cy3-like dye and an antibody labeled with a Cy5-like dye that is sensitive to to the histone modifications.

These images were contributed by Jeff Reifenberger of Brad Berstein's Lab at Massachusetts General Hospital, March 2012
