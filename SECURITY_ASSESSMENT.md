# Security Vulnerabilities Assessment – ImageAI-4381

## 1. Cover Page
Security Vulnerabilities Assessment for ImageAI-4381, a Python library for image/video classification, object detection, and custom training with CPU/GPU (CUDA) support.

- Document Title: Security Vulnerabilities Assessment – ImageAI-4381
- Version 1.0 | 2025-10-22 | Confidential
- Authors: Security Team | Reviewers: Maintainers
- Approved by: ______________________

## 2. Executive Summary
### 2.1 Scope and Objectives
This assessment evaluates the security posture of the ImageAI-4381 library across its Python API and CLI-like scripts, covering training and inference workflows and the dependency stack. It focuses on risks from deserialization/model loading, untrusted media parsing, supply chain exposure through dependencies (notably native bindings), GPU/CUDA runtime, configuration and logging, and CI/release integrity.

### 2.2 Methodology Overview
- Static analysis (SAST): Bandit (Python) — latest run pending artifact attachment
- Software composition analysis (SCA): pip-audit and/or OSV-Scanner — latest run pending artifact attachment
- Linting and style checks: Ruff/Flake8
- Manual code review of core modules and scripts, configuration review, dependency risk review
- Basic threat modeling of assets, actors, trust boundaries, and entry points

### 2.2.1 Scan Summary (current cycle)
- SAST (Bandit): Results to be summarized in Section 8 (Findings) with concrete examples and code references once artifacts are attached.
- SCA (pip-audit/OSV): Vulnerable packages (name, version, CVE, severity) will be summarized in Section 8 and Dependency/Supply Chain sections; detailed list to appear in Appendix 16.4.

### 2.3 Overall Risk Posture
Preliminary Medium risk, common for ML libraries relying on large third-party stacks with native code and optional GPU drivers.

### 2.4 Key Findings
- Model loading/deserialization can be dangerous (pickle/torch.load) without integrity checks.
- Broad dependency ranges and Git-sourced extras (pycocotools) raise supply chain risk; native CVEs are frequent.
- Untrusted media inputs (OpenCV/Pillow/FFmpeg) create DoS and crash risks.
- GPU/CUDA driver/runtime advisories can affect confidentiality/integrity; isolation is often weak.
- Configuration/secrets are undefined; logging may leak sensitive paths or metadata.

### 2.5 Remediation Priorities/Roadmap
- Enforce safe model loading practices and integrity checks.
- Introduce SCA in CI with pinned constraints and lockfiles.
- Harden input validation and safe codec usage, impose resource limits.
- Establish runtime isolation and least privilege execution (containers where applicable).
- Define secrets/configuration policy and sanitize logging.

## 3. Document Control
### 3.1 Version History
- v1.0 | 2025-10-22 | Security Team | Initial assessment document

### 3.2 Distribution and Access
This document is intended for the security team and core maintainers on a need-to-know basis.

### 3.3 References
- docs/Architecture.md; docs/architecture.md; docs/APIReference.md
- requirements.txt; requirements_gpu.txt; requirements_extra.txt
- imageai/backend_check/backend_check.py
- PyTorch/TensorFlow security advisories
- OpenCV/FFmpeg/Pillow/NumPy security advisories

## 4. Project and System Context
### 4.1 System Overview
ImageAI-4381 is a Python library exposing classification and detection models (MobileNetV2, ResNet50, InceptionV3, DenseNet121; RetinaNet, YOLOv3, TinyYOLOv3) and training utilities. It is consumed via Python import and example scripts; there is no HTTP service.

### 4.2 Supported Environments
- CPU and GPU (CUDA) usage based on user environment.
- Typical targets: Linux, Windows, macOS with compatible Python and CUDA drivers; GPU wheels are selected via extra-index URLs (requirements_gpu.txt).

### 4.3 Data Classification
- Inputs: images, videos, datasets, labels.
- Outputs: predictions, annotated frames, extracted objects, trained weights.
- PII risk depends on datasets; datasets should be treated as sensitive by integrators.

### 4.4 Dependencies and Third-Party Components
- ML frameworks: PyTorch, TorchVision (active). Legacy TensorFlow code is kept under imageai_tf_deprecated (deprecated).
- Image/video stack: OpenCV, Pillow; scientific: NumPy, SciPy.
- Tooling: pytest, tqdm, matplotlib.
- Optional training helper: pycocotools via Git URL (requirements_extra.txt).
- Model weights may be downloaded externally by users.

