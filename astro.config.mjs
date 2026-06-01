import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Update `site` to your GitHub Pages URL: https://<username>.github.io
// Update `base` to your repository name if it's not a user/org page.
export default defineConfig({
  site: 'https://joachim-danmayr.github.io',
  base: '/evanalyzer-doc',
  integrations: [
    starlight({
      title: 'EVAnalyzer Docs',
      sidebar: [
        {
          label: 'Guides',
          items: [
            { label: 'Getting Started', slug: 'guides/getting-started' },
          ],
        },
      ],
    }),
  ],
});
