# Hardening Checklist

## Supply-Chain
- [ ] constraints-cpu.txt and constraints-gpu.txt committed with vetted pins
- [ ] setup.py install_requires populated
- [ ] pip-audit/safety integrated in CI with fail-on-high
- [ ] CycloneDX SBOM generated and stored as release artifact
- [ ] Replace VCS dependency (pycocotools) with PyPI or pinned tag+hash

## Model Integrity
- [ ] Publish official SHA256 checksums for released weights
- [ ] Add verify_checksum() utility and integrate into load paths
- [ ] Unit tests for correct/incorrect checksums
- [ ] Enforce HTTPS and certificate validation for downloads

## Secure Coding
- [ ] Path canonicalization in examples/CLI
- [ ] Avoid shell=True; no user-controlled command execution
- [ ] Secure temporary file patterns used (NamedTemporaryFile, correct perms)

## Environment
- [ ] Document supported CUDA/driver matrix
- [ ] CPU-only baseline validated
- [ ] Offline install documented (wheels + checksums)

## Data Protection
- [ ] Guidance to strip EXIF/metadata where applicable
- [ ] Dataset provenance and checksums documented
- [ ] Retention and access guidance included
