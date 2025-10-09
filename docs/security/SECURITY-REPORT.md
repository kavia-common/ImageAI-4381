# ImageAI Security Report (Merged)
Generated: 2025-10-09T00:00:00Z

Note: This report is an immediate merge of docs/security files according to _order.txt. Missing files are noted below if any.

Included files (in order):
1) README.md
2) 01-executive-summary.md
3) 02-scope-methodology.md
4) 03-dependency-supply-chain.md
5) 04-static-and-secrets.md
6) 05-config-and-env.md
7) 06-threat-model.md
8) 07-vulnerability-register.md
9) 08-risk-matrix.md
10) 09-implementation-playbook.md
11) 10-hardening-checklist.md

Missing files report:
- None (all files present)

================================================================================
# [1/11] Source: README.md
================================================================================

# ImageAI Security Vulnerability Assessment Suite

## Overview
This folder contains a concise, table-driven security documentation suite for the ImageAI library. It is optimized for quick developer consumption and for use in ticketing and CI/CD automation. The content focuses on actionable findings, prioritized risks, and clear remediation guidance while remaining aligned with the current repository contents.

## Audience
Developers and tech leads familiar with the ImageAI codebase who need to assess and mitigate security risks quickly.

## Documents
- Executive Summary: See 01-executive-summary.md
- Scope and Methodology: See 02-scope-methodology.md
- Dependency and Supply Chain Risk: See 03-dependency-supply-chain.md
- Static and Secrets Analysis Summary: See 04-static-and-secrets.md
- Config and Environment Security Review: See 05-config-and-env.md
- Runtime/Execution Threat Model: See 06-threat-model.md
- Vulnerability Register (Prioritized): See 07-vulnerability-register.md
- Risk Matrix and Acceptance Criteria: See 08-risk-matrix.md
- Implementation Playbook: See 09-implementation-playbook.md
- Security Hardening Checklist: See 10-hardening-checklist.md

## Repository Context and Sources
This suite reflects the current repository state and references:
- requirements.txt
- requirements_gpu.txt
- requirements_extra.txt
- setup.py
- imageai/backend_check/backend_check.py
- imageai/backend_check/model_extension.py
- docs/dependency_doc.md

## Navigation
- Start with Executive Summary for prioritized view
- Use Vulnerability Register to drive remediation tickets
- Follow Implementation Playbook for step-by-step changes and validation
- Adopt CI/CD and release controls via the Hardening Checklist

## Maintenance Guidance
- Update 03-dependency-supply-chain.md and 07-vulnerability-register.md when dependencies change or new CVEs are identified.
- Ensure 09-implementation-playbook.md includes exact commands and validation steps added during remediation.
- Keep 10-hardening-checklist.md in sync with CI workflows and release processes.

## Exporting a Single PDF

You can build a consolidated security report (Markdown + PDF) that merges all the documents in a deterministic order defined in `_order.txt`.

Commands:
- python3 scripts/build_security_report.py
- or: make -C docs/security pdf

Outputs:
- docs/security/SECURITY-REPORT.md
- docs/security/SECURITY-REPORT.pdf

Dependencies for PDF export (any one of the following toolchains):
1) Preferred: Pandoc + wkhtmltopdf
   - Install pandoc: https://pandoc.org/installing.html
   - Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
2) Pandoc + WeasyPrint
   - Install pandoc and Python package weasyprint: pip install weasyprint
3) Python fallback (no pandoc):
   - pip install markdown weasyprint

If no PDF toolchain is available, the script will still generate SECURITY-REPORT.md and print instructions on how to enable PDF export.

Notes:
- The file `docs/security/_order.txt` controls which markdown files are merged and in what order.
- Page breaks are inserted between sections in the generated PDF for readability.
- The script is idempotent, UTF-8 safe, and exits non-zero on errors (missing files or conversion failures).

================================================================================
# [2/11] Source: 01-executive-summary.md
================================================================================

# ImageAI Security Vulnerability Assessment – Executive Summary

## Overall Risk Posture
The current ImageAI codebase presents a moderate security risk profile typical of a machine learning library with optional GPU support and multiple model formats. Primary exposure stems from dependency supply chain risks, use of deprecated TensorFlow/Keras code segments (in a clearly-labeled deprecated directory), and insufficient integrity controls around model files. There is no .env strategy in place, which limits configuration-induced leakage, but also leaves defaults and operational controls unspecified. Setup metadata does not enforce install_requires, shifting dependency control to external requirement files.

