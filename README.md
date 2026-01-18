
# 车牌检测与识别系统 v2.0

本项目是一个基于 **YOLOv8** 和 **PaddleOCR** 的车牌检测与识别系统。系统能够从图像、视频或摄像头中检测车牌，并高精度识别车牌号码。

## ✨ 特性

- 🚀 **高性能检测**: 基于YOLOv8的快速车牌定位
- 🎯 **高精度识别**: 使用PaddleOCR进行车牌号码识别
- 📷 **多种输入源**: 支持图片、视频文件、实时摄像头
- 🎨 **友好界面**: 清晰的命令行输出和可视化结果
- 🔧 **易于使用**: 统一的主入口，简单的命令行参数
- 📦 **模块化设计**: 清晰的代码结构，易于维护和扩展

---

## 📂 项目结构

```
CarPlateDetection/
├── main.py                    # 主入口脚本（推荐使用）
├── README.md                  # 项目文档
├── requirements.txt           # 依赖库列表
├── .gitignore                # Git忽略配置
│
├── src/                      # 源代码（核心功能）
│   ├── core/                 # 核心模块
│   │   ├── detector.py       # 车牌检测
│   │   ├── recognizer.py     # 车牌识别
│   │   └── pipeline.py       # 完整流程
│   ├── utils/                # 工具函数
│   │   └── visualization.py  # 可视化工具
│   └── config/               # 配置管理
│       └── settings.py       # 路径和参数配置
│
├── scripts/                  # 独立脚本（也可单独运行）
│   ├── detect_image.py       # 图片检测
│   ├── detect_video.py       # 视频检测
│   └── detect_camera.py      # 摄像头检测
│
├── models/                   # 模型文件
│   ├── yolo/                 # YOLO模型
│   └── paddle/               # PaddleOCR模型
│
├── data/                     # 数据目录
│   ├── test_images/          # 测试图片
│   ├── test_videos/          # 测试视频
│   └── datasets/             # 训练数据集
│
├── assets/                   # 资源文件
│   └── fonts/                # 字体文件
│
├── outputs/                  # 输出结果
│   ├── images/               # 图片检测结果
│   └── videos/               # 视频检测结果
│
└── legacy/                   # 旧版本文件（兼容保留）
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

## 🚀 快速开始

### 方式一：使用主入口（推荐）

```bash
# 图片检测
python main.py image -i path/to/image.jpg

# 视频检测
python main.py video -v path/to/video.mp4

# 摄像头检测
python main.py camera
```

### 方式二：直接运行脚本

```bash
# 图片检测
python scripts/detect_image.py --image path/to/image.jpg

# 视频检测
python scripts/detect_video.py --video path/to/video.mp4

# 摄像头检测
python scripts/detect_camera.py
```

---

## 📖 详细使用说明

### 1. 图片检测

```bash
# 基本用法
python main.py image -i test.jpg

# 保存结果
python main.py image -i test.jpg -o result.jpg

# 不显示窗口（仅保存）
python main.py image -i test.jpg -o result.jpg --no-display

# 调整显示比例
python main.py image -i test.jpg --scale 0.8
```

**输出示例：**
```
============================================================
           车牌检测与识别系统 - 图片检测模式
============================================================

输入图片: test.jpg
正在加载模型...
✓ 模型加载成功

正在处理图片...

------------------------------------------------------------
检测结果:
------------------------------------------------------------
  检测到 2 个车牌

  [1] 车牌号码: 京A12345
      置信度: 95.30%
      位置: (120, 200) -> (350, 280)

  [2] 车牌号码: 沪B67890
      置信度: 92.15%
      位置: (450, 180) -> (680, 260)

  处理耗时: 0.523 秒
------------------------------------------------------------
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
- **模块化设计**：代码结构清晰，易于维护和扩展。
- **Python API**：提供简洁的API接口，方便集成到其他项目中。

---

## 🔄 项目结构优化说明

本项目已进行结构优化，主要改进包括：

### 1. 模块化设计
- 将核心功能封装成独立的类（`PlateDetector`、`PlateRecognizer`、`PlatePipeline`）
- 分离工具函数和配置文件，提高代码复用性

### 2. 清晰的目录结构
- `src/` - 所有源代码
- `scripts/` - 可执行脚本
- `models/` - 模型文件
- `data/` - 数据文件
- `outputs/` - 输出结果

### 3. 统一的路径管理
- 使用 `src/config/settings.py` 统一管理所有路径
- 支持相对路径和绝对路径自动转换

### 4. 兼容性
- 保留了旧版本的脚本文件（根目录下的 `.py` 文件）
- 新旧代码可以共存，方便逐步迁移

---

## 🤝 致谢

- [YOLO by Ultralytics](https://github.com/ultralytics/yolov8)
- [PaddleOCR by PaddlePaddle](https://github.com/PaddlePaddle/PaddleOCR)