## 5. Assessment Scope and Methodology
### 5.1 In Scope
- Python modules under imageai/, especially yolov3, tiny_yolov3, retinanet/utils, backend_check.
- CLI-like scripts and examples/, scripts/pascal_voc_to_yolo.py.
- Dependency files: requirements.txt, requirements_gpu.txt, requirements_extra.txt.
- Tests demonstrating usage patterns.

### 5.2 Out of Scope
- External datasets and third-party pretrained weights (beyond integrity verification guidance).
- Integrator infrastructure and production orchestration.

### 5.3 Techniques
- Manual code review, configuration and dependency review.
- SAST and SCA scans; recommendations for fuzzing media and annotation parsers.

### 5.4 Tools and Sources
- Bandit, Ruff/Flake8, pip-audit/Safety/OSV, optional Atheris/Hypothesis fuzzing.

## 6. Threat Model
### 6.1 Assets
- Model weights/checkpoints; datasets and annotation files; generated artifacts; GPU resources; release artifacts (wheels, SBOM).

### 6.2 Actors
- Maintainers; library consumers; CI/CD services; external attackers via untrusted inputs (media, weights) or supply chain.

### 6.3 Entry Points
- Python API calls and example CLI-like scripts.
- File I/O for images, videos, annotations, weights.
- Environment/configuration (e.g., CUDA_VISIBLE_DEVICES).
- Model/dataset downloads performed by users.

### 6.4 Trust Boundaries and Data Flows
- Filesystem boundaries for untrusted media and weights.
- Network boundaries for external downloads (weights/datasets).
- GPU runtime boundaries and driver/toolkit interfaces.

### 6.5 Abuse Cases
- Malicious model files leading to code execution via unsafe deserialization.
- Crafted media files causing parser crashes/DoS or resource exhaustion.
- Supply chain compromise via vulnerable or typosquatted packages and Git-based extras.
- Leakage of sensitive metadata through verbose logging.

## 7. Attack Surface Analysis
### 7.1 Input Handling
OpenCV/Pillow media parsing may be susceptible to malformed inputs and resource exhaustion. Video analysis can be abused with high-resolution, high-frame-rate, or long-duration files. The repository’s utilities (e.g., detection utils and example scripts) should validate inputs and bound resources.

### 7.2 Model Loading/Serialization
torch.load and pickle-based formats are unsafe for untrusted content. Users often acquire weights over the internet and may not validate integrity. Without checksums or signatures, tampering could lead to RCE.

### 7.3 Dependency and Supply Chain
- requirements.txt and requirements_gpu.txt specify minimum versions and extra-index URLs; versions are not fully pinned nor hash-pinned.
- requirements_extra.txt uses a Git URL for pycocotools, increasing supply chain risk.
- Native libraries (OpenCV, Pillow, NumPy) have a history of CVEs.
- setup.py delegates to external requirements rather than install_requires constraints.

### 7.4 GPU/Hardware
CUDA/NVIDIA driver advisories can impact availability and confidentiality. Misconfigured GPU-enabled containers may run with unnecessary privileges or capabilities.

### 7.5 CLI/Scripting and File Ops
scripts/pascal_voc_to_yolo.py uses argparse and filesystem operations. Path handling and temporary directories must be hardened; avoid any subprocesses with shell=True (not present now), and sanitize output locations to prevent traversal.

### 7.6 Configuration/Secrets
No .env is defined. Consumers may use environment variables. Ensure no secrets are introduced into code or logs; document expected env configuration where relevant.

### 7.7 Logging/Telemetry
Verbose logs can leak dataset paths or file names. The code uses standard library and frameworks without an opinionated logging layer; integrators should use structured logging with redaction.

### 7.8 Build/CI/CD/Release
No lockfiles or SBOM are present. Reproducible builds and signed artifacts are not established. CI should include SAST/SCA gates and integrity verification workflows.

## 8. Findings
Each finding includes: ID, Title, Severity, Likelihood, Risk, Description, Impact, Affected Components, Evidence/PoC, Exploitability/Detection, Remediation, References.

### 8.0 Findings (SAST – Bandit)
This subsection summarizes the latest Bandit scan across the repository. The detailed JSON artifact is referenced in Appendix 16.4.