## Key High-Severity Findings
- Supply Chain Risks: Unpinned major versions for core ML packages (torch, torchvision, numpy, opencv-python) increase exposure to transitive CVEs and breakage. requirements_extra.txt references a Git-based dependency (pycocotools) which can change over time.
- Model Integrity: No checksum/signature verification for external model files; model file extension checks exist but do not verify provenance or integrity.
- Insecure Transport Defaults: Potential for insecure model artifact downloads in examples and user workflows (no enforced HTTPS checksums); repo includes no documented integrity workflow.
- Packaging/Install Gaps: setup.py sets install_requires=[], not aligning with requirements files; consumers may install without required versions or protections.
- Deprecated Code Surface: imageai_tf_deprecated contains code paths that could be enabled by users if improperly guided; they include legacy utilities and broader attack surface.

## Immediate Actions for Next Sprint
- Introduce SBOM generation and dependency scanning in CI (pip-audit or safety) for requirements*.txt and setup constraints.
- Pin versions (semver ranges or exact pins) for critical packages and separate CPU/GPU lock files; add constraints.txt for reproducibility.
- Implement model file integrity checks (SHA256) and document model provenance and verification steps.
- Align setup.py with install_requires reflecting minimal supported, secure versions; consider extras for GPU.
- Add security notes for users (safe loaders, model paths, permissions, no .h5 models in new backend).

## Top 10 Risks
| ID | Risk | Component | Likelihood | Impact | Severity | Effort | Owner | ETA |
|---|---|---|---|---|---|---|---|---|
| R1 | Unpinned/transitive dependency CVEs | requirements*.txt | High | High | Critical | Medium | Platform | 1 sprint |
| R2 | No model file integrity verification | Model handling | High | High | Critical | Medium | Core | 1 sprint |
| R3 | setup.py lacks install_requires | Packaging | Medium | High | High | Low | Platform | 1 sprint |
| R4 | Git-based dependency drift | requirements_extra | Medium | High | High | Medium | Platform | 1 sprint |
| R5 | Deprecated TF code misuse | imageai_tf_deprecated | Medium | Medium | Medium | Low | Docs | 1 sprint |
| R6 | Insecure transport for artifacts | Examples/Docs | Medium | Medium | Medium | Low | Docs | 1 sprint |
| R7 | Absence of secrets scanning | CI pipeline | Medium | Medium | Medium | Low | DevEx | 1 sprint |
| R8 | No config defaults or .env governance | Config | Low | Medium | Low | Low | Platform | 1 sprint |
| R9 | Logging hygiene (PII risk in apps) | Usage patterns | Low | Medium | Low | Medium | Core | 2 sprints |
| R10| Path handling for user file inputs | I/O flows | Low | Medium | Low | Medium | Core | 2 sprints |

## Quick Wins vs Strategic Items
| Item | Type | Time | Risk Reduced | Next Step |
|---|---|---|---|---|
| Add pip-audit to CI and fail on Critical/High | Quick Win | <1 day | High | Update CI workflow, add badge |
| Align setup.py install_requires | Quick Win | <1 day | Medium | Mirror requirements into setup constraints |
| Provide SHA256 checks for example model files | Quick Win | 1–2 days | High | Publish checksums and verification helper |
| Create constraints.txt per CPU/GPU | Quick Win | 1 day | Medium | Generate lock snapshots |
| Document deprecation and block .h5 by default | Quick Win | <1 day | Medium | Expand model_extension rationale |
| Implement model integrity verification utility | Strategic | 3–5 days | High | Add helper + tests + docs |
| Introduce SBOM generation and signing | Strategic | 2–3 days | Medium | CycloneDX + attach to releases |
| Harden release pipeline (checksums/signature) | Strategic | 2–3 days | High | Release checklist and automation |

================================================================================
# [3/11] Source: 02-scope-methodology.md
================================================================================

# Scope and Methodology

## Scope
This assessment covers:
- Python source (library modules, CLI scripts)
- Third-party dependencies (pip packages, optional GPU stack)
- Build/packaging (setup.py, wheels)
- Configurations and toggles (no .env present; flags in code and docs)
- Documentation and examples (usage patterns that may introduce risk)

In-repo files reviewed as primary sources:
- requirements.txt, requirements_gpu.txt, requirements_extra.txt
- setup.py
- imageai/backend_check/backend_check.py
- imageai/backend_check/model_extension.py
- docs/dependency_doc.md

