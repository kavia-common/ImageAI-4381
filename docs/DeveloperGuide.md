# Developer Guide

## Getting Started
ImageAI-4381 is a Python library focused on simple, high-level APIs for computer vision tasks. It is designed for local development in scripts and notebooks. You can use CPU-only environments or accelerate with an NVIDIA GPU.

PDF export: To render this document to PDF locally, install pandoc and run:
- Linux/macOS: pandoc -s docs/DeveloperGuide.md -o docs/DeveloperGuide.pdf
- Windows (PowerShell): pandoc -s docs/DeveloperGuide.md -o docs/DeveloperGuide.pdf

## Local Development Setup
1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   - CPU: pip install -r requirements.txt
   - GPU: pip install -r requirements_gpu.txt (ensure your CUDA/cuDNN matches PyTorch build)
   - Extras (for training): pip install -r requirements_extra.txt
3. Editable install (optional for development): pip install -e .
4. Run tests: pytest

Python versions: 3.7–3.10 per upstream; 3.9+ recommended.

## Project Structure
- imageai/
  - backend_check/: Environment checks and model extension validation.
  - Classification/: ImageClassification class and helpers for MobileNetV2, ResNet50, InceptionV3, DenseNet121.
  - Detection/: ObjectDetection and VideoObjectDetection for YOLOv3/TinyYOLOv3 and RetinaNet.
  - Detection/Custom/: Trainers and inference classes for custom YOLO models with YOLO-format datasets.
  - yolov3/, retinanet/: Model implementations and utilities.
- examples/: Ready-to-run classification, detection, video, and training scripts.
- scripts/: Utilities like pascal_voc_to_yolo.py for dataset conversion.
- test/: Unit/integration tests for classification, detection, and video flows.
- docs/: Documentation and plans.

## How to Run Classification/Detection/Video Examples
- Classification (examples/image_prediction.py)
  - Provide backbone weight file (.pth) compatible with your chosen model.
  - Run: python examples/image_prediction.py
- Detection (examples/object_detection.py)
  - Provide YOLOv3/TinyYOLOv3 (.pt) or RetinaNet (.pth) weights.
  - Run: python examples/object_detection.py
- Video (examples/video_object_detection.py, video_analysis_per_second.py)
  - Ensure data-videos/ contains sample videos or update paths.
  - Run: python examples/video_object_detection.py

Tips:
- If you need CPU-only execution, call useCPU() on the classifier/detector before loading the model.
- Use minimum_percentage_probability to tune output density.

## Training Custom Models
- Custom Object Detection (YOLO format)
  - Prepare dataset directories (train and validation), each with images/ and annotations/ (YOLO .txt files).
  - Use imageai.Detection.Custom.DetectionModelTrainer:
    - setModelTypeAsYOLOv3() or setModelTypeAsTinyYOLOv3()
    - setDataDirectory(<path>)
    - setTrainConfig(object_names_array=[...], batch_size=..., num_experiments=..., train_from_pretrained_model=<optional>.pt)
    - trainModel()
  - Outputs:
    - models/: .pt checkpoints (best and last)
    - json/: configuration with anchors and labels
- Custom Classification
  - Use imageai/Classification/Custom/ trainer utilities and example scripts (examples/custom_model_training.py).

## Extending with New Models
- Classification backbones:
  - Follow the pattern in imageai/Classification/__init__.py; add your model to classification_models dict, normalize inputs consistently, and ensure top-k logic is preserved.
- Detection:
  - Add wrappers and utilities similar to YOLOv3/TinyYOLOv3 if integrating additional architectures.
  - Update tests to cover new flows and validate output schema (labels, probabilities, bounding boxes).

## Coding Standards and Linting
- Suggested tooling for consistency (to be added):
  - Black (formatting), isort (imports), Ruff/Flake8 (linting), mypy/pyright (typing).
- Testing:
  - Use pytest for unit and integration tests.
  - Keep tests deterministic with fixed seeds where applicable; use small fixtures in test-images/ and data-videos/.

## Contribution Guidelines
- Fork and create feature branches.
- Ensure new code paths have tests and do not break existing ones.
- Keep APIs stable; when breaking changes are unavoidable, provide migration notes.
- Document new features in examples and update docs accordingly.
- Submit PRs with:
  - Clear description of changes and rationale.
  - Test results and performance notes if applicable.

---
Conversion to PDF: See pandoc command at the beginning of this document.