- Scan scope: imageai/, scripts/, examples/, setup.py, tests/
- Tool: Bandit (JSON output)
- Summary:
  - High severity: [to be populated with count and brief description]
  - Medium severity: [to be populated]
  - Low severity: [to be populated]
- Representative issues to record:
  - [ID] [File:Line] [Bandit code] [Short title]
    - Context: [code reference or function]
    - Risk: [brief risk]
    - Suggested remediation: [concise actionable step]
- Notable code hotspots to review explicitly:
  - Use of pickle/torch.load if present (B301/B403)
  - XML parsing in scripts/pascal_voc_to_yolo.py (ensure safe parsing and input validation)
  - Any subprocess usage (confirm no shell=True; ideally none used)

Artifacts:
- bandit-report.json (Appendix 16.4)

### 8.1 Findings (SCA – pip-audit/OSV)
This subsection summarizes dependency vulnerabilities identified by pip-audit and/or OSV.

- Scan inputs: requirements.txt, requirements_gpu.txt, requirements_extra.txt
- Tools: pip-audit (PyPI advisories), OSV-Scanner (ecosystem advisories)
- Summary:
  - Critical: [count] — [list package(s)]
  - High: [count] — [list package(s)]
  - Medium/Low: [count] — [list package(s)]
- Representative vulnerable packages:
  - [package]==[version] — [CVE-XXXX-YYYY], [severity], [short description], [fixed version if known]
- Proposed remediations:
  - Pin non-vulnerable versions in constraints/lockfiles with hashes.
  - Where upstream fixes are unavailable, apply temporary constraints to safe ranges, or document exceptions with compensating controls.

Artifacts:
- pip-audit-report.json and/or osv-scanner-report.json (Appendix 16.4)

### 8.A Image Classification
(No unique classification-specific findings beyond general media/model concerns at this time.)

### 8.B Object Detection (RetinaNet, YOLOv3, TinyYOLOv3)
(No unique detection-specific findings beyond media/model/dependency areas at this time.)

### 8.C Video Object Detection/Analysis
(No unique video-specific findings beyond input handling and codec/DoS risk; see F-02.)

### 8.D Custom Model Training
(Training inherits model serialization risks and dependency/toolchain exposure; see F-01, F-03.)

#### F-01: Potential Unsafe Model Deserialization
- Severity: High | Likelihood: Medium | Risk: High
- Description: Loading untrusted PyTorch pickled objects via torch.load may lead to code execution. Weights are commonly downloaded externally without integrity verification.
- Affected: Model loading utilities and user code integrating the library.
- Preconditions: Attacker supplies a crafted model or tampers with weights in transit.
- Evidence: General risk inherent to pickle/torch.load; require repository-wide grep and Bandit scan to identify use sites.
- Detection: Static scanning for torch.load/pickle; runtime monitoring for unexpected imports during load.
- Remediation:
  - Prefer state_dict-only checkpoints; use safe formats like safetensors where possible.
  - Enforce checksums/signatures before load; document expected hashes for official weights.
  - Use torch.load with weights_only=True where applicable, or strictly validate loaded objects and map to CPU to reduce implicit GPU code execution.
- References: https://pytorch.org/docs/stable/generated/torch.load.html; https://github.com/huggingface/safetensors

#### F-02: Unvalidated Media Inputs May Trigger Parser CVEs/DoS
- Severity: Medium | Likelihood: Medium | Risk: Medium
- Description: Untrusted images/videos processed via OpenCV/Pillow may cause crashes, excessive memory/CPU usage, or exploit native decoder CVEs.
- Affected: Data loading in examples and detection/classification preprocessing.
- Preconditions: Processing attacker-supplied media.
- Evidence: Historical CVEs in FFmpeg/OpenCV/Pillow; absence of explicit size/codec guards in example scripts/utilities.
- Detection: Add tests that exercise large/malformed media; fuzz decoding paths.
- Remediation: Whitelist formats/codecs, enforce size/duration limits, apply timeouts, and sandbox parsing when feasible.
- References: https://ffmpeg.org/security.html; https://cve.mitre.org/

