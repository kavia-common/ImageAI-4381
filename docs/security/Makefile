# Simple Makefile to generate SECURITY-REPORT.md and SECURITY-REPORT.pdf
# Usage:
#   make           # default target -> all
#   make md
#   make pdf
#   make clean

PYTHON ?= python3
ROOT := $(abspath $(CURDIR)/../..)
SCRIPT := $(ROOT)/scripts/build_security_report.py
SEC_DIR := $(ROOT)/docs/security
MD := $(SEC_DIR)/SECURITY-REPORT.md
PDF := $(SEC_DIR)/SECURITY-REPORT.pdf

.PHONY: all md pdf clean

all: md pdf

md:
	$(PYTHON) $(SCRIPT) --only-md

pdf:
	$(PYTHON) $(SCRIPT)

clean:
	@rm -f $(MD) $(PDF)
	@echo "Cleaned generated security report artifacts."
