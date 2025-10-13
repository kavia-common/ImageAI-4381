# ImageAI-4381: Hierarchical Execution Plan

## Executive Summary
This execution plan defines a hierarchical roadmap to maintain and evolve ImageAI-4381 with a CPU-first, PyTorch-first posture while preserving legacy TensorFlow code within the imageai_tf_deprecated namespace. The scope covers image classification, object detection, video analysis, and custom model training across high-level phases, detailed sequenced tasks, in-depth technical considerations, and specific features with acceptance criteria. The plan emphasizes deterministic execution, CI-friendly constraints, minimal diffs in code changes, clear packaging/requirements alignment across CPU and GPU environments, and strict isolation for any deprecated TensorFlow components.

Objectives:
- Ensure stable CPU-first operation by default with PyTorch as the primary backend.
- Maintain optional GPU enablement through explicit requirements_gpu.txt flow.
- Isolate all TensorFlow/Keras-based logic under imageai_tf_deprecated with no accidental runtime cross-over.
- Strengthen tests and examples to be deterministic, reproducible, and efficient for CI.
- Provide an auditable plan with clear sequencing, dependencies, risks, and mitigations.

## High-level Phases
1. Baseline Stabilization and Environment Alignment
2. Backend Guardrails and TF Deprecated Isolation Reinforcement
3. Feature Hardening for Classification and Object Detection
4. Video Analysis Pipeline Quality and Performance Pass
5. Custom Training UX and Reliability Improvements
6. Packaging, Requirements, and Determinism Enhancements
7. CI Readiness, Test Coverage Expansion, and Example Validation
8. Documentation, Migration Guidance, and Release Readiness

## Detailed Tasks per Phase (with file/module touchpoints and acceptance criteria)
### Phase 1: Baseline Stabilization and Environment Alignment
Tasks:
1. Review requirements alignment for CPU-first and GPU variants.
   - Touchpoints: requirements.txt, requirements_gpu.txt, requirements_extra.txt, setup.py
   - Actions: Verify PyTorch/TorchVision CPU wheels via extra-index URLs, confirm GPU file points to compatible CUDA extra-index URLs. Avoid conflicting pins between CPU/GPU files.
   - Acceptance Criteria:
     - Clean pip installs on fresh venvs for CPU and GPU variants.
     - No import errors when running basic examples and tests.

2. Confirm backend gate loads on import and prevents TF-first usage.
   - Touchpoints: imageai/__init__.py, imageai/backend_check/backend_check.py
   - Actions: Validate error messaging paths for missing PyTorch vs accidental TF install.
   - Acceptance Criteria:
     - Import imageai on CPU-only environment succeeds when torch/torchvision present.
     - Meaningful RuntimeError when torch/torchvision absent or TF is found first.

