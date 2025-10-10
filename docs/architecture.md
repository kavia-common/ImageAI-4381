# ImageAI-4381 Architecture and PRD Overview

## Table of Contents
- 1. Project Overview
- 2. Key Features
- 3. Architecture Overview
- 4. Interfaces and Usage
  - Python API
  - CLI Scripts
- 5. Environment and Deployment
- 6. Dependencies and Runtime
- 7. Configuration
- 8. Roadmap and Maintenance

## 1. Project Overview
ImageAI-4381 is a Python backend library that provides easy-to-use deep learning-based image classification, object detection, video analysis, and custom model training. The project exposes a Python library interface for importing in scripts and notebooks, and includes example and helper scripts. There is no HTTP API included in this repository.

- Name: ImageAI-4381
- Description: A Python library for easy-to-use deep learning-based image and video classification, object detection, and custom model training.
- Container Type: backend (Python)
- Interfaces: Python library (import), example/utility scripts (no HTTP API)

## 2. Key Features
ImageAI-4381 supports common vision tasks and streamlines model loading, inference, and training:

- Image classification using MobileNetV2, ResNet50, InceptionV3, and DenseNet121.
- Object detection using RetinaNet, YOLOv3, and TinyYOLOv3.
- Video object detection and analysis utilities for per-frame or per-second processing.
- Custom model training for both classification and detection, including dataset preparation tools.
- A convenient Python API that favors minimal code to load models and run inference.
- Compatible with CPU-only environments and NVIDIA GPU setups via PyTorch; TensorFlow-based code is present under imageai_tf_deprecated for reference but current version uses a PyTorch backend.

## 3. Architecture Overview
The library is organized into modular packages aligned to tasks and model families. A high-level view:

- Backend selection and guardrails
  - The imageai.backend_check package verifies that PyTorch and TorchVision are available and blocks accidental TensorFlow usage for current versions.
- Task modules
  - imageai/Classification implements classification flows, model setup, and inference helpers.
  - imageai/Detection implements object detection flows for images and videos, with additional utilities for custom detections and video pipelines.
- Model wrappers and loaders
  - Each supported architecture has a thin wrapper for model loading and weight management. Classification wraps standard backbones; detection supports RetinaNet and YOLOv3 variants.
- Preprocessing and augmentation
  - Image loading and conversion rely on Pillow, OpenCV, and NumPy. Augmentation for training commonly leverages torchvision and optional libraries in extended workflows.
- Training orchestration (custom)
  - Custom classification and detection training modules expose configuration of hyperparameters, datasets, and checkpointing. The repo also includes conversion utilities (for example, scripts/pascal_voc_to_yolo.py) for preparing datasets.
- Inference utilities for batch and streaming
  - Detection provides image and video pipelines, including options to extract detected objects, tweak thresholds, and return arrays or files.

Note: TensorFlow/Keras-based implementations are preserved under imageai_tf_deprecated for historical compatibility; the active backend for v3.x is PyTorch.

## 4. Interfaces and Usage

### Python API
The primary interface is through importable classes and helpers under the imageai package. The Classification and Detection readmes include runnable examples. Typical usage patterns:

- Classification
  - Initialize and load a chosen backbone, then run classifyImage on an input.
- Detection
  - Select a detection model type (RetinaNet, YOLOv3, TinyYOLOv3), set the path to pretrained weights, load the model, and call detectObjectsFromImage or related APIs.
- Custom Training
  - Use the Custom subpackages to configure and run classification or detection training; dataset preparation utilities and parameters are provided.

Illustrative examples based on repository docs and examples:

```python
# Classification
from imageai.Classification import ImageClassification
import os

execution_path = os.getcwd()
prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth"))
prediction.loadModel()

predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, "1.jpg"), result_count=5)
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction, ":", eachProbability)
```

```python
# Object Detection (YOLOv3)
from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
detector.loadModel()

detections = detector.detectObjectsFromImage(
    input_image=os.path.join(execution_path, "image2.jpg"),
    output_image_path=os.path.join(execution_path, "image2new.jpg"),
    minimum_percentage_probability=30
)
```

### CLI Scripts
The repository does not provide dedicated CLI entry points for classification/detection by default. However, it includes example scripts under examples/ and a dataset conversion script under scripts/.

Commonly used scripts:
- examples/image_prediction.py
- examples/object_detection.py
- examples/video_object_detection.py
- examples/custom_model_training.py
- scripts/pascal_voc_to_yolo.py (dataset conversion utility)

You can run these scripts with Python to perform the desired task. If you wish to add CLI wrappers (e.g., imageai-classify/imageai-detect), they can be created as thin wrappers around the Python API.

## 5. Environment and Deployment
- Runtime: This is a Python library intended for use in Python environments such as local development, servers, or notebooks. There is no service process or HTTP server in this repo; no ports are opened.
- CPU vs GPU:
  - CPU-only operation works out of the box with requirements.txt.
  - GPU acceleration requires an NVIDIA GPU with appropriate drivers and a CUDA/cuDNN version matching the chosen PyTorch build. Use requirements_gpu.txt to install CUDA-enabled wheels from the PyTorch extra index URLs provided in that file.
- Isolation:
  - Use a dedicated virtual environment or Conda environment. For teams targeting both CPU and GPU environments, maintain distinct environments to prevent dependency mismatches.

## 6. Dependencies and Runtime
- Python: 3.7–3.10 supported by upstream README; 3.9+ recommended for new deployments.
- Core frameworks:
  - PyTorch and TorchVision (versions pinned via requirements files; CPU and CUDA variants provided).
- Vision and numerics:
  - Pillow, NumPy, OpenCV, SciPy, Matplotlib, tqdm, pytest, mock.
- Optional and extra:
  - requirements_extra.txt adds pycocotools via the specified repository for custom detection workflows.
- Installation:
  - CPU: pip install -r requirements.txt
  - GPU: pip install -r requirements_gpu.txt
  - Extras: pip install -r requirements_extra.txt

Note: Current setup.py intentionally leaves install_requires empty; rely on requirements files for environment creation.

## 7. Configuration
- .env: Not used by default in this repository; there are no required environment variables.
- Potential future variables:
  - MODEL_CACHE_DIR: Path to cache or store downloaded/pretrained weights.
  - DEFAULT_BACKEND: Backend selector if multiple backends are reintroduced.
  - CUDA_VISIBLE_DEVICES: Standard CUDA control for multi-GPU systems.
- If environment variables are introduced, include an .env.example and document variables here and in the README.

## 8. Roadmap and Maintenance
- Model export and interoperability
  - Add ONNX export and ONNX Runtime inference paths for broader deployment targets.
- Unified training APIs
  - Harmonize configuration and entry points across classification and detection training modules.
- Weights management
  - Provide integrated download helpers and checksum verification for supported backbones and detectors.
- Quality and test coverage
  - Expand tests for data loaders, model wrappers, inference utilities, and video pipelines.
  - Add performance and correctness tests using small fixtures for CI.
- Developer experience
  - Adopt Black and isort for formatting; add Ruff for linting; enforce with pre-commit hooks.
- Performance benchmarking
  - Provide a small benchmark suite contrasting CPU vs GPU performance on representative datasets and model sizes.

---
Document purpose: concise architecture and PRD overview for ImageAI-4381, aligned with the current PyTorch-centric implementation and repository-provided examples and requirements.
