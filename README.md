
# 车牌检测与识别

本项目是一个基于 **YOLOv8** 和 **PaddleOCR** 的车牌检测与识别系统。系统能够从图像或视频中检测车牌，并高精度识别车牌号码。

---

## 📂 项目结构

```
CarPlateDetection/
├── CameraTest.py          # 基于摄像头的实时检测测试脚本
├── Config.py              # 配置文件
├── datasets/              # 数据集目录
├── detect_tools.py        # 自定义检测与可视化工具
├── Font/
│   └── platech.ttf        # 用于车牌文字显示的字体
├── imgTest.py             # 静态图片测试脚本
├── models/
│   └── best.pt            # 预训练YOLO模型
├── paddleModels/          # PaddleOCR预训练模型
│   ├── cls/               # 分类模型
│   ├── det/               # 检测模型
│   └── rec/               # 识别模型
├── paddleTest.py          # PaddleOCR测试脚本
├── PlateDetect.py         # 车牌检测脚本
├── PlateRecognizer.py     # 车牌识别脚本
├── README.md              # 项目文档
├── requirements.txt       # Python依赖库
├── runs/                  # YOLO训练输出结果
│   ├── detect/            # 检测结果
│   └── train/             # 训练结果
├── setup.py               # 项目安装脚本
├── TestFiles/             # 测试用图像与视频文件
│   ├── *.jpg              # 示例测试图片
│   ├── *.mp4              # 示例测试视频
│   └── img.png            # 示例图片
├── train.py               # YOLOv8训练脚本
├── VideoTest.py           # 视频测试脚本
├── yolov8n.pt             # YOLOv8预训练模型
└── YOLO_PlateRecognition.py  # 主程序：车牌检测与识别
```

---

## 🔧 安装方法

1. 克隆此仓库：
   ```bash
   git clone https://github.com/BZPJ2000/CarPlateDetection.git
   cd CarPlateDetection
   ```

2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```

3. 下载并放置预训练模型：
   - YOLOv8 模型：放在 `models/best.pt`
   - PaddleOCR 模型：放置在 `paddleModels/` 目录中

4. （可选）将项目设置为Python包：
   ```bash
   python setup.py install
   ```

---

## 🚀 使用方法

### 1. 图像中的车牌检测与识别
运行以下命令对静态图像进行车牌检测与识别：
```bash
python imgTest.py
```

### 2. 视频中的车牌检测与识别
运行以下命令处理视频文件：
```bash
python VideoTest.py
```

### 3. 使用摄像头进行实时检测
运行以下命令通过连接的摄像头检测车牌：
```bash
python CameraTest.py
```

### 4. 训练YOLO模型
运行以下命令在自定义数据集上训练YOLOv8模型：
```bash
python train.py
```

---

## 📋 环境依赖

- Python 3.8+
- PaddleOCR
- Ultralytics YOLOv8
- OpenCV
- PIL (Pillow)

使用以下命令安装所有依赖库：
```bash
pip install -r requirements.txt
```

---

## 🎯 功能特点

- **基于YOLOv8的车牌检测**：快速高效地检测图像或视频中的车牌位置。
- **基于OCR的文字识别**：利用PaddleOCR读取检测到的车牌号码。
- **实时处理**：支持处理视频流或实时摄像头数据。
- **高度可定制**：可以轻松在自定义数据集上训练以适应不同地区的车牌样式。
---

## 🤝 致谢

- [YOLO by Ultralytics](https://github.com/ultralytics/yolov8)
- [PaddleOCR by PaddlePaddle](https://github.com/PaddlePaddle/PaddleOCR)

