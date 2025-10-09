# Security Vulnerabilities – ImageAI-4381

This document summarizes the consolidated security analysis for ImageAI-4381 and complements the modular detailed report under docs/security and the generated consolidated SECURITY-REPORT.* files.

## Executive Summary
The primary risks are supply-chain and integrity-related: unpinned dependencies (including GPU profiles), absence of model checksum verification, and a Git-based dependency for pycocotools. No network service is exposed; threats are centered on local execution, artifact integrity, and downstream usage patterns. Priority actions are pinning dependencies, enabling CI scans and SBOM, enforcing model integrity checks, and hardening path handling in examples/CLI.

## Key Risks (Prioritized)
- Critical: Unpinned/transitive dependency CVEs; lack of model file checksum validation.
- High: Empty install_requires; Git-based dependency drift risk.
- Medium: Insecure download guidance; environment mismatches; data privacy concerns.
- Low: Path handling patterns from examples that may be misused downstream.

## Where to Find the Full Report
- Modular sections: docs/security/
- Consolidated report (Markdown): docs/security/SECURITY-REPORT.md
- Consolidated report (PDF, build via script): docs/security/SECURITY-REPORT.pdf

To build the PDF:
- python3 scripts/build_security_report.py
- If successful, copy to repository root with the requested name:
  - cp docs/security/SECURITY-REPORT.pdf security_vulnerabilities_report.pdf
