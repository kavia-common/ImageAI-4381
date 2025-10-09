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

