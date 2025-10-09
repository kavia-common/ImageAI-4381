# Dependency and Supply-Chain

## Overview
Dependencies are defined in requirements.txt and requirements_gpu.txt with broad lower bounds (>=). setup.py specifies install_requires=[], which means consumers may install the library without necessary security-vetted dependencies unless they separately install requirements. requirements_extra.txt references pycocotools via a Git URL, which introduces drift and reproducibility risks.

## Dependency Risk Table
| Package | Version Spec | Risk Summary | Severity | Action |
|---|---|---|---|---|
| torch | >=1.9.0 (CPU/GPU wheels via extra index) | Large binary surface; advisories occur | High | Pin per profile; scan |
| torchvision | >=0.10.0 | Tied to torch ABI; transitive risk | High | Pin aligned to torch |
| numpy | >=1.18.1 | Historical CVEs; widely used | Medium–High | Pin vetted version |
| opencv-python | >=4.1.2 | Bundles native libs; historical CVEs | High | Pin; scan |
| pillow | >=7.0.0 | Historical image parsing CVEs | High | Pin >=9.5.x |
| scipy | >=1.7.3 | Native code; transitive risks | Medium | Pin |
| matplotlib | >=3.4.3 | Lower risk; transitive | Medium | Pin |
| tqdm | ==4.64.1 | Lower risk; keep updated | Low | Pin latest |
| pytest | ==7.1.3 (dev) | Dev-only | Low | Dev constraints only |
| mock | ==4.0.3 (dev) | Dev-only | Low | Dev constraints only |
| pycocotools (git) | floating head | Supply-chain drift | High | Use PyPI or pinned tag+hash |

Sources: requirements.txt, requirements_gpu.txt, requirements_extra.txt, setup.py

## Transitive Dependencies
| Parent | Child | Risk | Action |
|---|---|---|---|
| torch/torchvision | numpy, typing-extensions, etc. | CVEs propagate via transitives | SBOM + scan |
| opencv-python | ffmpeg-related libs | CVEs in bundled libs/wheels | Pin, scan |
| pillow | libjpeg/zlib | Multiple historical issues | Pin, scan |

## Notes
- CPU vs GPU: Use separate constraints (constraints-cpu.txt, constraints-gpu.txt) to achieve reproducible environments with correct wheel sources (PyTorch extra-index URLs).
- Reproducibility: Pin all direct dependencies; consider pip-compile workflows for lockfiles.

## Actions
- Populate install_requires in setup.py with safe minimal bounds aligned to constraints.
- Add pip-audit/safety to CI and fail on Critical/High.
- Generate CycloneDX SBOM for CPU and GPU profiles and attach to release artifacts.
- Replace Git-based pycocotools with a pinned PyPI release or a specific tag+hash; optionally require hashes (--require-hashes).
