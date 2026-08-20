import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

const downloads = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/downloads' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      category: z.enum(['template', 'model']),
      // Path to the plain download (just the template/model itself),
      // relative to `public/`, e.g.
      // "/downloads/templates/cell_uptake_2_channel_coloc.evapt".
      file: z.string(),
      fileSize: z.string().optional(),
      // Optional second download: a .zip bundling the same file together
      // with example images, for people who want sample data to try it on.
      bundleFile: z.string().optional(),
      bundleSize: z.string().optional(),
      // Preview thumbnails shown on the card - independent of `bundleFile`.
      images: z.array(image()).optional(),
      tags: z.array(z.string()).optional(),
    }),
});

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  downloads,
};
