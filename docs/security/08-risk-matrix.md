# Risk Matrix

| ID | Risk | Severity | Likelihood | Remediation Effort | Priority | Rationale |
|---|---|---|---|---|---|---|
| VR-001 | Unpinned/transitive dependency CVEs | Critical | High | Medium | P1 | Unpinned CPU/GPU wheels with wide surface area |
| VR-002 | No model file integrity verification | Critical | High | Medium | P1 | Trojaned weights common across ML ecosystems |
| VR-003 | Empty install_requires in setup.py | High | Medium | Low | P1 | Consumers may install insecure combinations |
| VR-004 | Git-based pycocotools dependency | High | Medium | Medium | P2 | Moving target undermines reproducibility |
| VR-005 | Insecure artifact download guidance | Medium | Medium | Low | P2 | Remediated via docs + helper code |
| VR-006 | Path handling for user inputs | Low | Medium | Medium | P3 | Library usage pattern; risk in downstream apps |
