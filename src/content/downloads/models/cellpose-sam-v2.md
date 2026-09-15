---
title: "Cellpose SAM v2"
description: "AI Cellpose Segmentation"
category: model
file: https://github.com/evanalyzer/evanalyzer-models/releases/download/app-deps/cpsam_v2.zip
fileSize: "573 MB"
---

Cellpose-SAM is a biological segmentation model that integrates the pretrained transformer architecture of Meta's Segment Anything Model (SAM) with the Cellpose framework to accurately predict vector flow fields for dense cellular structures.
By combining these methods, it achieves "superhuman generalization," outperforming the average accuracy of human annotators and reaching near-optimal cell masking performance. [1]

</br>

**[1]:** _Pachitariu, M., Rariden, M., & Stringer, C. (2025). Cellpose-SAM: superhuman generalization for cellular segmentation. bioRxiv. doi.org_

</br>

Unzip the download and point **Model path** at the `cpsam_v2.pt` file inside when configuring the [AI Cellpose Segmentation](/commands/ai-segmentation/cellpose/) command.