3. Ensure examples and tests reference CPU-friendly defaults.
   - Touchpoints: examples/*.py, test/*.py
   - Actions: Confirm tests use small inputs and skip or mark GPU-only paths unless explicitly enabled.
   - Acceptance Criteria:
     - Tests pass locally on CPU in a constrained CI-like environment.

### Phase 2: Backend Guardrails and TF Deprecated Isolation Reinforcement
Tasks:
1. Strengthen extension checks and clear error paths.
   - Touchpoints: imageai/backend_check/model_extension.py
   - Actions: Re-validate that .pt/.pth map to PyTorch paths and .h5/.ckpt are rejected with instructive messages for deprecated TF usage.
   - Acceptance Criteria:
     - Loading mismatched extensions yields actionable error messages pointing to imageai_tf_deprecated or legacy versions.

2. Namespace isolation audit for deprecated TF code.
   - Touchpoints: imageai_tf_deprecated/**
   - Actions: Ensure no imports from deprecated tree leak into imageai/ (PyTorch tree) at runtime or setup. Retain code as-is for historical compatibility within its own namespace.
   - Acceptance Criteria:
     - Importing imageai does not import imageai_tf_deprecated modules.
     - Running PyTorch examples/tests does not trigger TF/Keras imports.

### Phase 3: Feature Hardening for Classification and Object Detection
Tasks:
1. Classification API verification and determinism.
   - Touchpoints: imageai/Classification/__init__.py, imageai/Classification/Custom/{__init__.py,data_transformation.py,training_params.py}, imageai/Classification/README.md
   - Actions: Validate model selection, weight loading, and classifyImage flow; set deterministic seeds for CPU (torch.manual_seed, numpy, Python random if used); verify top-k outputs with stable ordering when probabilities tie.
   - Acceptance Criteria:
     - Example classification scripts run deterministically across re-runs.
     - Unit tests in test/test_image_classification.py and test/test_custom_classification.py pass reliably.

2. Object detection API verification and determinism.
   - Touchpoints: imageai/Detection/__init__.py, imageai/Detection/Custom/yolo/{dataset.py,compute_loss.py,metric.py,validate.py,custom_anchors.py}, imageai/Detection/README.md
   - Actions: Validate setModelTypeAs* flows, weight loading, detectObjectsFromImage/image+video pipelines; enforce seeds in data loaders and transforms for reproducibility; confirm non-max suppression parameters are documented and used consistently.
   - Acceptance Criteria:
     - test/test_object_detection.py and test/test_custom_object_detection.py pass consistently in CPU constrained runs.
     - Outputs stable within tolerance (e.g., bounding box ordering documented).

### Phase 4: Video Analysis Pipeline Quality and Performance Pass
Tasks:
1. Validate per-second and per-frame video utilities with bounded resource use.
   - Touchpoints: examples/video_object_detection.py, examples/video_analysis_per_second.py, examples/video_analysis_per_frame.py, test/test_video_object_detection.py, test/test_custom_video_detection.py
   - Actions: Ensure small sample videos used in tests; provide frame sampling knobs; add seed setting before transformations.
   - Acceptance Criteria:
     - Video tests pass on CI within reasonable time budget.
     - No excessive memory growth across frames; optional downscale documented.

### Phase 5: Custom Training UX and Reliability Improvements
Tasks:
1. Classification training consistency.
   - Touchpoints: imageai/Classification/Custom/{__init__.py,training_params.py}, test/test_custom_classification_training.py
   - Actions: Validate parameter defaults for CPU training; ensure reproducible results across small epochs; document data directory structures.
   - Acceptance Criteria:
     - Training tests finish within CI limits and produce expected model artifact paths.

2. Detection training data and anchors.
   - Touchpoints: imageai/Detection/Custom/{__init__.py}, imageai/Detection/Custom/yolo/{dataset.py,custom_anchors.py}, scripts/pascal_voc_to_yolo.py, test/test_custom_detection_training.py
   - Actions: Confirm dataset parsing/label transforms; provide deterministic anchor generation seeds; ensure dataset converter guidance is clear.
   - Acceptance Criteria:
     - Custom detection training test passes, with model artifacts created in expected locations.

### Phase 6: Packaging, Requirements, and Determinism Enhancements
Tasks:
1. Requirements parity and extras.
   - Touchpoints: requirements.txt, requirements_gpu.txt, requirements_extra.txt, MANIFEST.in
   - Actions: Verify extras (e.g., pycocotools) are optional; document when to use extras for COCO flows; ensure MANIFEST includes docs where necessary.
   - Acceptance Criteria:
     - CPU install requires no CUDA; GPU install follows requirements_gpu.txt; extras install successfully when needed.

2. Deterministic defaults and seeds.
   - Touchpoints: Library initialization points in classification/detection where randomness may occur.
   - Actions: Provide simple helper or documented code snippet to set seeds (torch, numpy, random); recommend torch.set_deterministic_algorithms where supported.
   - Acceptance Criteria:
     - Repeated runs on same inputs produce consistent outputs within documented tolerances.

### Phase 7: CI Readiness, Test Coverage Expansion, and Example Validation
Tasks:
1. Test stability in CI.
   - Touchpoints: test/*.py
   - Actions: Ensure all tests pass under CPU-only environment, with reduced data sizes and fast paths; mark long-running tests as optional.
   - Acceptance Criteria:
     - CI can run the default test suite in <10–15 minutes without GPU.

2. Example scripts validation.
   - Touchpoints: examples/*.py, data-images/*, data-videos/*
   - Actions: Validate examples run to completion with current APIs; update paths/constants where needed to reference repository data.
   - Acceptance Criteria:
     - All examples that rely on included assets run successfully on CPU with clear outputs.

### Phase 8: Documentation, Migration Guidance, and Release Readiness
Tasks:
1. Architecture and migration docs alignment.
   - Touchpoints: docs/architecture.md, imageai/backend_check/backend_check.py
   - Actions: Ensure docs highlight CPU-first, PyTorch-first policy; add explicit migration guidance from TF to PyTorch; reference deprecated namespace.
   - Acceptance Criteria:
     - Architecture doc updated, consistent with code; links to deprecated directory guidelines present.

2. Release checklist and notes.
   - Touchpoints: README.md, CHANGELOG (if added), docs/*
   - Actions: Include release notes with tested Python versions, dependency pins strategy, and deterministic guidance; include checksum guidance for weights.
   - Acceptance Criteria:
     - Release notes drafted; install/run instructions validated on clean environments.

## In-depth Technical Considerations and Risks
- Backend posture: The import guard at imageai/backend_check/backend_check.py attempts torch/torchvision first and raises if absent, while catching accidental TF usage to steer users to legacy versions. This must remain minimal to avoid import overhead while ensuring clear errors.
- Determinism: True bitwise determinism may vary across architectures and library versions. The plan targets practical, repeatable outputs via seeds, avoiding nondeterministic cuDNN algorithms when on GPU, and stable sorting/documented tolerances for detection post-processing.
- Performance on CPU: Prefer smaller default models and downscaled inputs in examples/tests. Document options to reduce resolution or frames for video paths.
- Packaging: setup.py currently delegates dependency management to requirements files. Ensure docs instruct users to create venvs and install the correct file per environment (CPU, GPU, extras).
- TF isolation: All TensorFlow/Keras implementations exist under imageai_tf_deprecated and must not be imported in the primary package tree. Any example or doc snippet referencing TF belongs only in the deprecated namespace documentation.

Risks:
- Environment drift between CPU and GPU requirements may cause inconsistent behavior or install failures.
- Upstream dependency CVEs (OpenCV, Pillow, NumPy) require ongoing monitoring and pin updates.
- Model weight deserialization risks; mitigate via guidance to use state_dict-only .pth/.pt where possible and verify checksums.

Mitigations:
- Maintain clear CPU vs GPU requirements files with compatible pins.
- Document safe model-loading patterns and checksum verification examples.
- Keep example/test datasets small and curated to avoid long runtimes and memory pressure.

## Specific Feature Breakdowns (Classification, Object Detection, Video Analysis, Custom Training)
### Classification
Scope:
- Backbones: MobileNetV2, ResNet50, InceptionV3, DenseNet121.
- APIs: Model selection, setModelPath, loadModel, classifyImage.

Acceptance Criteria:
- Loading each supported backbone works with appropriate weights.
- classifyImage returns top-k labels with probabilities; stable across re-runs with seeds set.
- Tests: test/test_image_classification.py, test/test_custom_classification.py pass on CPU.

### Object Detection
Scope:
- Models: RetinaNet, YOLOv3, TinyYOLOv3.
- APIs: setModelTypeAs*, setModelPath, loadModel, detectObjectsFromImage; custom detection training utilities under imageai/Detection/Custom.

Acceptance Criteria:
- Image detection returns bounding boxes, classes, and probabilities, saving outputs and optionally extracting objects.
- Non-max suppression parameters are documented; outputs deterministic within tolerance with seeds set.
- Tests: test/test_object_detection.py, test/test_custom_object_detection.py pass on CPU.

### Video Analysis
Scope:
- VideoObjectDetection and examples for per-frame and per-second analysis.

Acceptance Criteria:
- Video examples run to completion on provided sample videos with CPU-only; options to downscale and frame-skip documented.
- Callbacks work as documented; test/test_video_object_detection.py and test/test_custom_video_detection.py pass reliably under CI constraints.

### Custom Training
Scope:
- Classification and detection training with configurable parameters, dataset utilities, and anchors.

Acceptance Criteria:
- Training tests (classification and detection) complete within CI timeboxes on small datasets, producing expected model artifacts.
- Deterministic seeds reduce run-to-run variance; datasets and directory structures are documented and validated.

## Sequencing and Dependencies
- Phase 1 precedes all other phases; requirements and backend import guard must be stable before feature hardening.
- Phase 2 must complete before expanding tests or refactoring examples to ensure TF isolation is enforced.
- Phase 3 and Phase 4 can proceed in parallel after Phase 2, with shared dependency on deterministic utilities (seeds).
- Phase 5 (training) depends on confirmed stable inference and dataset utilities from Phases 3–4.
- Phase 6 (packaging/determinism) integrates with earlier phases to finalize environment guidance.
- Phase 7 (CI/tests) depends on stabilized features and deterministic settings.
- Phase 8 (docs/release) finalizes after all prior phases converge.

## Deliverables and Acceptance Criteria
- Updated requirements files validated for CPU and GPU installs.
- Verified backend guardrails with meaningful error messages.
- Passing test suite in CPU-only CI, including classification, detection, and video tests.
- Documented deterministic execution steps (seed setup) and resource bounds guidance.
- Migration notes clarifying PyTorch-first posture and TF deprecated isolation.
- Examples validated against repository assets on CPU-only.

## Appendix: Deprecated TensorFlow Isolation Policy
- All TensorFlow/Keras code resides strictly under imageai_tf_deprecated/.
- The primary imageai package must not import or depend on imageai_tf_deprecated at import time or runtime for PyTorch flows.
- Any examples or READMEs related to TF remain only under imageai_tf_deprecated documentation files and directories.
- Error messages guide users to install legacy versions (e.g., <=2.1.6) for TF usage or to use the deprecated namespace explicitly.
- No new features will be added to the deprecated TF tree; security fixes only if required.

## In-depth Technical Considerations and Risks (Expanded)
- CPU-first defaults:
  - requirements.txt pins CPU wheels for torch/torchvision via extra index URLs.
  - Examples and tests should not assume CUDA is present; avoid torch.cuda.is_available() dependencies in default paths.
- PyTorch-first enforcement:
  - imageai/backend_check/backend_check.py ensures torch/torchvision presence and provides explicit RuntimeError otherwise.
  - model_extension checks refuse TF-formatted weights in PyTorch codepaths and direct users to the deprecated namespace.
- Determinism:
  - Recommended seed setting sequence (illustrative):
    - import random; import numpy as np; import torch
    - random.seed(1337); np.random.seed(1337); torch.manual_seed(1337)
    - If GPU: torch.backends.cudnn.deterministic = True; torch.backends.cudnn.benchmark = False
  - Document that some operations may still vary slightly based on library versions.
- CI-friendly constraints:
  - Prefer small sample images/videos and short epoch training in tests.
  - Provide options in examples to reduce resolution or frame rate.
- Packaging:
  - Users must choose requirements.txt for CPU and requirements_gpu.txt for GPU; requirements_extra.txt adds pycocotools for COCO flows.

## Risks & Mitigations
- Risk: Dependency drift causing incompatible wheels.
  - Mitigation: Regularly validate installs; track PyTorch installation guidance; keep extra-index URLs updated.
- Risk: Nondeterministic outputs breaking tests.
  - Mitigation: Set seeds; stable post-processing ordering; tolerate small numeric differences with thresholds in assertions.
- Risk: Accidental TF usage.
  - Mitigation: Strong backend guards; clear errors; docs emphasize deprecated TF namespace isolation.
- Risk: Long CI runtimes for video and training tests.
  - Mitigation: Use minimal datasets; lower resolution; fewer iterations; mark heavy tests as optional.

## References to Code Touchpoints
- Backend guardrails: imageai/__init__.py; imageai/backend_check/backend_check.py; imageai/backend_check/model_extension.py
- Classification: imageai/Classification/__init__.py; imageai/Classification/Custom/{__init__.py,data_transformation.py,training_params.py}
- Detection and Custom YOLO: imageai/Detection/__init__.py; imageai/Detection/Custom/{__init__.py}; imageai/Detection/Custom/yolo/{dataset.py,compute_loss.py,metric.py,validate.py,custom_anchors.py}
- Examples: examples/*
- Tests: test/*
- Requirements and packaging: requirements.txt; requirements_gpu.txt; requirements_extra.txt; MANIFEST.in; setup.py
- Deprecated TF isolation: imageai_tf_deprecated/**

---
Page header: ImageAI-4381 Execution Plan
Page footer: Kavia Orchestrator • v1.0
