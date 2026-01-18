# 快速开始指南

欢迎使用车牌检测与识别系统！本指南将帮助你快速上手。

## 📋 前置要求

- Python 3.8+
- pip 包管理器
- （可选）GPU 和 CUDA（用于加速）

## 🚀 5分钟快速开始

### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2: 准备模型文件

确保以下模型文件已放置在正确位置：

- YOLO模型: `models/yolo/best.pt`
- PaddleOCR模型: `models/paddle/`

### 步骤 3: 运行检测

**检测图片：**
```bash
python main.py image -i data/test_images/your_image.jpg
```

**检测视频：**
```bash
python main.py video -v data/test_videos/your_video.mp4
```

**使用摄像头：**
```bash
python main.py camera
```

## 💡 常用命令

### 图片检测

```bash
# 基本检测
python main.py image -i test.jpg

# 保存结果
python main.py image -i test.jpg -o result.jpg

# 不显示窗口
python main.py image -i test.jpg --no-display
```

### 视频检测

```bash
# 基本检测
python main.py video -v test.mp4

# 保存结果
python main.py video -v test.mp4 -o result.mp4

# 跳帧处理（提高速度）
python main.py video -v test.mp4 --skip-frames 3
```

### 摄像头检测

```bash
# 自动查找摄像头
python main.py camera

# 指定摄像头ID
python main.py camera -c 0

# 显示FPS
python main.py camera --show-fps

# 录制视频
python main.py camera -o recording.mp4
```

## 🎮 快捷键

- **图片模式**: 按任意键退出
- **视频模式**:
  - `q` - 退出
  - `p` - 暂停/继续
- **摄像头模式**:
  - `q` - 退出
  - `s` - 截图

## 📊 输出说明

检测完成后，你会看到：

1. **控制台输出**: 检测到的车牌号码、置信度、位置
2. **可视化窗口**: 带有标注的图像/视频
3. **保存文件**: （如果指定了 `-o` 参数）

## 🔧 常见问题

### 1. 找不到模型文件

确保模型文件在正确的位置：
- `models/yolo/best.pt`
- `models/paddle/cls/`, `models/paddle/det/`, `models/paddle/rec/`

### 2. 摄像头无法打开

尝试指定摄像头ID：
```bash
python main.py camera -c 0  # 或 1, 2, 3...
```

### 3. 处理速度慢

- 使用跳帧: `--skip-frames 2`
- 降低分辨率
- 使用GPU加速

## 📚 更多信息

- 完整文档: 查看 `README.md`
- API使用: 查看 `docs/MIGRATION.md`
- 问题反馈: GitHub Issues

---

祝你使用愉快！🎉
