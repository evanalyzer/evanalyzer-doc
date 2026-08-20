---
title: Cell Uptake - 2 Channel Colocalization
description: Segments cells from a brightfield/nucleus channel and spots from a second fluorescence channel, then colocalizes spots with cells to measure per-cell uptake.
category: template
file: /downloads/templates/cell_uptake_2_channel_coloc.evapt
tags: [colocalization, uptake, 2-channel]
---

Ready-made project template for measuring how much of a labelled compound (extracellular vesicles, nanoparticles, dye) is taken up per cell.

- **Channel 1** - nucleus/whole-cell stain, segmented into `cell` objects.
- **Channel 2** - the uptake marker, segmented into `spot` objects.
- A [Colocalization](/commands/object/colocalization/) step assigns each spot to the cell it overlaps, so per-cell spot counts and intensities can be read directly from the results table.

Import it via **File → New from Template**, then repoint the two pipelines at your own channels and adjust the threshold/size filters for your data. See [Saving a Project as a Template](/guide/pipelines/#saving-a-project-as-a-template) for how project templates work in general.
