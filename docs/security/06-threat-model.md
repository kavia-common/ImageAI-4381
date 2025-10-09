# Threat Model

## Assets
- Model weights (.pt/.pth) and their integrity.
- User-provided image/video inputs and derived outputs.
- Training datasets and resulting custom models.
- Build artifacts, released wheels, and SBOMs.

## Actors
- Legitimate developers and library users.
- Malicious third parties distributing trojaned models or poisoned datasets.
- Supply-chain adversaries introducing vulnerable or malicious dependencies.
- Insider misuse within downstream applications or services.

## Entry Points
- Loading model files from disk or downloaded sources.
- Installing dependencies via PyPI or extra indexes (CPU/GPU wheels).
- Executing examples and CLI tools with user-controlled file paths.

## Scenarios
- Loading a malicious checkpoint without checksum validation leading to arbitrary code execution or model behavior compromise.
- Installing dependencies with known CVEs due to loose pins or VCS-based dependencies.
- Running examples with unvalidated paths leading to unsafe operations when adapted to services.
- CUDA/driver/toolkit mismatches causing instability or exposure to known binary advisories.

## Controls
- Pin and scan dependencies; generate SBOMs and gate releases on severity thresholds.
- Require checksum verification for model files; publish official checksums for releases.
- Harden path handling and avoid unsafe defaults in examples and CLI.
- Document supported environment matrices and verify CPU-only baseline builds.
