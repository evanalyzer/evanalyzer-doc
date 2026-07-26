---
title: VS Code Extension
description: Edit EVAnalyzer project, project template, and pipeline template files in VS Code with validation, autocomplete, and creation wizards.
---

**EVAnalyzer File Support** is a VS Code extension for EVAnalyzer's three JSON-based file formats. It's under active development on the [`init` branch](https://github.com/evanalyzer/evanalyzer-vscode/tree/init) of the evanalyzer-vscode repository (not yet merged to `main`).

| Extension | Contents | Schema |
| --- | --- | --- |
| `.evapipe` | Pipeline templates | [`pipeline_template.schema.json`](https://github.com/evanalyzer/evanalyzer-vscode/blob/init/schemas/pipeline_template.schema.json) |
| `.evaproj` | Project files | [Project File Schema](/fundamentals/project-schema/) |
| `.evapt` | Project templates | [`project_template.schema.json`](https://github.com/evanalyzer/evanalyzer-vscode/blob/init/schemas/project_template.schema.json) |

## What it does

### Editing

The extension associates all three extensions with VS Code's built-in JSON language support and registers each one's JSON Schema, so opening any `.evapipe`, `.evaproj`, or `.evapt` file gives you:

- Syntax highlighting, bracket matching, and code folding
- Red squiggles on invalid fields or values
- Hover documentation pulled from the schema's descriptions
- Autocomplete for property names and enum values

### Creating

Three commands walk the relevant JSON Schema and prompt you only for the fields it actually requires, then write out a valid starter file:

- **EVAnalyzer: New Project...**
- **EVAnalyzer: New Project Template...**
- **EVAnalyzer: New Pipeline Template...**

Run them from the Command Palette (`Ctrl/Cmd+Shift+P`), or right-click a folder in the Explorer and choose **New EVAnalyzer File**. Once the required fields are filled in, the wizard also offers to fill in any optional fields.

:::tip
Since the wizard reads the same JSON Schema that EVAnalyzer itself generates (see the [Project File Schema](/fundamentals/project-schema/) reference), a project scaffolded this way is guaranteed to match whatever version of EVAnalyzer produced that schema.
:::

## Installation

The extension isn't published to the VS Code Marketplace or Open VSX yet, so for now it has to be built and installed from source:

```sh
git clone -b init https://github.com/evanalyzer/evanalyzer-vscode.git
cd evanalyzer-vscode
npm install
npm run package
code --install-extension evanalyzer-file-support-*.vsix
```

:::caution
The extension currently lives on the `init` branch, not `main` - the `-b init` above is required. Once it's merged, this page will be updated to drop it.
:::

`npm run package` type-checks the project, bundles it, runs its test suite, and produces a `.vsix` file - the same format the Marketplace uses, so `code --install-extension` installs it exactly as if it had come from there.

:::note
Once the extension is published, this page will be updated with a direct Marketplace/Open VSX link and the [Downloads](/getting-started/downloads/) page will link straight to the latest release instead.
:::

## Requirements

VS Code 1.85.0 or later.