#### F-03: Supply Chain and Dependency Risk
- Severity: High | Likelihood: High | Risk: High
- Description: Broad version ranges, extra-index URLs for torch/vision, and a Git-based pycocotools dependency increase integrity risk and exposure to known CVEs.
- Affected: requirements.txt, requirements_gpu.txt, requirements_extra.txt, setup.py process.
- Preconditions: Unpinned or outdated dependencies, unsafe indexes, typosquatting attacks.
- Detection: Run pip-audit/OSV and generate SBOM; monitor advisories for native libraries and PyTorch stack.
- Remediation: Pin versions with constraints/lockfiles, hash-pin (pip-tools/uv), restrict indexes, pin Git deps by commit with checksum or replace with packaged alternatives; CI gate on High/Critical CVEs.

#### F-04: GPU/CUDA Runtime Vulnerabilities and Isolation
- Severity: Medium | Likelihood: Low–Medium | Risk: Medium
- Description: NVIDIA driver/CUDA advisories can impact confidentiality/integrity; shared GPUs risk cross-tenant leakage if isolation is weak.
- Affected: GPU execution environments in containers or shared servers.
- Detection: Track NVIDIA advisories; verify runtime profiles; inventory driver/CUDA versions.
- Remediation: Pin and regularly update CUDA/driver, align with torch wheels; enforce non-root containers, minimal capabilities, seccomp/AppArmor; limit device access.

#### F-05: CLI and Temp-File Safety
- Severity: Medium | Likelihood: Medium | Risk: Medium
- Description: Path traversal, inadequate validation of user inputs, and insecure temp directories can introduce risks. The conversion script performs filesystem operations; ensure robust validation and safe file handling.
- Affected: scripts/pascal_voc_to_yolo.py and examples/.
- Detection: Manual review and Bandit checks (e.g., for unsafe usage patterns).
- Remediation: Strict argparse validation (types, ranges), pathlib.Path resolve() checks, avoid shell=True for any subprocesses, use tempfile with secure defaults, and sanitize output paths.

#### F-06: Configuration and Secrets Handling
- Severity: Medium | Likelihood: Medium | Risk: Medium
- Description: No documented environment variables or secrets policy; risk of ad-hoc environment use and inadvertent logging of sensitive values.
- Remediation: Provide .env.example (no secrets), centralize configuration loading with validation, and document policy for secrets management and logging redaction.

#### F-07: Logging Privacy and Metadata Leakage
- Severity: Low–Medium | Likelihood: Medium | Risk: Low–Medium
- Description: File paths and dataset identifiers can be exposed in logs, potentially leaking sensitive information about data sources or structure.
- Remediation: Redact sensitive content, minimize metadata in logs, and set appropriate log levels and retention.

### 8.x Category Summaries (optional)
- Model Integrity: F-01
- Input Handling: F-02, F-05
- Supply Chain: F-03
- GPU/Hardware: F-04
- Configuration/Privacy: F-06, F-07

## 9. Risk Evaluation and Prioritization
- Risk Matrix: Qualitative Likelihood x Impact mapping (Low/Medium/High).
- Top Risks (linked to Sections 8.0 and 8.1):
  - R1: Unsafe deserialization/model loading (evidence to be updated from Bandit in 8.0)
  - R2: Dependency/supply chain vulnerabilities (evidence to be updated from SCA in 8.1)
  - R3: Input parsing/DoS vectors (XML/media validations; see 8.0 hotspots)
  - R4: GPU runtime/driver CVEs and isolation
  - R5: Configuration/logging privacy gaps
- Quick Wins vs Strategic:
  - Quick wins: dependency pinning and SCA in CI, checksum verification for weights, argparse validation in scripts.
  - Strategic: adopt safetensors and signatures for weights, SBOM and signed releases, sandboxing and container hardening.

## 10. Remediation Plan
### 10.1 Immediate (0–30 days)
- Introduce pinned constraints and lockfiles for CPU and GPU; align torch/torchvision versions to supported CUDA variants.
- Implement a safe model loader with checksum verification and guidance to prefer state_dict/safetensors.
- Provide input validation helpers (size/format/duration limits); integrate with example scripts.
- Run Bandit and pip-audit/OSV; triage issues and document outcomes.

### 10.2 Near Term (30–90 days)
- Enforce SAST/SCA in CI and fail on High/Critical without explicit exception.
- Generate SBOM (CycloneDX) as part of release artifacts.
- Harden scripts: strict argparse, safe temp dirs, sanitize paths; ensure no shell=True exists now or in future contributions.
- Add SECURITY.md with reporting and supported versions policy.
- For pycocotools, pin to a vetted commit with checksum or replace with packaged release.

