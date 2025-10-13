# Product Requirements Document (PRD)

## Overview
ImageAI-4381 is a Python library that streamlines deep learning-based image and video workflows by providing simple, high-level APIs for image classification, object detection, video analysis, and custom model training. The library targets developers who want to rapidly prototype or embed computer vision capabilities without building and wiring models and preprocessing pipelines from scratch. The current implementation centers on a PyTorch backend, while legacy TensorFlow/Keras implementations are retained only for historical reference under imageai_tf_deprecated.

The project is designed for local use in scripts and notebooks. It exports a Python package (imageai) and ships example scripts; it does not expose an HTTP API. The library supports CPU environments and NVIDIA GPU acceleration for higher throughput.

PDF export: To render this document to PDF locally, install pandoc and run:
- Linux/macOS: pandoc -s docs/PRD.md -o docs/PRD.pdf
- Windows (PowerShell): pandoc -s docs/PRD.md -o docs/PRD.pdf

## Goals and Non-Goals
### Goals
- Provide a minimal, consistent Python API to:
  - Classify images using known backbones (MobileNetV2, ResNet50, InceptionV3, DenseNet121).
  - Detect objects in images and videos using RetinaNet, YOLOv3, and TinyYOLOv3.
  - Train custom classification and detection models with minimal boilerplate.
- Offer convenience features that reduce setup friction:
  - Simple model selection and weight loading.
  - Handy utilities for drawing predictions, extracting detected objects, and returning results in common formats.
  - Example scripts for common use cases, including conversion utilities (e.g., Pascal VOC to YOLO).
- Support both CPU and GPU usage paths via PyTorch and TorchVision.

### Non-Goals
- Providing a managed HTTP/REST service or server framework (no ports/services are run by this library).
- Building a comprehensive dataset labeling tool or model zoo downloader. Dataset preparation aids are minimal and focus on compatibility.
- Creating a low-level deep learning framework; ImageAI wraps existing frameworks (PyTorch/TorchVision) and focuses on usability.

## User Personas and Use Cases
### Personas
- Data Scientist: Prototyping classification/detection quickly to evaluate feasibility, with the option to fine-tune custom models.
- Backend/Automation Engineer: Embedding reliable object detection or classification into a data pipeline or a batch job.
- CV Enthusiast/Student: Learning the basics of CV tasks and experimenting with pretrained models and small datasets.

### Use Cases
- Rapid prototyping of image classification for pre-labeled datasets: Load a pretrained backbone, set the path to a .pth weight file, classify test images, and iterate.
- Batch object detection on images for downstream indexing/analytics: Iterate over an image directory, run detection with YOLOv3 or RetinaNet, and save annotated results.
- Video analytics: Process prerecorded videos frame-by-frame, aggregate detections per frame/second, and save an annotated output video.
- Custom model training: Train YOLOv3/TinyYOLOv3 detectors on custom datasets in YOLO format and use the resulting models via simple inference classes.
- Building educational demos: Use examples/ scripts to demonstrate classification, detection, and video processing with small data samples.

## Features
- Classification
  - Backbones: MobileNetV2, ResNet50, InceptionV3, DenseNet121.
  - Image input types: file path, numpy array, PIL image.
  - Top-N predictions with probabilities.
  - CPU/GPU execution; automatic GPU usage if available (overridable with useCPU()).
- Object Detection (Images)
  - Models: RetinaNet (TorchVision), YOLOv3, TinyYOLOv3.
  - Adjustable thresholds for objectness/NMS.
  - Outputs detection lists and can render annotations on images.
  - Optionally extracts detected objects as separate images/files.
  - Custom object filtering via a CustomObjects dictionary.
- Video Object Detection
  - Per-frame and interval-based detection functions.
  - Callback hooks per frame/second/minute and on completion.
  - Saves annotated videos; supports optional return of frames to callbacks.
- Custom Training
  - Detection: YOLOv3/TinyYOLOv3 trainers for datasets in YOLO format (with train and validation splits).
  - Classification: Trainer classes and params for MobileNetV2, ResNet50, InceptionV3, DenseNet121.
  - Utilities: anchors generation, dataset loaders, loss functions, and validation metrics (mAP).
- Examples and Tools
  - Example scripts for classification, detection, video analysis, and training.
  - Dataset conversion: scripts/pascal_voc_to_yolo.py.

## Success Metrics
- Developer productivity:
  - Time-to-first-result: the time to load a model and obtain predictions in a new environment.
  - Lines-of-code for a basic classification/detection setup should remain minimal.
- Reliability and stability:
  - Unit/integration tests pass across supported models and core flows.
  - Correctness of outputs on known fixtures (presence and shape of detections; valid probabilities and labels).
- Performance:
  - GPU acceleration demonstrably improves throughput in detection and video processing.
  - Reasonable memory usage on CPU-only runs for small images and clips.
- Adoption:
  - Example scripts run successfully end-to-end after installing requirements, using the provided sample assets.

## Constraints and Assumptions
- Runtime: Python 3.7–3.10 per README, with focus on 3.9+ for new deployments.
- Dependencies: PyTorch/TorchVision are required; TensorFlow/Keras code under imageai_tf_deprecated is not used in v3.x flows.
- Weights: Users provide appropriate .pth/.pt model files that match chosen backbones. The library does not download weights automatically.
- Hardware: GPU support assumes NVIDIA GPUs with CUDA that matches the installed PyTorch build.
- Dataset format for detection training: YOLO formatted data directories with train/validation split and annotations.

## Release Plan
- Current: PyTorch-centric release with classification, detection, video pipelines, and YOLOv3/TinyYOLOv3 custom training.
- Next Iterations (indicative):
  - Add optional weight download helpers and checksum verification.
  - Extend training ergonomics (config files, richer logging, and automated evaluation reports).
  - ONNX export and optional inference for portability.
  - Linting/formatting with Black, isort, Ruff, and pre-commit hooks.
  - Additional small benchmarks to guide users on CPU vs GPU trade-offs.

---
Conversion to PDF: See pandoc command at the beginning of this document.