## Out of Scope
- External model hosting services and their infrastructure
- Runtime environments not represented here (e.g., downstream applications embedding ImageAI) beyond threat model assumptions

## Methods
- SBOM planning and dependency vulnerability scanning (e.g., pip-audit, safety)
- Static code heuristics for dangerous patterns:
  - eval/exec, pickle, yaml.load with UnsafeLoader
  - Path traversal in file I/O
  - Unsafe subprocess usage with user-controlled inputs
  - Insecure HTTP downloads without checksum
- Secrets detection (API keys, tokens in repo and history)
- Configuration review: defaults, fallbacks, env strategy
- Threat modeling across contexts: local dev, server batch, embedded usage, user-supplied inputs

## Assumptions
- Large codebase, concise outputs required
- No internet access during analysis; process and templates prefer repository-grounded findings
- Project currently has no .env variables defined
- Users may utilize CPU-only or GPU-enabled environments

## Tools and Acceptance
- Use pip-audit/safety in CI to scan dependencies from requirements*.txt and install_requires
- Generate CycloneDX SBOMs and attach to releases
- Acceptance gates:
  - No open Criticals for release
  - Highs mitigated or with compensating controls
  - Mediums planned within 2 sprints; Lows in backlog

================================================================================
# [4/11] Source: 03-dependency-supply-chain.md
================================================================================

# Dependency and Supply Chain Risk Report

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

================================================================================
# [5/11] Source: 04-static-and-secrets.md
================================================================================

# Static and Secrets Analysis Summary

## Heuristic Checks Applied
- Dangerous execution: eval/exec (none observed in sampled files)
- Deserialization risks: pickle usage (not observed in sampled files); yaml.load without SafeLoader (not observed)
- Path traversal: file I/O routines handling user-supplied paths (applicable across examples and detectors)
- Subprocess usage with user inputs: not observed in primary files reviewed
- Insecure download flows: model files and assets without checksum verification (documentation/examples risk)
- Hardcoded secrets: no secrets observed in reviewed files

## Findings
| ID | Location | Pattern | Severity | Evidence | Fix Summary |
|---|---|---|---|---|---|
| S1 | imageai/backend_check/model_extension.py | Only extension check for .pt/.pth; no integrity/provenance | High | Extension check without checksum | Add SHA256 verification utility for model files; require checksum parameter |
| S2 | setup.py | install_requires=[] | High | Packaging does not enforce deps | Mirror requirements into install_requires with secure pins/min bounds |
| S3 | requirements_extra.txt | Git-based pycocotools | High | Floating reference | Pin to tag/commit; consider PyPI if viable |
| S4 | requirements*.txt | Broad version ranges | Medium | >= specs | Adopt constraints-cpu/gpu.txt with pinned versions |
| S5 | Examples/Docs | Potential HTTP(s) downloads of models | Medium | No checksum examples | Update docs with checksum instructions; provide helper script |
| S6 | Path handling in examples | User-supplied file paths | Low | Examples accept paths | Document safe path handling and validation (exists, canonicalize) |

## Notes on Source Coverage
Reviewed files:
- requirements.txt, requirements_gpu.txt, requirements_extra.txt
- setup.py
- imageai/backend_check/backend_check.py
- imageai/backend_check/model_extension.py

