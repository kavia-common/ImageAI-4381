Intentionally left blank. Risk Report

## Overview
Dependencies are currently specified in requirements.txt and requirements_gpu.txt with broad version ranges. setup.py does not enforce install_requires, shifting responsibility to external installation steps. requirements_extra.txt references a Git-based pycocotools, which introduces drift risk.

## Dependency Risk Table
| Package | Version Spec | Known CVEs | Severity | Fix Version | Status |
|---|---|---|---|---|---|
| torch | >=1.9.0 (CPU/GPU) | Unknown (scan required) | Unknown | Triage | Pending scan |
| torchvision | >=0.10.0 | Unknown | Unknown | Triage | Pending scan |
| numpy | >=1.18.1 | Historical CVEs exist | Medium–High | Pin latest secure | Pending scan |
| opencv-python | >=4.1.2 | Historical CVEs exist | Medium–High | Pin latest secure | Pending scan |
| pillow | >=7.0.0 | Historical CVEs exist | Medium–High | >=9.5.x recommended | Pending scan |
| scipy | >=1.7.3 | Unknown | Unknown | Triage | Pending scan |
| matplotlib | >=3.4.3 | Unknown | Unknown | Triage | Pending scan |
| tqdm | ==4.64.1 | Unknown | Unknown | Triage | Pending scan |
| pytest | ==7.1.3 | N/A (dev) | N/A | N/A | Dev-only |
| mock | ==4.0.3 | N/A (dev) | N/A | N/A | Dev-only |
| pycocotools (git) | floating head | Drift risk | High | Pin to tag/commit | Change needed |

Sources: requirements.txt, requirements_gpu.txt, requirements_extra.txt, setup.py

## Transitive Dependencies
| Parent | Child | Risk | Action |
|---|---|---|---|
| torch/torchvision | numpy, typing-extensions, etc. | Transitive CVEs possible | SBOM + scan |
| opencv-python | ffmpeg-related wheels | CVEs in bundled libs possible | Pin and scan |
| pillow | libjpeg/zlib wrappers | Historical CVEs | Keep current secure version |

## Notes
- GPU vs CPU: Different wheels (CPU vs CUDA) are fetched from PyTorch extra-index URLs; maintain separate constraints for reproducibility (e.g., constraints-cpu.txt, constraints-gpu.txt).
- Pinned versions and Reproducibility: Introduce constraints files and lock to known-good builds per release branch.
- Model File Integrity: Treat model artifacts as part of supply chain; maintain SHA256 checksums and store alongside model downloads. Enforce verification before use.

## Actions
- Add install_requires in setup.py mirroring minimal supported secure versions.
- Add pip-audit/safety to CI; fail on Critical/High.
- Generate CycloneDX SBOM for CPU and GPU environments and attach to release artifacts.
- Replace git-based dependency with pinned version from PyPI or tagged commit+hash; store checksum or VCS tag.

