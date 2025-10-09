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
