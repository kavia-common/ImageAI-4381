# Runtime/Execution Threat Model

## Contexts Considered
- Local development: Single-user workstations processing local media.
- Server-side batch processing: Automated jobs handling user-supplied media at scale.
- Embedded usage: Integrated into larger applications/services.
- Handling user-supplied images/videos/models: Untrusted inputs and artifacts.

## Data Flow Narrative
Inputs (images/videos/models) -> Preprocessing -> Model load/execute -> Postprocessing -> Outputs.
Trust boundaries:
- External artifacts (models, media) cross into the process
- Filesystem paths provided by users
- Optional network locations for downloads (via user code)

## STRIDE Considerations
- Spoofing: Maliciously named model files or swapped artifacts.
- Tampering: Modified model binaries; path traversal in file I/O.
- Repudiation: Lack of logging for artifact verification events.
- Information Disclosure: Verbose errors exposing paths/config.
- Denial of Service: Large/malformed inputs; resource exhaustion on GPU/CPU.
- Elevation of Privilege: Not directly applicable unless combined with external tooling/subprocess.

## Threats
| Threat | Vector | Asset | Mitigation | Residual Risk |
|---|---|---|---|---|
| Unverified model file | Swapped .pt/.pth | Model integrity | Enforce SHA256 verification before load | Low |
| Path traversal | Crafted paths | Filesystem | Normalize and validate paths; restrict to allowed dirs | Low–Medium |
| Dependency CVEs | Vulnerable transitive deps | Process/system | CI dependency scanning; constraints; prompt upgrades | Medium |
| DoS via large inputs | Oversized media | Availability | Input size checks; timeouts; resource limits | Medium |
| Info leakage in logs | Verbose errors | Privacy | Sanitize exceptions; avoid dumping paths | Low |
| GPU misconfig | Incompatible CUDA wheels | Stability | Separate profiles; preflight checks | Low |

