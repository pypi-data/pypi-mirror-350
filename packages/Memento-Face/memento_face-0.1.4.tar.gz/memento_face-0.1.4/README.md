
---

# Face Detection and Recognition

A PyTorch-based face detection and recognition system built with EfficientNet backbones and ArcFace loss, supporting live webcam detection and recognition, image inference, and easy embedding extraction.

---

## Table of Contents

* [Overview](#overview)
* [Model Architecture](#model-architecture)
* [Installation](#installation)
* [Usage](#usage)

  * [Detection Model](#detection-model)
  * [Recognition Model](#recognition-model)
  * [Live Webcam Testing](#live-webcam-testing)
* [Saving and Loading Weights](#saving-and-loading-weights)
* [Customizing Confidence Thresholds and Frame Skips](#customizing-confidence-thresholds-and-frame-skips)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

This repository implements a face detection and recognition pipeline consisting of:

* **DetectionModel:** Uses EfficientNet-B0 as backbone, with a custom neck and heads for bounding box and objectness prediction.
* **RecognitionModel:** Uses EfficientNet-B2 backbone, neck, pooling, and ArcFace for robust face embeddings and classification.

---

## Model Architecture

### DetectionModel

* **Backbone:** EfficientNet-B0 feature extractor (pretrained weights).
* **Neck:** Three Conv-BatchNorm-SiLU blocks reducing channel depth from 1280 to 96.
* **Heads:**

  * **BBox Head:** Predicts bounding box coordinates (4 channels).
  * **Objectness Head:** Predicts objectness confidence (1 channel).
* **Output:** Concatenated tensor of shape `[B, 5, H, W]` (bbox + objectness).
* **Decoding:** Converts network outputs to bounding boxes and confidence scores using grid and stride calculations.

### RecognitionModel

* **Backbone:** EfficientNet-B2 feature extractor.
* **Neck:** Conv-BatchNorm-SiLU block to reduce channels to embedding dimension (default 256).
* **Pooling:** Adaptive average pooling to 1x1.
* **Embedding Head:** BatchNorm and Dropout followed by normalization.
* **ArcFace:** Angular margin softmax layer for face recognition classification.
* **Output:** Either normalized embeddings or classification logits (if labels provided).

---

## Installation

To install from PyPI:

```bash
pip install MementoML
```

Make sure you have Python 3.8+ and PyTorch installed. Install dependencies:

I used Python 3.12.7.

```bash
pip install torch torchvision numpy opencv-python matplotlib pillow
```

or

```bash
pip install -r requirements.txt
```

Place the pre-trained weight files in the working directory:

* `FaceDetectionWeights.pth`
* `FaceRecognitionWeights.pth`

---

## Usage

### Detection Model

Detect faces in a single image and plot bounding boxes:

```python
from PIL import Image
import matplotlib.pyplot as plt

detector = DetectionModel(weights="FaceDetectionWeights.pth", device="cuda")
img = Image.open("test_face.jpg")
detector.face_and_plot(img, conf_thresh=0.5)
```

Run live webcam face detection:

```python
detector = DetectionModel(weights="FaceDetectionWeights.pth", device="cuda")
detector.live_test(conf_thresh=0.8, frame_skip=0)
```

---

### Recognition Model

Generate a face embedding from an image:

```python
from PIL import Image

recognizer = RecognitionModel(weights="FaceRecognitionWeights.pth", device="cuda")
img = Image.open("face_crop.jpg")
embedding = recognizer.generate_emb(img)
print(embedding.shape)  # torch.Size([256])
```

---

### Live Webcam Testing

Both detection and recognition models support live webcam testing individually:

Detection example shown above; for recognition, run your own scripts on cropped face images or saved crops.

---

## Saving and Loading Weights

Save your model weights after training:

```python
detector.save_weights("new_detection_weights.pth")
recognizer.save_weights("new_recognition_weights.pth")
```

Load weights:

```python
detector = DetectionModel(weights="new_detection_weights.pth")
recognizer = RecognitionModel(weights="new_recognition_weights.pth")
```

---

## Customizing Confidence Thresholds and Frame Skips

* **Confidence Threshold:** Adjust detection sensitivity.

```python
detector.live_test(conf_thresh=0.5)  # More sensitive, detect more faces
```

* **Frame Skip:** Process every Nth frame in live webcam feed to reduce compute.

```python
detector.live_test(frame_skip=5)  # Process every 5th frame
```

---

## Contributing

Feel free to open issues or submit pull requests. Suggestions and improvements are welcome!

---

## License

This project is licensed under the MIT License.

---

If you want me to generate examples for training, or detailed info about the ArcFace loss or anything else, just ask!
My email: [therazielmoesch@gmail.com](mailto:therazielmoesch@gmail.com)

---
