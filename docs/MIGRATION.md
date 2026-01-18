# 项目重构迁移指南

本文档说明了项目重构前后的文件对应关系和代码迁移方法。

## 📋 文件对应关系

### 旧文件 → 新文件映射

| 旧文件路径 | 新文件路径 | 说明 |
|-----------|-----------|------|
| `Config.py` | `src/config/settings.py` | 配置文件，增加了更多路径配置 |
| `detect_tools.py` | `src/utils/visualization.py` | 可视化工具函数 |
| `imgTest.py` | `scripts/detect_image.py` | 图片检测脚本 |
| `VideoTest.py` | `scripts/detect_video.py` | 视频检测脚本 |
| `CameraTest.py` | `scripts/detect_camera.py` | 摄像头检测脚本 |
| `train.py` | `scripts/train_model.py` | 模型训练脚本 |
| `YOLO_PlateRecognition.py` | `src/core/pipeline.py` | 封装为类 |
| `Font/platech.ttf` | `assets/fonts/platech.ttf` | 字体文件 |
| `models/best.pt` | `models/yolo/best.pt` | YOLO模型 |
| `paddleModels/whl/*` | `models/paddle/*` | PaddleOCR模型 |
| `TestFiles/*` | `data/test_images/*` | 测试文件 |

## 🔧 代码迁移示例

### 1. 导入路径变化

**旧代码：**
```python
import Config
import detect_tools as tools
```

**新代码：**
```python
from src.config import settings
from src.utils import visualization
```

### 2. 使用配置文件

**旧代码：**
```python
model_path = 'models/best.pt'
font_path = 'Font/platech.ttf'
```

**新代码：**
```python
from src.config import settings

model_path = settings.YOLO_MODEL_PATH
font_path = settings.FONT_PATH
```

### 3. 使用新的类封装

**旧代码（直接调用）：**
```python
from ultralytics import YOLO
from paddleocr import PaddleOCR
import detect_tools as tools

# 加载模型
model = YOLO('models/best.pt')
ocr = PaddleOCR(...)

# 检测
results = model(image)[0]
boxes = results.boxes.xyxy.tolist()

# 识别
for box in boxes:
    crop_img = image[y1:y2, x1:x2]
    result = ocr.ocr(crop_img)
    # ...
```

**新代码（使用类）：**
```python
from src.core.pipeline import PlatePipeline

# 创建流程实例
pipeline = PlatePipeline()

# 一行代码完成检测和识别
boxes, license_list, conf_list = pipeline.process_image(image)

# 绘制结果
image = pipeline.draw_results(image, boxes, license_list)
```

## 🚀 新功能优势

### 1. 更简洁的API
- 使用 `PlatePipeline` 类一次性完成检测和识别
- 自动处理图像裁剪和结果整合

### 2. 更好的可维护性
- 代码模块化，职责清晰
- 配置集中管理，易于修改

### 3. 更强的扩展性
- 可以轻松替换检测或识别模型
- 支持自定义参数配置

## 📝 快速开始

### 运行新版本脚本

```bash
# 图片检测
python scripts/detect_image.py

# 视频检测
python scripts/detect_video.py

# 摄像头检测
python scripts/detect_camera.py

# 模型训练
python scripts/train_model.py
```

### 在代码中使用

```python
from src.core.detector import PlateDetector
from src.core.recognizer import PlateRecognizer
from src.core.pipeline import PlatePipeline

# 方式1: 使用完整流程
pipeline = PlatePipeline()
boxes, plates, confs = pipeline.process_image("image.jpg")

# 方式2: 分别使用检测和识别
detector = PlateDetector()
recognizer = PlateRecognizer()

boxes = detector.get_plate_boxes("image.jpg")
plate_images = detector.crop_plates(image, boxes)
results = recognizer.recognize_batch(plate_images)
```

## ⚠️ 注意事项

1. **路径问题**：新版本使用绝对路径，确保从项目根目录运行脚本
2. **模型位置**：模型文件已移动到新位置，旧脚本需要更新路径
3. **兼容性**：旧版本脚本仍然保留在根目录，可以继续使用

## 🔄 逐步迁移建议

1. 先测试新版本脚本是否正常工作
2. 逐步将自定义代码迁移到新的API
3. 更新所有硬编码的路径为配置文件中的路径
4. 完成迁移后可以删除旧版本文件

