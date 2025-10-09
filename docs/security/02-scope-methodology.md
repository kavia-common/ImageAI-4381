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
- No .env variables are defined in this container
- Users may utilize CPU-only or GPU-enabled environments
- Model artifacts may be downloaded from the internet or loaded from local storage

## Tools and Acceptance
- Use pip-audit or safety in CI to scan dependencies from requirements*.txt and install_requires
- Generate CycloneDX SBOMs and attach to releases
- Acceptance gates:
  - No open Criticals for release
  - Highs mitigated or with compensating controls
  - Mediums planned within 2 sprints; Lows in backlog
