# Mukh

<div align="center">

[![Downloads](https://static.pepy.tech/personalized-badge/mukh?period=total&units=international_system&left_color=grey&right_color=blue&left_text=downloads)](https://pepy.tech/project/mukh)
[![Documentation](https://img.shields.io/badge/docs-View%20Documentation-blue.svg?style=flat)](https://ishandutta0098.github.io/mukh/)
[![Stars](https://img.shields.io/github/stars/ishandutta0098/mukh?color=yellow&style=flat&label=%E2%AD%90%20stars)](https://github.com/ishandutta0098/mukh/stargazers)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat)](https://github.com/ishandutta0098/mukh/blob/master/LICENSE)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-@ishandutta0098-blue.svg?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ishandutta0098)
[![Twitter](https://img.shields.io/:follow-@ishandutta0098-blue.svg?style=flat&logo=x)](https://twitter.com/intent/user?screen_name=ishandutta0098)
[![YouTube](https://img.shields.io/badge/YouTube-@ishandutta--ai-red?style=flat&logo=youtube)](https://www.youtube.com/@ishandutta-ai)

</div>

Mukh (मुख, meaning "face" in Sanskrit) is a comprehensive face analysis library that provides unified APIs for various face-related tasks. It simplifies the process of working with multiple face analysis models through a consistent interface.

## Features

- 🎯 **Unified API**: Single, consistent interface for multiple face analysis tasks
- 🔄 **Model Flexibility**: Support for multiple models per task
- 🛠️ **Custom Pipelines**: Optimized preprocessing and model combinations
- 📊 **Evaluator Mode**: Intelligent model recommendations based on your dataset
- 🚀 **Easy to Use**: Simple, intuitive APIs for quick integration

## Currently Supported Tasks

- Face Detection
- Facial Landmark Prediction

## Installation

```bash
pip install mukh
```

## Usage

### Face Detection

```python
import cv2
from mukh.detection import FaceDetector

# Initialize detector
detection_model = "blazeface" # Available models: "blazeface", "mediapipe", "ultralight"
detector = FaceDetector.create(detection_model)

# Detect faces
image_path = "path/to/image.jpg"
faces, annotated_image = detector.detect_with_landmarks(image_path)

# Save output
output_path = "path/to/output.jpg"
cv2.imwrite(output_path, annotated_image)
```

## Contact

For questions and feedback, please open an issue on GitHub.
