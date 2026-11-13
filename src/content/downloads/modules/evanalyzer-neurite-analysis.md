---
title: "Neurite analysis"
description: "Neurite skeletons, Sholl profiles and traced neurite trees per neuron"
category: module
file: /downloads/templates/module_templates/evanalyzer/neurite_analysis.evamodule
fileSize: "12 KB"
tags: ["neurite", "neuron", "sholl", "skeleton", "filament", "tracing"]
---

Per neuron its neurite tree and Sholl profile, from a soma channel and a neurite channel (e.g. tubulin, MAP2). Somata: Gaussian blur, Otsu threshold. Neurites: vesselness at the fibre widths, Otsu threshold, skeletonized to one centre line per neurite object ("Skeletons") with its end points ("Tips"). The skeletons are linked to the soma and the neurite object they overlap most; per skeleton the skeleton values (total and longest-path length, branch and end points, segment length and straightness, mean diameter from its neurite object) and the Sholl values (circles around the linked soma's centroid every "Ring step": crossings per radius, most crossings, critical and enclosing radius, mean crossings, Sholl regression coefficient). Independently, each neuron is traced as a tree from its soma to the tips along the neurite channel ("Segments"): per segment its branch level, Strahler order, path distance and length; per neuron (on its soma) the total length, primary neurites, branch points, tips, highest branch level and longest path. Results › Trees shows the dendrograms of the traced neurons, Charts › Profile the Sholl curves. A skeleton that overlaps no soma gets no soma parent and its Sholl circles are not centred on a soma. All lengths, widths and radii are in pixels.

**Contributed by:** Joachim Danmayr
