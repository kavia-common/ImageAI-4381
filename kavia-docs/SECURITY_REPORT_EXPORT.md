# Exporting the Security Vulnerabilities Report (PDF)

Requested output files:
- PDF: security_vulnerabilities_report.pdf (repository root)
- Markdown: SECURITY_VULNERABILITIES.md (repository root)

Steps:
1) Build the consolidated report and PDF:
   - python3 scripts/build_security_report.py

2) Copy the generated PDF to the requested filename at the repository root:
   - cp docs/security/SECURITY-REPORT.pdf security_vulnerabilities_report.pdf

Notes:
- If PDF generation fails, install pandoc and wkhtmltopdf or use the Python fallback (pip install markdown weasyprint) as supported by scripts/build_security_report.py.
