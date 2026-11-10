# Screenshots

The screenshots of the app are taken automatically by
`scripts/screenshots/take.py` - see [scripts/screenshots/README.md](scripts/screenshots/README.md).
Re-run it after a design change:

```sh
python3 scripts/screenshots/take.py
```

The current shots are taken with a build of EVAnalyzer's `main` (commit
`57df2c0`, after 1.1.0-alpha.3) - the ruler, the Profile chart and the Paths
and Trees views are in no release yet. See
[scripts/screenshots/README.md](scripts/screenshots/README.md#the-binary) for
how to build it.

Still placeholders in the docs (a dashed `evx-shot-todo` box), not scripted yet:

- [ ] **Marker and pixel values** - `guide/images.md` - `src/assets/screenshots/screenshot-image-measure-points.png`
- [ ] **Coloc pairs** - `guide/results.md` - `src/assets/screenshots/screenshot-results-coloc-details-view.png` (A row per: Coloc pairs - the demo plate's rows show no partner columns)
- [ ] **Parents and children** - `guide/results.md` - `src/assets/screenshots/screenshot-results-children.png` (the neuron project has Relate Objects: skeletons in somata - CHILDREN "map2@skeleton in dapi@soma")

Find the placeholders with `grep -rn evx-shot-todo src/content/docs`.
