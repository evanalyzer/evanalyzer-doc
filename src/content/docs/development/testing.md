---
title: Testing
description: Running the EVAnalyzer test suite.
---

## Unit and integration tests

Run all tests with:

```sh
cargo test
```

The `evanalyzer_cfg` crate includes a round-trip deserialisation test that validates example project files:

```sh
cargo test -p evanalyzer_cfg
```

The fixture `tests/fixtures/example.improj` is used to verify that project files serialise and deserialise without loss.

## Code coverage

```sh
cargo llvm-cov          # terminal report
cargo llvm-cov --html   # HTML report in target/llvm-cov/
```

See [Building](/development/building/#code-coverage) for installation instructions.

## Manual verification

Before each release, a set of analysis pipelines is run on reference images to verify:
- Correct object counts match expected values.
- Exported CSV files match reference outputs.
- No regressions in segmentation quality.

Reference test images and expected outputs are maintained separately in the test repository.
