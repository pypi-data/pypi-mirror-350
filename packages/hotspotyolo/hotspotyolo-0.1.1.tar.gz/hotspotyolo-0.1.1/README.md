# hotspotyolo

## Overview
The `hotspotyolo` is a Python package designed for generating heatmaps using the YOLOv8 - v11 model. It provides an easy-to-use interface for visualizing model predictions and understanding the decision-making process of the YOLOv8 architecture.

## Parameters

The `params` dictionary configures how the heatmap is generated and visualized. Here’s a description of each parameter:

- **weight** (`str`): Path to the YOLO model weights file (e.g., `"best.pt"`).
- **device** (`str`): Device to run inference on. Use `"cuda:0"` for GPU or `"cpu"` for CPU.
- **method** (`str`): The XAI method to use for heatmap generation. Supported options include: `"GradCAMPlusPlus"`, `"GradCAM"`, `"XGradCAM"`, `"EigenCAM"`, `"HiResCAM"`, `"LayerCAM"`, `"RandomCAM"`, `"EigenGradCAM"`, `"KPCA_CAM"`.
- **layer** (`list[int]`): List of layer indices to target for heatmap extraction. Example: `[21]`.
- **backward_type** (`str`): Specifies which outputs to use for backpropagation. Options depend on the task:
  - `detect`: `<class, box, all>`
  - `segment`: `<class, box, segment, all>`
  - `pose`: `<box, keypoint, all>`
  - `obb`: `<box, angle, all>`
  - `classify`: `<all>`
- **conf_threshold** (`float`): Confidence threshold for detections (e.g., `0.2`).
- **ratio** (`float`): Ratio that decides how many detections we should consider in forward pass. (recommended range: `0.02`–`0.1`).
- **show_result** (`bool`): If `True`, displays the result with heatmaps overlaid. Set to `False` to skip visualization.
- **renormalize** (`bool`): If `True`, renormalizes the heatmap for better visualization.
- **task** (`str`): Task type. Supported values: `"detect"`, `"segment"`, `"pose"`, `"obb"`, `"classify"`.
- **img_size** (`int`): Input image size for the model (e.g., `1280`).
- **save_metadata** (`bool`): If `True`, saves additional metadata in the output folder.

Adjust these parameters as needed for your specific use case and model.



## Installation
You can install the latest release directly from PyPI:
```
pip install hotspotyolo
```

To install the package, clone the repository and run the following command:
```
pip install -e .
```

If you already have requirements.txt then do this most of you will have it. 
```
pip install . --no-deps
```

## Usage

```python

from hotspotyolo import yolo_heatmap
image_path = "sample.png"
model_weight = "best.pt"
output_folder = 'test_result'

params = {
    'weight': model_weight,
    'device': 'cuda:0',
    'method': 'GradCAMPlusPlus', 
    'layer': [21],
    'backward_type': 'all',
    'conf_threshold': 0.2, 
    'ratio': 0.02, 
    'show_result': True, 
    'renormalize': True, 
    'task':'obb', 
    'img_size':640, 
    'save_metadata': True, 
}

model = yolo_heatmap(**params)
model(image_path, output_folder)
```

## Results 

### OBB CAM
![OBB CAM Example](results/obb/result.png)

### Detection CAM
![Detection CAM Example](results/detect/result.png)

### Segmentation CAM
![Segmentation CAM Example](results/seg/result.png)

### Classification CAM
![Classification CAM Example](results/classify/result.png)


## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## Important
Right now the pose model is not working.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.