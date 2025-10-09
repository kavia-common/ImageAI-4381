# Config and Environment Security Review

## Areas Reviewed
- ENV handling strategy: No .env present; configuration occurs via function parameters and code defaults.
- Logging and PII exposure: No direct evidence of PII logging in reviewed files; caution in downstream usage.
- CUDA/TF flags and sandboxing: backend_check ensures PyTorch primary; deprecated TensorFlow code remains in imageai_tf_deprecated.
- Model storage directories and permissions: Not explicitly enforced.

## Config Risks
| Variable/Setting | Risk | Recommended Default | Enforcement |
|---|---|---|---|
| Model file path | Unverified artifacts | Require checksum argument (SHA256) | Validate at load |
| Backend selection | Confusion with TF legacy | Default to PyTorch; block .h5 by default | Already blocked by extension; document clearly |
| GPU vs CPU installs | Mismatch/incompatibility | Separate constraints files | CI tests per profile |
| Logging level | Sensitive info leakage in downstream apps | Default to INFO; redact file paths in logs | Document best practices |
| Temp/Cache directories | Permission/leakage | Use secure temp dirs with 0700 perms | Use tempfile; document |

## Recommendations
- Introduce an optional checksum parameter to all model load functions. Reject mismatched checksums.
- Provide environment variables to control strictness (e.g., IMAGEAI_STRICT_INTEGRITY=1) and default to strict in CI.
- Document GPU vs CPU installation profiles with constraints files and expected CUDA versions.
- Encourage use of system temp directories with restricted permissions for intermediate files.

