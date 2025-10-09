#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build Security Report

This script deterministically merges multiple Markdown files listed in docs/security/_order.txt
into a single SECURITY-REPORT.md with a generated title page and table of contents,
then attempts to export a PDF SECURITY-REPORT.pdf using the following toolchain order:

1) Pandoc + wkhtmltopdf (preferred if available)
2) Pandoc + WeasyPrint (fallback via pandoc --pdf-engine=weasyprint)
3) Pure Python: markdown to HTML + WeasyPrint (fallback)
4) If no PDF toolchain is available, it will still generate SECURITY-REPORT.md and print
   clear instructions to install pandoc and wkhtmltopdf or weasyprint.

Usage:
  python3 scripts/build_security_report.py [--only-md | --only-pdf]

- Default (no flags): builds md and then tries to build pdf.
- --only-md: only generates SECURITY-REPORT.md
- --only-pdf: expects md to exist, only attempts PDF.

Exit codes:
  0 on success; non-zero on errors (missing files, conversion failure, etc.)
"""

import os
import sys
import subprocess
import shutil
import datetime
import tempfile

from pathlib import Path
from typing import List, Optional


BASE_DIR = Path(__file__).resolve().parents[1]
SEC_DIR = BASE_DIR / "docs" / "security"
ORDER_FILE = SEC_DIR / "_order.txt"
OUTPUT_MD = SEC_DIR / "SECURITY-REPORT.md"
OUTPUT_PDF = SEC_DIR / "SECURITY-REPORT.pdf"

# Basic CSS styling for HTML/PDF output
CSS_STYLES = """
/* Security Report Styles */
@page {
  size: A4;
  margin: 20mm;
}
body {
  font-family: "DejaVu Sans", Arial, Helvetica, sans-serif;
  line-height: 1.5;
  color: #222;
  font-size: 11pt;
}
h1, h2, h3, h4, h5, h6 {
  color: #111;
  margin-top: 1.2em;
  margin-bottom: 0.5em;
  font-weight: 700;
}
h1 { font-size: 24pt; border-bottom: 2px solid #444; padding-bottom: 6px; }
h2 { font-size: 18pt; border-bottom: 1px solid #666; padding-bottom: 4px; }
h3 { font-size: 14pt; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 10pt;
}
th, td {
  border: 1px solid #999;
  padding: 6px 8px;
  text-align: left;
}
thead th {
  background: #f0f0f0;
}
code, pre {
  background: #f7f7f7;
  border: 1px solid #e0e0e0;
}
pre {
  padding: 10px;
  overflow-x: auto;
}
.toc {
  page-break-after: always;
}
.page-break {
  page-break-before: always;
}
.title-page {
  text-align: center;
  margin-top: 25%;
}
.title-page h1 {
  font-size: 28pt;
  margin-bottom: 0.2em;
}
.title-page .meta {
  margin-top: 1.5em;
  color: #555;
}
"""

# HTML wrapper template used by the Python+WeasyPrint fallback
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def check_cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_cmd(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def read_order_file(order_path: Path) -> List[Path]:
    if not order_path.exists():
        eprint(f"Order file not found: {order_path}")
        sys.exit(2)
    items: List[Path] = []
    with order_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = (SEC_DIR / Path(line)).resolve()
            if not p.exists():
                eprint(f"Missing file listed in order: {line} -> {p}")
                sys.exit(3)
            items.append(p)
    if not items:
        eprint("Order file is empty after filtering comments/blank lines.")
        sys.exit(4)
    return items


def build_title_page(project_name: str) -> str:
    today = datetime.date.today().isoformat()
    title_md = f"""<!-- Generated Title Page -->
<div class="title-page">
<h1>{project_name} Security Report</h1>
<div class="meta">
<p>Date: {today}</p>
<p>Repository: {project_name}</p>
</div>
</div>

<div class="toc">
## Table of Contents
[TOC]
</div>

"""
    return title_md


def insert_page_break() -> str:
    return "\n<div class=\"page-break\"></div>\n"


def generate_security_report_md(order_files: List[Path], out_md: Path, project_name: str) -> None:
    contents: List[str] = []
    contents.append(build_title_page(project_name))
    # Merge files with page breaks
    for idx, p in enumerate(order_files):
        with p.open("r", encoding="utf-8") as f:
            text = f.read().strip()
        # Ensure each section starts on a new "page" in PDF by adding page-break before (except first content section after TOC)
        if idx == 0:
            # First content file after the TOC gets a break to start fresh
            contents.append(insert_page_break())
        else:
            contents.append(insert_page_break())
        contents.append(f"<!-- Begin: {p.name} -->\n")
        contents.append(text)
        contents.append(f"\n<!-- End: {p.name} -->\n")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    with out_md.open("w", encoding="utf-8") as f:
        f.write("\n".join(contents))


def try_pandoc_pdf_with_wkhtmltopdf(md_path: Path, pdf_path: Path) -> bool:
    if not check_cmd_exists("pandoc"):
        return False
    if not check_cmd_exists("wkhtmltopdf"):
        return False
    # Build temporary CSS file for pandoc to include
    with tempfile.TemporaryDirectory() as td:
        css_file = Path(td) / "style.css"
        css_file.write_text(CSS_STYLES, encoding="utf-8")
        # Replace our [TOC] marker with pandoc's table-of-contents option
        # pandoc will auto-gen TOC with --toc; keep [TOC] harmless in content.
        cmd = [
            "pandoc",
            str(md_path),
            "--from", "markdown+yaml_metadata_block+table_captions+pipe_tables+autolink_bare_uris",
            "--toc",
            "--pdf-engine=wkhtmltopdf",
            "--css", str(css_file),
            "-V", "geometry:margin=20mm",
            "-V", "toc-title:Table of Contents",
            "-o", str(pdf_path)
        ]
        proc = run_cmd(cmd)
        if proc.returncode == 0 and pdf_path.exists():
            return True
        eprint("Pandoc + wkhtmltopdf failed.")
        eprint(proc.stdout)
        eprint(proc.stderr)
        return False


def try_pandoc_pdf_with_weasyprint(md_path: Path, pdf_path: Path) -> bool:
    if not check_cmd_exists("pandoc"):
        return False
    # weasyprint binary may not exist; pandoc expects the engine name "weasyprint" if the python pkg is installed
    # However, in many envs pandoc cannot directly use python weasyprint. We'll still try.
    with tempfile.TemporaryDirectory() as td:
        css_file = Path(td) / "style.css"
        css_file.write_text(CSS_STYLES, encoding="utf-8")
        cmd = [
            "pandoc",
            str(md_path),
            "--from", "markdown+yaml_metadata_block+table_captions+pipe_tables+autolink_bare_uris",
            "--toc",
            "--pdf-engine=weasyprint",
            "--css", str(css_file),
            "-V", "geometry:margin=20mm",
            "-V", "toc-title:Table of Contents",
            "-o", str(pdf_path)
        ]
        proc = run_cmd(cmd)
        if proc.returncode == 0 and pdf_path.exists():
            return True
        eprint("Pandoc + weasyprint failed.")
        eprint(proc.stdout)
        eprint(proc.stderr)
        return False


def try_python_weasyprint(md_path: Path, pdf_path: Path, title: str) -> bool:
    # Fallback: use python markdown + weasyprint
    try:
        import markdown  # type: ignore
    except Exception as ex:
        eprint("Python fallback requires the 'markdown' package. Not available.")
        eprint(str(ex))
        return False
    try:
        from weasyprint import HTML, CSS  # type: ignore
    except Exception as ex:
        eprint("Python fallback requires the 'weasyprint' package. Not available.")
        eprint(str(ex))
        return False

    md_text = md_path.read_text(encoding="utf-8")
    # Replace [TOC] with a minimal generated TOC: we can do a simple approach by leaving [TOC]
    # because python-markdown can produce TOC via extension if configured. Let's enable toc.
    # We'll use markdown with 'toc' extension to auto-generate an internal TOC.
    html_body = markdown.markdown(
        md_text,
        extensions=[
            "toc",
            "tables",
            "fenced_code",
            "sane_lists",
            "codehilite",
            "attr_list"
        ],
        extension_configs={
            "toc": {
                "permalink": True,
                "title": "Table of Contents"
            }
        }
    )
    html = HTML_TEMPLATE.format(title=title, css=CSS_STYLES, body=html_body)
    try:
        HTML(string=html, base_url=str(SEC_DIR)).write_pdf(str(pdf_path), stylesheets=[])
        return pdf_path.exists()
    except Exception as ex:
        eprint("Python WeasyPrint conversion failed.")
        eprint(str(ex))
        return False


def main(argv: List[str]) -> int:
    only_md = "--only-md" in argv
    only_pdf = "--only-pdf" in argv
    project_name = BASE_DIR.name

    order_files = read_order_file(ORDER_FILE)

    # When only building PDF, ensure MD exists
    if not only_pdf:
        try:
            generate_security_report_md(order_files, OUTPUT_MD, project_name)
            print(f"Generated: {OUTPUT_MD}")
        except Exception as ex:
            eprint(f"Failed to generate {OUTPUT_MD}: {ex}")
            return 5

    if only_md:
        return 0

    # Build PDF
    # Try Pandoc + wkhtmltopdf
    if try_pandoc_pdf_with_wkhtmltopdf(OUTPUT_MD, OUTPUT_PDF):
        print(f"Generated: {OUTPUT_PDF} (pandoc + wkhtmltopdf)")
        return 0

    # Try Pandoc + weasyprint
    if try_pandoc_pdf_with_weasyprint(OUTPUT_MD, OUTPUT_PDF):
        print(f"Generated: {OUTPUT_PDF} (pandoc + weasyprint)")
        return 0

    # Try Python markdown + WeasyPrint
    if try_python_weasyprint(OUTPUT_MD, OUTPUT_PDF, f"{project_name} Security Report"):
        print(f"Generated: {OUTPUT_PDF} (python markdown + weasyprint)")
        return 0

    # If we reach here, PDF could not be generated
    eprint("Unable to generate PDF. SECURITY-REPORT.md has been created.")
    eprint("To enable PDF export, please install one of the following toolchains:")
    eprint("Preferred: pandoc + wkhtmltopdf")
    eprint("  - Install pandoc: https://pandoc.org/installing.html")
    eprint("  - Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
    eprint("Or fallback: pandoc + weasyprint (pip install weasyprint)")
    eprint("Or pure Python fallback: pip install markdown weasyprint")
    return 6


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
