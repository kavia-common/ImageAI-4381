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

