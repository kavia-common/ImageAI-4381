# Static Analysis and Secrets

## Dangerous Patterns Review
The inspected modules do not include direct use of eval/exec, shell=True subprocess calls, or unsafe YAML/pickle loaders. However, PyTorch checkpoint loading may execute arbitrary code paths when loading objects beyond raw state_dicts, so model files should be treated as untrusted unless verified. Path usage in examples accepts user-supplied file paths without canonicalization, which can be unsafe if consumers reuse these patterns in multi-user or service contexts. The current extension validation in imageai/backend_check/model_extension.py correctly rejects .h5 files and enforces .pt/.pth, but it does not perform checksum validation.

## Secrets and Credentials
There are no hardcoded secrets in the inspected files, and no .env-based configuration is present for this container. Nonetheless, future contributions could accidentally introduce secrets.

## Recommendations
- Deserialization hygiene: Prefer loading weights via state_dict-only flows where feasible and document that untrusted checkpoints can be dangerous.
- Checksum verification: Provide a small utility function to verify SHA256 checksums for model files and document how to use it before loading.
- Path handling: In examples and CLI, canonicalize and validate files before access, and avoid writing outputs alongside inputs by default.
- Secret scanning in CI: Add a lightweight secrets scanning step (e.g., gitleaks or trufflehog) to prevent accidental inclusion of API keys or credentials in future changes.

### Example checksum utility
```python
import hashlib
from pathlib import Path

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_checksum(path: Path, expected_sha256: str) -> None:
    actual = sha256_file(path)
    if actual.lower() != expected_sha256.lower():
        raise ValueError(f"Checksum mismatch for {path}. Expected {expected_sha256}, got {actual}.")
```
