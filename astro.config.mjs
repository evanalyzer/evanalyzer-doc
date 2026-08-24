import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import starlight from "@astrojs/starlight";
import starlightImageZoom from "starlight-image-zoom";
import starlightLlmsTxt from "starlight-llms-txt";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

export default defineConfig({
  site: "https://evanalyzer.org",
  // starlight-image-zoom doesn't support Astro's newer default "satteri"
  // markdown processor yet - stay on the remark/rehype pipeline until it does.
  // remark-math/rehype-katex render the $$ ... $$ formula blocks used in the
  // fundamentals docs (e.g. metrics.md) - without them, "$$" is emitted as
  // literal text instead of typeset math.
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
  integrations: [
    starlight({
      plugins: [
        starlightImageZoom(),
        starlightLlmsTxt({
          projectName: "EVAnalyzer",
          details:
            "EVAnalyzer's pipeline configuration format is described by a JSON Schema published at https://evanalyzer.org/schema/project.schema.json - a `oneOf` discriminated union covering every pipeline command, suitable for validating or generating `.evaproj` project/pipeline files programmatically.",
          optionalLinks: [
            {
              label: "Pipeline JSON Schema",
              url: "https://evanalyzer.org/schema/project.schema.json",
              description:
                "Machine-readable JSON Schema for .evaproj project/pipeline files",
            },
          ],
          // The homepage hero's title animation and compare sliders are raw
          // HTML (with inline <style>/<script>) injected via Starlight's
          // hero.title/hero.image, since that's the only way to customize
          // them - strip those tags so they don't dump as tag soup here.
          customSelectors: { all: ["style", "script"] },
        }),
      ],
      title: "EVAnalyzer",
      favicon: "/favicon.png",
      head: [
        {
          tag: "link",
          attrs: { rel: "preconnect", href: "https://fonts.googleapis.com" },
        },
        {
          tag: "link",
          attrs: {
            rel: "preconnect",
            href: "https://fonts.gstatic.com",
            crossorigin: true,
          },
        },
        {
          tag: "link",
          attrs: {
            rel: "stylesheet",
            href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
          },
        },
      ],
      customCss: ["katex/dist/katex.min.css", "./src/styles/custom.css"],
      components: {
        SiteTitle: "./src/components/overrides/SiteTitle.astro",
        ThemeSelect: "./src/components/overrides/ThemeSelect.astro",
        Header: "./src/components/overrides/Header.astro",
      },
      sidebar: [
        {
          label: "Getting Started",
          collapsed: true,
          items: [
            { label: "Installation", slug: "getting-started/installation" },
            {
              label: "System Requirements",
              slug: "getting-started/system-requirements",
            },
            { label: "First Steps", slug: "getting-started/first-steps" },
          ],
        },
        {
          label: "User Guide",
          collapsed: true,
          items: [
            { label: "Images", slug: "guide/images" },
            { label: "Classification", slug: "guide/classification" },
            { label: "Pipelines", slug: "guide/pipelines" },
            { label: "Results", slug: "guide/results" },
          ],
        },
        {
          label: "Fundamentals",
          collapsed: true,
          items: [
            { label: "Image Formats", slug: "fundamentals/image-formats" },
            { label: "Object Classes", slug: "fundamentals/classes" },
            { label: "Objects & Metrics", slug: "fundamentals/metrics" },
            {
              label: "Project File Schema",
              slug: "fundamentals/project-schema",
            },
          ],
        },
        {
          label: "AI",
          collapsed: true,
          items: [
            { label: "AI Models", slug: "ai/overview" },
            {
              label: "Importing bioimage.io Models",
              slug: "ai/bioimageio-import",
            },
            { label: "Training a Classifier", slug: "ai/training" },
            { label: "Random Forest", slug: "ai/random-forest" },
            {
              label: "k-Nearest Neighbors",
              slug: "ai/k-nearest-neighbors",
            },
            {
              label: "Neural Network (MLP)",
              slug: "ai/neural-network-mlp",
            },
          ],
        },
        {
          label: "Commands",
          collapsed: true,
          items: [
            { label: "Overview", slug: "commands/overview" },
            {
              label: "Image Processing",
              collapsed: true,
              items: [
                { label: "Blur", slug: "commands/image-processing/blur" },
                {
                  label: "Gaussian Blur",
                  slug: "commands/image-processing/gaussian-blur",
                },
                {
                  label: "Rolling Ball",
                  slug: "commands/image-processing/rolling-ball",
                },
                {
                  label: "Illumination Correction",
                  slug: "commands/image-processing/illumination-correction",
                },
                {
                  label: "Rank Filter",
                  slug: "commands/image-processing/rank-filter",
                },
                {
                  label: "Enhance Contrast",
                  slug: "commands/image-processing/enhance-contrast",
                },
                {
                  label: "Color Filter",
                  slug: "commands/image-processing/color-filter",
                },
                {
                  label: "Intensity Transform",
                  slug: "commands/image-processing/intensity-transform",
                },
                {
                  label: "Median Subtract",
                  slug: "commands/image-processing/median-subtract",
                },
                {
                  label: "Image Math",
                  slug: "commands/image-processing/image-math",
                },
                {
                  label: "Image Cache",
                  slug: "commands/image-processing/image-cache",
                },
              ],
            },
            {
              label: "Edge & Feature Detection",
              collapsed: true,
              items: [
                {
                  label: "Canny Edge Detection",
                  slug: "commands/edge-detection/canny",
                },
                {
                  label: "Sobel Edge Detection",
                  slug: "commands/edge-detection/sobel",
                },
                { label: "Hessian", slug: "commands/edge-detection/hessian" },
                {
                  label: "Laplacian",
                  slug: "commands/edge-detection/laplacian",
                },
                {
                  label: "Structure Tensor",
                  slug: "commands/edge-detection/structure-tensor",
                },
                {
                  label: "Weighted Deviation",
                  slug: "commands/edge-detection/weighted-deviation",
                },
              ],
            },
            {
              label: "Segmentation",
              collapsed: true,
              items: [
                { label: "Threshold", slug: "commands/segmentation/threshold" },
                {
                  label: "Connected Components",
                  slug: "commands/segmentation/connected-components",
                },
                { label: "Watershed", slug: "commands/segmentation/watershed" },
              ],
            },
            {
              label: "Morphology",
              collapsed: true,
              items: [
                {
                  label: "Morphological Transform",
                  slug: "commands/morphology/morphological-transform",
                },
              ],
            },
            {
              label: "AI Segmentation",
              collapsed: true,
              items: [
                {
                  label: "Stardist",
                  slug: "commands/ai-segmentation/stardist",
                },
                { label: "UNet", slug: "commands/ai-segmentation/unet" },
                {
                  label: "Cellpose",
                  slug: "commands/ai-segmentation/cellpose",
                },
                {
                  label: "AI Pixel Classifier",
                  slug: "commands/ai-segmentation/pixel-classifier",
                },
              ],
            },
            {
              label: "Object Processing",
              collapsed: true,
              items: [
                {
                  label: "Fill Holes",
                  slug: "commands/object/fill-holes",
                },
                {
                  label: "Extract Objects",
                  slug: "commands/object/extract-objects",
                },
                {
                  label: "Classify Objects",
                  slug: "commands/object/classify-objects",
                },
                {
                  label: "AI Object Classifier",
                  slug: "commands/object/ai-object-classifier",
                },
                {
                  label: "Colocalization",
                  slug: "commands/object/colocalization",
                },
                { label: "Voronoi", slug: "commands/object/voronoi" },
                {
                  label: "Object Transform",
                  slug: "commands/object/transform-objects",
                },
                {
                  label: "Distance Transform",
                  slug: "commands/object/distance-transform",
                },
                {
                  label: "Object Math",
                  slug: "commands/object/object-math",
                },
                { label: "Save Image", slug: "commands/object/save-image" },
              ],
            },
          ],
        },
        {
          label: "CLI",
          collapsed: true,
          items: [{ label: "Command Line Interface", slug: "cli/cli" }],
        },
        {
          label: "VS Code Extension",
          collapsed: true,
          items: [{ label: "Editing Project Files", slug: "vscode/extension" }],
        },
        {
          label: "Tutorials",
          collapsed: true,
          items: [
            { label: "Spot Count", slug: "tutorials/spot-count" },
            {
              label: "Spot Count per Cell",
              slug: "tutorials/spot-count-per-cell",
            },
            {
              label: "Spot Colocalization",
              slug: "tutorials/spot-colocalization",
            },
          ],
        },
        {
          label: "Development",
          collapsed: true,
          items: [
            { label: "Building", slug: "development/building" },
            { label: "Testing", slug: "development/testing" },
          ],
        },
        {
          label: "Project",
          collapsed: true,
          items: [
            { label: "About", slug: "about" },
            { label: "Comparison", slug: "comparison" },
            { label: "Citation", slug: "citation" },
            { label: "FAQ", slug: "faq" },
            { label: "Support", slug: "support" },
          ],
        },
      ],
    }),
  ],
});
