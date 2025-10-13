# API Reference (High-level)

## Installation
- CPU:
  - pip install -r requirements.txt
- GPU:
  - pip install -r requirements_gpu.txt
- Extras (training utilities):
  - pip install -r requirements_extra.txt

PDF export: To render this document to PDF locally, install pandoc and run:
- Linux/macOS: pandoc -s docs/APIReference.md -o docs/APIReference.pdf
- Windows (PowerShell): pandoc -s docs/APIReference.md -o docs/APIReference.pdf

## Initialization
Import modules from the imageai package. The core pattern is:
- Configure model type and path.
- Optionally force CPU via useCPU().
- loadModel() before inference.
- Call the appropriate inference method.

## Classification API
Module: imageai.Classification

- Class: ImageClassification
  - setModelTypeAsResNet50()
  - setModelTypeAsDenseNet121()
  - setModelTypeAsInceptionV3()
  - setModelTypeAsMobileNetV2()
  - setModelPath(path: str)
  - useCPU()
  - loadModel()
  - classifyImage(image_input: Union[str, np.ndarray, PIL.Image], result_count: int=5)
    - Returns: (List[str], List[float]) predicted labels and probabilities.

Example:
```python
from imageai.Classification import ImageClassification
import os

clf = ImageClassification()
clf.setModelTypeAsResNet50()
clf.setModelPath(os.path.join("path", "to", "resnet50-weights.pth"))
clf.loadModel()
labels, probs = clf.classifyImage("test-images/1.jpg", result_count=5)
```

## Object Detection API
Module: imageai.Detection

- Class: ObjectDetection
  - setModelTypeAsYOLOv3()
  - setModelTypeAsTinyYOLOv3()
  - setModelTypeAsRetinaNet()
  - setModelPath(path: str)
  - useCPU()
  - loadModel()
  - CustomObjects(**kwargs) -> dict
    - Build a filter dict for COCO classes (e.g., person=True, cell_phone=True).
  - detectObjectsFromImage(
      input_image: Union[str, np.ndarray, PIL.Image],
      output_image_path: str=None,
      output_type: str="file",
      extract_detected_objects: bool=False,
      minimum_percentage_probability: int=50,
      display_percentage_probability: bool=True,
      display_object_name: bool=True,
      display_box: bool=True,
      custom_objects: dict=None
    )
    - Returns:
      - If output_type="file": list of detections; optionally also list of extracted file paths.
      - If output_type="array": (np.ndarray, detections) or (np.ndarray, detections, extracted arrays).

Detection example (YOLOv3):
```python
from imageai.Detection import ObjectDetection
import os

det = ObjectDetection()
det.setModelTypeAsYOLOv3()
det.setModelPath(os.path.join("path", "to", "yolov3.pt"))
det.loadModel()
detections = det.detectObjectsFromImage(
    input_image="test-images/2.jpg",
    output_image_path="output.jpg",
    minimum_percentage_probability=40
)
```

## Video Analysis API
Module: imageai.Detection

- Class: VideoObjectDetection
  - setModelTypeAsYOLOv3(), setModelTypeAsTinyYOLOv3(), setModelTypeAsRetinaNet()
  - setModelPath(path: str)
  - useCPU()
  - loadModel()
  - CustomObjects(**kwargs)
  - detectObjectsFromVideo(
      input_file_path="",
      camera_input=None,
      output_file_path="",
      frames_per_second=20,
      frame_detection_interval=1,
      minimum_percentage_probability=50,
      log_progress=False,
      display_percentage_probability=True,
      display_object_name=True,
      display_box=True,
      save_detected_video=True,
      per_frame_function=None,
      per_second_function=None,
      per_minute_function=None,
      video_complete_function=None,
      return_detected_frame=False,
      detection_timeout=None,
      custom_objects=None
    )
  - Returns: output_video_filepath when save_detected_video=True.

## Training APIs
Module: imageai.Detection.Custom

- Class: DetectionModelTrainer
  - setModelTypeAsYOLOv3(), setModelTypeAsTinyYOLOv3()
  - setDataDirectory(data_directory: str)  # expects YOLO-format directories
  - setTrainConfig(object_names_array: List[str], batch_size: int=4, num_experiments=100, train_from_pretrained_model: str=None)
  - trainModel()  # saves models/ and json/ artifacts

- Class: CustomObjectDetection
  - setModelTypeAsYOLOv3(), setModelTypeAsTinyYOLOv3()
  - setModelPath(model_path: str)
  - setJsonPath(configuration_json: str)
  - useCPU()
  - loadModel()
  - detectObjectsFromImage(...)  # similar return signature to ObjectDetection

- Class: CustomVideoObjectDetection
  - setModelTypeAsYOLOv3(), setModelTypeAsTinyYOLOv3()
  - setModelPath(), setJsonPath(), useCPU(), loadModel()
  - detectObjectsFromVideo(...)  # similar to VideoObjectDetection

## CLI Usage
This repository does not include dedicated CLI entry points by default. Use:
- Examples: python examples/<script>.py
- Utilities: python scripts/pascal_voc_to_yolo.py

You may create thin CLI wrappers around the Python APIs if desired.

---
Conversion to PDF: See pandoc command at the beginning of this document.

