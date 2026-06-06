import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  site: "https://evanalyzer.org",
  integrations: [
    starlight({
      title: "EVAnalyzer Docs",
      sidebar: [
        {
          label: "Getting Started",
          items: [
            { label: "Installation", slug: "getting-started/installation" },
            { label: "First Steps", slug: "getting-started/first-steps" },
          ],
        },
        {
          label: "User Guide",
          items: [
            { label: "Project Setup", slug: "guide/project-setup" },
            { label: "Images", slug: "guide/images" },
            { label: "Classification", slug: "guide/classification" },
            { label: "Pipelines", slug: "guide/pipelines" },
            { label: "Results", slug: "guide/results" },
          ],
        },
        {
          label: "Fundamentals",
          items: [
            { label: "Image Formats", slug: "fundamentals/image-formats" },
            { label: "Objects", slug: "fundamentals/objects" },
            { label: "Metrics", slug: "fundamentals/metrics" },
          ],
        },
        {
          label: "Commands",
          items: [
            { label: "Overview", slug: "commands/overview" },
            {
              label: "Image Processing",
              items: [
                { label: "Blur", slug: "commands/image-processing/blur" },
                { label: "Gaussian Blur", slug: "commands/image-processing/gaussian-blur" },
                { label: "Rolling Ball", slug: "commands/image-processing/rolling-ball" },
                { label: "Rank Filter", slug: "commands/image-processing/rank-filter" },
                { label: "Enhance Contrast", slug: "commands/image-processing/enhance-contrast" },
                { label: "Color Filter", slug: "commands/image-processing/color-filter" },
                { label: "Intensity Transform", slug: "commands/image-processing/intensity-transform" },
                { label: "Median Subtract", slug: "commands/image-processing/median-subtract" },
                { label: "Image Math", slug: "commands/image-processing/image-math" },
                { label: "Image Cache", slug: "commands/image-processing/image-cache" },
              ],
            },
            {
              label: "Edge & Feature Detection",
              items: [
                { label: "Canny Edge Detection", slug: "commands/edge-detection/canny" },
                { label: "Sobel Edge Detection", slug: "commands/edge-detection/sobel" },
                { label: "Hessian", slug: "commands/edge-detection/hessian" },
                { label: "Laplacian", slug: "commands/edge-detection/laplacian" },
                { label: "Structure Tensor", slug: "commands/edge-detection/structure-tensor" },
                { label: "Weighted Deviation", slug: "commands/edge-detection/weighted-deviation" },
              ],
            },
            {
              label: "Segmentation",
              items: [
                { label: "Threshold", slug: "commands/segmentation/threshold" },
                { label: "Connected Components", slug: "commands/segmentation/connected-components" },
                { label: "Watershed", slug: "commands/segmentation/watershed" },
              ],
            },
            {
              label: "Morphology",
              items: [
                { label: "Morphological Transform", slug: "commands/morphology/morphological-transform" },
              ],
            },
            {
              label: "Object Processing",
              items: [
                { label: "Extract ROIs", slug: "commands/object/extract-rois" },
                { label: "Classify ROIs", slug: "commands/object/classify-rois" },
                { label: "Colocalization", slug: "commands/object/colocalization" },
                { label: "Voronoi", slug: "commands/object/voronoi" },
                { label: "Distance Transform", slug: "commands/object/distance-transform" },
                { label: "Save Image", slug: "commands/object/save-image" },
              ],
            },
          ],
        },
        {
          label: "CLI",
          items: [
            { label: "Command Line Interface", slug: "cli/cli" },
          ],
        },
        {
          label: "Tutorials",
          items: [
            { label: "Spot Count", slug: "tutorials/spot-count" },
            { label: "Spot Count per Cell", slug: "tutorials/spot-count-per-cell" },
            { label: "Spot Colocalization", slug: "tutorials/spot-colocalization" },
          ],
        },
        {
          label: "Development",
          items: [
            { label: "Building", slug: "development/building" },
            { label: "Testing", slug: "development/testing" },
          ],
        },
      ],
    }),
  ],
});
