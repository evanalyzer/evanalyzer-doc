---
title: VS Code Extension
description: Edit EVAnalyzer project, project template, and pipeline template files in VS Code with validation, autocomplete, and creation wizards.
---

**EVAnalyzer File Support** is a VS Code extension for EVAnalyzer's three JSON-based file formats, developed in the [evanalyzer-vscode](https://github.com/evanalyzer/evanalyzer-vscode) repository. See [Installation](/getting-started/installation/#vs-code-extension) to get the latest release.

| Extension | Contents | Schema |
| --- | --- | --- |
| `.evapipe` | Pipeline templates | [`pipeline_template.schema.json`](https://github.com/evanalyzer/evanalyzer-vscode/blob/main/schemas/pipeline_template.schema.json) |
| `.evaproj` | Project files | [Project File Schema](/fundamentals/project-schema/) |
| `.evapt` | Project templates | [`project_template.schema.json`](https://github.com/evanalyzer/evanalyzer-vscode/blob/main/schemas/project_template.schema.json) |

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

The extension isn't published to the VS Code Marketplace or Open VSX yet, so install the packaged `.vsix` directly:

1. Download `evanalyzer-file-support-*.vsix` from the [latest release](https://github.com/evanalyzer/evanalyzer-vscode/releases/latest) (also linked from [Installation](/getting-started/installation/#vs-code-extension)).
2. Install it:

   ```sh
   code --install-extension evanalyzer-file-support-*.vsix
   ```

   Or in VS Code: open the **Extensions** view, click the **...** menu, choose **Install from VSIX...**, and select the downloaded file.

### Building from source

To build the extension yourself instead - for example, to try an unreleased change:

```sh
git clone https://github.com/evanalyzer/evanalyzer-vscode.git
cd evanalyzer-vscode
npm install
npm run package
code --install-extension evanalyzer-file-support-*.vsix
```

`npm run package` type-checks the project, bundles it, runs its test suite, and produces a `.vsix` file - the same format used for the published release.

:::note
Once the extension is published to the Marketplace/Open VSX, this page will be updated with a direct install link.
:::

## Requirements

VS Code 1.85.0 or later.