### 10.3 Long Term (>90 days)
- Signed wheels and reproducible builds; publish provenance/attestations (SLSA).
- Provide container hardening guidance/profiles (non-root, seccomp/AppArmor, read-only rootfs).
- Establish continuous monitoring for NVIDIA advisories and scheduled dependency updates.

### 10.4 Owners, Targets, and Success Criteria
- Owners: Dependencies (Maintainer/Deps Owner), Model IO (Model IO Owner), Parsers (Parsers Owner), CI/CD and Release (Release Eng), Runtime (Security Lead).
- Targets: Tracked in Risk Register below.
- Success: SCA shows no unaddressed High/Critical; Bandit free of High; safe loader and input validators adopted in examples; SBOM and signed artifacts delivered.

## 11. Security Hardening Guidance
### 11.1 Safe Input Handling
- Whitelist image formats; use PIL to check MIME and size; enforce max resolution (for example, 4096x4096) and fail fast.
- For videos, enforce max duration, resolution, and frame rates; restrict codecs; consider timeouts and early abort on decode errors.
- Consider sandboxing media parsing in worker processes when needed for robustness.

### 11.2 Model Security
- Disallow arbitrary pickle loading; favor state_dict checkpoints and safetensors.
- Verify checksums/signatures before loading; publish official hashes for recommended weights.
- Restrict file locations for model loads to trusted directories where feasible.

### 11.3 Dependency Policy
- Maintain separate CPU and GPU constraints; use pip-tools/uv to generate lockfiles with hashes.
- Run SCA on PRs and nightly; require remediation or explicit exception for High/Critical.
- Avoid Git-based dependencies; if necessary, pin to a specific commit and verify integrity.

### 11.4 Runtime Isolation
- Container guidance: run as non-root, read-only rootfs, minimal capabilities, seccomp/AppArmor; bind-mount inputs read-only when possible.
- Establish least privilege on filesystem and device access.

### 11.5 GPU Hygiene
- Pin CUDA and driver versions to PyTorch’s compatibility matrix; monitor NVIDIA advisories.
- Use nvidia-container-toolkit with minimal device mappings; prefer explicit GPU selection via CUDA_VISIBLE_DEVICES.

### 11.6 Secrets Management
- Do not store secrets in the repo. Use external secret stores; rotate keys regularly.
- Provide .env.example for documentation only; never commit real secrets.

### 11.7 Logging and Privacy
- Redact sensitive values; avoid logging full paths; employ structured logging with configurable levels and retention.

### 11.8 Secure CLI Patterns
- argparse types and range validation; normalize and resolve paths; avoid directory traversal; never use shell=True in subprocess; use tempfile for secure temporary storage.

## 12. Validation and Verification
### 12.1 Test Coverage
- Add unit tests for input validators and safe model loader.
- Add integration tests covering boundary conditions (max sizes/durations) and negative cases with malformed inputs.

### 12.2 Fuzzing Strategy
- Target image and video decoding paths and annotation parsers using Hypothesis/Atheris; develop a seed corpus of malformed samples.

### 12.3 Regression Testing
- For each fix, add regression tests and acceptance criteria to prevent reintroduction.

### 12.4 Continuous Monitoring
- Scheduled SCA and SAST; NVIDIA CVE monitoring; automated dependency update PRs validated by CI.

## 13. Incident Response and Disclosure
### 13.1 Vulnerability Reporting
- Provide a security contact and SLA in SECURITY.md; triage and respond according to severity.

### 13.2 Advisories and Patch Releases
- Issue coordinated security advisories and patch releases; backport Critical/High fixes to supported branches; provide mitigations if patching is delayed.

### 13.3 Rollback and Contingency
- Maintain last-known-good constraints and rollback instructions; keep previous stable wheels accessible.

## 14. Compliance and Licensing Considerations
### 14.1 Third-Party Licensing
- Track licenses of frameworks and dependencies via SBOM; ensure compatibility with project licensing.

### 14.2 Privacy/Data Protection
- If datasets contain PII, ensure compliance with applicable regulations and organizational policies; minimize and anonymize where possible.

### 14.3 Export Controls
- Assess export controls for models and cryptography as applicable to distribution regions.

