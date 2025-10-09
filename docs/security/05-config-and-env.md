# Configuration and Environment

## Environment Variables and Defaults
There is no .env file defined for this container. Configuration primarily occurs through function parameters and CLI arguments. Defaults should be conservative: avoid writing outputs adjacent to inputs, do not follow symlinks for model files by default, and error loudly on ambiguous paths.

## GPU/CPU Profiles
requirements_gpu.txt uses PyTorch extra-index URLs for CUDA 10.2-specific wheels. Users may have different CUDA toolkits and drivers. GPU environments should be treated as distinct, tested profiles with explicit documentation on supported driver/toolkit combinations. Provide a CPU-only constraints file and validate it as the secure baseline.

## Network and TLS
When downloading model weights or datasets, enforce HTTPS and validate TLS certificates. Document how to perform offline installation using vetted wheels with checksums. Avoid guidance that disables certificate verification.

## Packaging and Installation
setup.py currently specifies install_requires=[]; populate it with minimal, security-vetted bounds aligned to constraints files. This protects consumers who install via pip without reading requirements files. Provide per-profile constraints (CPU, CUDA variants) and ensure CI validates them regularly.
