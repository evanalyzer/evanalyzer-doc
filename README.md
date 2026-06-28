# evanalyzer-doc

Run in devel mode

```sh
npm run dev -- --host
```

Documentation of EVAnalyzer
All files are created. Here's what was set up:

Project structure:

package.json - Astro + Starlight dependencies
astro.config.mjs - Starlight config with sidebar
tsconfig.json - TypeScript config
src/content/docs/index.mdx - Hello World splash page
src/content/docs/guides/getting-started.md - Getting started guide
DevContainer:

.devcontainer/devcontainer.json - Node 22 + Astro VS Code extension, auto-runs npm install, forwards port 4321
CI/CD:

.github/workflows/deploy.yml - Builds on push to main and deploys to GitHub Pages
Before pushing, you need to do two things:

Update astro.config.mjs - change site to your actual GitHub username URL (https://<your-username>.github.io). The base: '/evanalyzer-doc' is already set to match your repo name.

Enable GitHub Pages in repo settings - go to Settings → Pages → Source → select GitHub Actions.

Then run locally:

npm install
npm run dev
My pipelone in github shows

Run actions/setup-node@v4
Found in cache @ /opt/hostedtoolcache/node/22.22.3/x64
Environment details
/opt/hostedtoolcache/node/22.22.3/x64/bin/npm config get cache
/home/runner/.npm
Error: Dependencies lock file is not found in /home/runner/work/evanalyzer-doc/evanalyzer-doc. Supported file patterns: package-lock.json,npm-shrinkwrap.json,yarn.lock
Show more
The npm ci command requires a committed package-lock.json. Let me check if npm is available and generate it.

Bash Check if npm is available
IN
which npm && npm --version

OUT
Exit code 1
npm isn't available locally so we can't generate a package-lock.json. The error comes from actions/setup-node's cache: npm option, which requires a lock file. I'll fix the workflow to use npm install without the npm cache dependency.

Read deploy.yml
Edit deploy.yml
Removed 1 line
The fix: removed cache: npm and switched npm ci to npm install. The cache: npm option in setup-node strictly requires a package-lock.json to exist - without it, the step fails before even reaching the install command.

If you later want to restore caching (which speeds up builds), just run npm install locally once to generate a package-lock.json, commit it, and then you can revert to npm ci + cache: npm.