Further review recommended for:
- Model loading paths, file operations in imageai/* and examples/*
- Any future code interacting with network resources

================================================================================
# [6/11] Source: 05-config-and-env.md
================================================================================

# Config and Environment Security Review

## Areas Reviewed
- ENV handling strategy: No .env present; configuration occurs via function parameters and code defaults.
- Logging and PII exposure: No direct evidence of PII logging in reviewed files; caution in downstream usage.
- CUDA/TF flags and sandboxing: backend_check ensures PyTorch primary; deprecated TensorFlow code remains in imageai_tf_deprecated.
- Model storage directories and permissions: Not explicitly enforced.

## Config Risks
| Variable/Setting | Risk | Recommended Default | Enforcement |
|---|---|---|---|
| Model file path | Unverified artifacts | Require checksum argument (SHA256) | Validate at load |
| Backend selection | Confusion with TF legacy | Default to PyTorch; block .h5 by default | Already blocked by extension; document clearly |
| GPU vs CPU installs | Mismatch/incompatibility | Separate constraints files | CI tests per profile |
| Logging level | Sensitive info leakage in downstream apps | Default to INFO; redact file paths in logs | Document best practices |
| Temp/Cache directories | Permission/leakage | Use secure temp dirs with 0700 perms | Use tempfile; document |

## Recommendations
- Introduce an optional checksum parameter to all model load functions. Reject mismatched checksums.
- Provide environment variables to control strictness (e.g., IMAGEAI_STRICT_INTEGRITY=1) and default to strict in CI.
- Document GPU vs CPU installation profiles with constraints files and expected CUDA versions.
- Encourage use of system temp directories with restricted permissions for intermediate files.

================================================================================
# [7/11] Source: 06-threat-model.md
================================================================================

# Runtime/Execution Threat Model

## Contexts Considered
- Local development: Single-user workstations processing local media.
- Server-side batch processing: Automated jobs handling user-supplied media at scale.
- Embedded usage: Integrated into larger applications/services.
- Handling user-supplied images/videos/models: Untrusted inputs and artifacts.

## Data Flow Narrative
Inputs (images/videos/models) -> Preprocessing -> Model load/execute -> Postprocessing -> Outputs.
Trust boundaries:
- External artifacts (models, media) cross into the process
- Filesystem paths provided by users
- Optional network locations for downloads (via user code)

## STRIDE Considerations
- Spoofing: Maliciously named model files or swapped artifacts.
- Tampering: Modified model binaries; path traversal in file I/O.
- Repudiation: Lack of logging for artifact verification events.
- Information Disclosure: Verbose errors exposing paths/config.
- Denial of Service: Large/malformed inputs; resource exhaustion on GPU/CPU.
- Elevation of Privilege: Not directly applicable unless combined with external tooling/subprocess.

## Threats
| Threat | Vector | Asset | Mitigation | Residual Risk |
|---|---|---|---|---|
| Unverified model file | Swapped .pt/.pth | Model integrity | Enforce SHA256 verification before load | Low |
| Path traversal | Crafted paths | Filesystem | Normalize and validate paths; restrict to allowed dirs | Low–Medium |
| Dependency CVEs | Vulnerable transitive deps | Process/system | CI dependency scanning; constraints; prompt upgrades | Medium |
| DoS via large inputs | Oversized media | Availability | Input size checks; timeouts; resource limits | Medium |
| Info leakage in logs | Verbose errors | Privacy | Sanitize exceptions; avoid dumping paths | Low |
| GPU misconfig | Incompatible CUDA wheels | Stability | Separate profiles; preflight checks | Low |

================================================================================
# [8/11] Source: 07-vulnerability-register.md
================================================================================

# Vulnerability Register (Prioritized)

## Register
| ID | Title | Component | Severity | Likelihood | Evidence | CWE/CVE Ref | Fix Recommendation | Effort | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| VR-001 | Unpinned/transitive dependency CVEs | Dependencies | Critical | High | requirements*.txt unpinned | CWE-1104 | Introduce constraints-cpu/gpu.txt; enable pip-audit in CI; pin secure versions | Medium | Platform | Open |
| VR-002 | No model file integrity verification | Model handling | Critical | High | Only extension check present | CWE-353 | Add checksum verification utility and API; require SHA256 param | Medium | Core | Open |
| VR-003 | Packaging lacks install_requires | Packaging | High | Medium | setup.py install_requires=[] | CWE-693 | Populate install_requires with secure bounds; sync with constraints | Low | Platform | Open |
| VR-004 | Git-based pycocotools dependency | Supply Chain | High | Medium | requirements_extra.txt | CWE-494 | Pin to tag/commit; prefer PyPI release; add hash | Medium | Platform | Open |
| VR-005 | Insecure artifact download guidance | Docs/Examples | Medium | Medium | No checksum docs | CWE-319 | Update docs to include checksum steps; provide helper script | Low | Docs | Open |
| VR-006 | Path handling for user inputs | I/O flows | Low | Medium | Examples accept arbitrary paths | CWE-22 | Canonicalize and validate paths; document safe usage | Medium | Core | Open |

## Notes
- Deprecated TF code remains segregated; ensure docs steer users away from it in v3.x.
- Reassess severities post initial dependency scans.

================================================================================
# [9/11] Source: 08-risk-matrix.md
================================================================================

# Risk Assessment Matrix and Acceptance Criteria

## Matrix Definition
- Severity: Low, Medium, High, Critical
- Likelihood: Low, Medium, High

Risk Matrix (Severity x Likelihood):
- Critical/High = Must fix before release
- High/Medium = Mitigate or add compensating controls
- Medium/* = Plan fix within 2 sprints
- Low/* = Backlog

## Acceptance Criteria
- No open Criticals for release.
- High findings must be mitigated or have compensating controls documented and approved.
- Medium findings scheduled within 2 sprints; Low findings tracked in backlog.

## Application to Register
- VR-001, VR-002: Block release until resolved.
- VR-003, VR-004: High; mitigate prior to release or apply compensating controls with clear plan.
- VR-005: Medium; schedule within 2 sprints.
- VR-006: Low; backlog with guidance in docs.

================================================================================
# [10/11] Source: 09-implementation-playbook.md
================================================================================

# Implementation Playbook

## Task 1: Add Dependency Scanning to CI
| Task | Description | Files/Modules | Commands/Tools | Validation Checks | Rollback Plan |
|---|---|---|---|---|---|
| CI: pip-audit | Add pip-audit to CI for requirements and install_requires | CI config, requirements*.txt, setup.py | pip-audit; safety | CI fails on Critical/High; report uploaded | Disable fail-on-high temporarily (documented) |

## Task 2: Introduce Constraints for CPU and GPU
| Task | Description | Files/Modules | Commands/Tools | Validation Checks | Rollback Plan |
|---|---|---|---|---|---|
| constraints files | Create constraints-cpu.txt and constraints-gpu.txt with pinned versions | New files + docs | pip-compile or manual pins | Deterministic install; tests pass on both profiles | Revert to >= specs temporarily |

## Task 3: Populate install_requires in setup.py
| Task | Description | Files/Modules | Commands/Tools | Validation Checks | Rollback Plan |
|---|---|---|---|---|---|
| setup constraints | Add minimal secure bounds in install_requires | setup.py | N/A | pip install imageai installs required deps | Revert commit if breakage |

## Task 4: Implement Model Integrity Verification
| Task | Description | Files/Modules | Commands/Tools | Validation Checks | Rollback Plan |
|---|---|---|---|---|---|
| checksum utility | Create helper to verify SHA256 for model files; integrate into loaders | imageai/* (model load points) | hashlib; unit tests | Load fails on bad checksum; passes on correct | Feature flag to disable in dev |

## Task 5: Replace Git-Based Dependency
| Task | Description | Files/Modules | Commands/Tools | Validation Checks | Rollback Plan |
|---|---|---|---|---|---|
| pycocotools pin | Use PyPI or fixed tag with hash | requirements_extra.txt | pip with --require-hashes | Builds reproducibly | Revert to previous ref if needed |

## Task 6: Documentation Updates
| Task | Description | Files/Modules | Commands/Tools | Validation Checks | Rollback Plan |
|---|---|---|---|---|---|
| integrity notes | Add checksum steps; warn against .h5 | README, examples, docs | N/A | Docs show checksum flow | Revert doc changes |

================================================================================
# [11/11] Source: 10-hardening-checklist.md
================================================================================

# Security Hardening Checklist

## CI Controls
| Check | Status | Owner | Frequency |
|---|---|---|---|
| Run pip-audit on requirements and install_requires | Planned | Platform | Per PR |
| Run safety as secondary scanner | Planned | Platform | Per PR |
| SAST for Python (bandit/semgrep) | Planned | Platform | Per PR |
| Secret scanning (trufflehog/gitleaks) | Planned | Platform | Per PR |
| Build with constraints-cpu/gpu | Planned | Platform | Per PR |

## Release Controls
| Check | Status | Owner | Frequency |
|---|---|---|---|
| Generate and attach SBOM (CycloneDX) | Planned | Release Eng | Each release |
| Publish checksums for model artifacts | Planned | Release Eng | Each release |
| Sign wheels/sdist | Planned | Release Eng | Each release |
| Verify dependency diffs (lockfiles) | Planned | Release Eng | Each release |

## Runtime Controls
| Check | Status | Owner | Frequency |
|---|---|---|---|
| Enforce model checksum verification by default | Planned | Core | Each release |
| Use secure temp dirs with restricted permissions | Planned | Core | Each release |
| Safe loaders (no unsafe pickle/yaml) | Planned | Core | Each release |

## Documentation Controls
| Check | Status | Owner | Frequency |
|---|---|---|---|
| Security notes in README and examples | Planned | Docs | Each release |
| Deprecation guidance for TF/keras code | Planned | Docs | Each release |