## 15. Risk Register
ID | Title | Category | Severity | Owner | Status | Target Date | Notes
---|---|---|---|---|---|---|---
R1 | Unsafe deserialization | Model Integrity | High | Model IO Owner | Open | 30d | Prefer safetensors/state_dict; checksums/signatures
R2 | Dependency CVEs | Supply Chain | High | Deps Owner | Open | 14d | Add pip-audit/OSV in CI; constraints/lockfiles with hashes
R3 | Media parsing DoS | Input Handling | Medium | Parsers Owner | Open | 45d | Add validators and fuzzing; enforce limits
R4 | GPU runtime/driver CVEs | Environment/GPU | Medium | Security Lead | Open | 60d | Pin/update drivers; container isolation guidance
R5 | Git-sourced dependency integrity | Supply Chain | Medium | Maintainers | Open | 30d | Pin pycocotools to commit or replace with packaged alternative

## 16. Appendices
### 16.1 Dependency Inventory
If an SBOM is not yet available, maintain a lightweight dependency inventory derived from requirements files. Replace placeholders with exact pinned versions when constraints/lockfiles are created.

- Source files:
  - requirements.txt
  - requirements_gpu.txt
  - requirements_extra.txt

- Inventory (placeholder until pinned):
  | Package           | Declared Version Range/Pin     | Source File               | Notes                                |
  |-------------------|--------------------------------|---------------------------|--------------------------------------|
  | pillow            | >=7.0.0                        | requirements.txt/gpu      | Monitor Pillow CVEs; pin once SCA reviewed |
  | numpy             | >=1.18.1                       | requirements.txt/gpu      | Native code; CVE-prone; pin hashes   |
  | opencv-python     | >=4.1.2                        | requirements.txt/gpu      | Native; frequent CVEs; pin hashes    |
  | torch             | >=1.9.0 (cpu index)            | requirements.txt          | Align with CPU wheel index           |
  | torchvision       | >=0.10.0 (cpu index)           | requirements.txt          | Align with torch version             |
  | torch             | >=1.9.0 (cu102 index)          | requirements_gpu.txt      | Ensure CUDA compatibility            |
  | torchvision       | >=0.10.0 (cu102 index)         | requirements_gpu.txt      | Ensure CUDA compatibility            |
  | scipy             | >=1.7.3                        | requirements.txt/gpu      |                                      |
  | matplotlib        | >=3.4.3                        | requirements.txt/gpu      |                                      |
  | tqdm              | ==4.64.1                       | requirements.txt/gpu      |                                      |
  | pytest            | ==7.1.3                        | requirements.txt/gpu      | Dev/test dependency                  |
  | mock              | ==4.0.3                        | requirements.txt/gpu      | Dev/test dependency                  |
  | cython            | (unversioned)                  | requirements.txt/gpu      | Prefer version pin                   |
  | pycocotools       | git+https (repo/branch commit) | requirements_extra.txt     | Pin commit or replace with packaged release |

When SBOM is generated (CycloneDX), supersede this table with an authoritative SBOM reference.

### 16.2 Environment Matrix
OS (Ubuntu LTS/Windows/macOS), Python versions, CUDA/driver versions aligned with torch/vision wheel compatibility.

### 16.3 Configuration Baseline
Add .env.example for documentation with non-secret defaults; central configuration loader recommended.

### 16.4 Tool Output Artifacts
- Bandit (SAST):
  - Artifact: bandit-report.json
  - Command used: bandit -r . -f json -o bandit-report.json
- pip-audit (SCA):
  - Artifact: pip-audit-report.json
  - Example command: pip-audit -r requirements.txt -r requirements_gpu.txt -r requirements_extra.txt -f json -o pip-audit-report.json
- OSV-Scanner (SCA) [optional/additional]:
  - Artifact: osv-scanner-report.json
  - Example command: osv-scanner --lock requirements.txt --lock requirements_gpu.txt --lock requirements_extra.txt --json > osv-scanner-report.json
- Linting:
  - Ruff/Flake8 outputs (optional): ruff.txt / flake8.txt

Note: Artifacts should be stored at the repository root or under docs/security/artifacts/ and referenced here accordingly.

### 16.5 Glossary
- SAST: Static Application Security Testing
- SCA: Software Composition Analysis
- CVE: Common Vulnerabilities and Exposures
- CUDA: Compute Unified Device Architecture
- SBOM: Software Bill of Materials

### 16.6 Document Control (Distribution and References quick copy)
- Distribution and Access: see 3.2
- References: see 3.3
