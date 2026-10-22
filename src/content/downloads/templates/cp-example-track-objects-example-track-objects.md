---
title: "Example Track Objects"
description: "Ported from CellProfiler ExampleTrackObjects pipeline"
category: template
file: /downloads/templates/project_templates/cp_example_track_objects/example_track_objects.evatemplate
fileSize: "6.5 KB"
bundleFile: /downloads/templates/project_templates/cp_example_track_objects/example_track_objects-with-images.zip
bundleSize: "3.71 MB"
tags: ["tracking", "time-lapse", "drosophila", "cellprofiler"]
---

Drosophila embryo GFP-histone time-lapse: segment embryos per frame and track them. Ported from the CellProfiler ExampleTrackObjects.cppipe example. Input: images/SequenceN.tif, one gray 21-frame time stack per sequence, built with Fiji from the RGB frames as (R+G+B)/3 (= CP ColorToGray 'Combine', equal weights); each sequence is its own image, which replaces CP's per-folder grouping. Embryos = CP IdentifyPrimaryObjects: Gaussian sigma 1 (CP threshold smoothing scale 1.3488), 2-class Otsu computed on the raw image (lower bound 0.01), fill holes, intensity-seeded watershed with CP's automatic declumping values (seed smoothing sigma 7.14, maxima suppression 16.7 px; CP's low-resolution speed-up is not reproduced), minimum equivalent diameter 25 px (area >= 491 px), border objects discarded. Tracking: SIMPLE_TRACKER (nearest neighbour, max 50 px) instead of CP's Overlap method. Result vs CP: objects 63/120/115 vs 65/119/109 per sequence, every CP object matched within 15 px in Seq1/Seq3 and 116/119 in Seq2, median per-object area ratio 0.99-1.00. Tracks: Seq1 3 vs 4 (CP's extra one is a one-frame object), Seq3 7 vs 7; Seq2 10 vs 6 because CP's Overlap gives both daughters of a dividing embryo the parent's label, whereas nearest-neighbour tracking continues the parent in one daughter and starts a new track for the other, plus one frame (t=4) where two touching embryos are merged. Track data: `evanalyzer cli export csv --group-by track --class Embryos` gives a time course per track (area, shape, intensity per frame); the per-object export has T and Track ID columns. CP's per-track motion measurements (Displacement, IntegratedDistance, Linearity) are not computed by evanalyzer; they can be derived from the centroids in `export parquet` and then agree with CP for tracks without a division (e.g. Seq3 displacement 35.8/43.2/51.8/59.1 px CP vs 34.7/42.8/50.5/59.1 px eva).

**Contributed by:** Victoria Foe, G. Odell, Rob Saint

## About the example data

This example identifies the nuclei of a time-lapse movie frame by frame and tracks them from frame to frame. Each sequence is analyzed independently; export the tracks with `evanalyzer cli export csv --group-by track`.

About these images:

A portion of a time lapse movie of a syncytial blastoderm stage Drosophila embryo with a GFP-histone gene which renders chromatin fluorescent in live embryos. The movie shows nuclear divisions 10 through 13.

Victoria Foe made this movie on a Bio-Rad Radiance 2000 laser scanning confocal microscope using a 40X 1.3NA oil objective. The frames are 7 seconds apart.

GFP-histone transformed files provided by Rob Saint.

V. Foe and G. Odell, 26 July 2001

The 21 RGB frames of each CellProfiler sequence folder are combined into one gray time stack per sequence (`Sequence1.tif` ... `Sequence3.tif`, gray = (R+G+B)/3 like CellProfiler's ColorToGray 'Combine').
