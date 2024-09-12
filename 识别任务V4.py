import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from paddleocr import PaddleOCR, draw_ocr
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 设置环境变量以避免某些库的兼容问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 设置PaddleOCR模型的路径
cls_model_dir = 'paddleModels/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
rec_model_dir = 'paddleModels/whl/rec/ch/ch_PP-OCRv4_rec_infer'

# 初始化PaddleOCR，设置使用角度分类器
ocr = PaddleOCR(use_angle_cls=True, lang="ch", cls_model_dir=cls_model_dir, rec_model_dir=rec_model_dir)

# 指定图像路径
img_path = 'test.jpg'

# 进行OCR识别
results = ocr.ocr(img_path, cls=True)

# 加载图像
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError("图像文件未找到，请确保文件路径正确或者文件存在。")

# 处理每一行的结果
for line in results:
    # 每一行的结果包含坐标和文本信息
    for item in line:
        points, text, confidence = item[0], item[1][0], item[1][1]
        points = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        # 绘制多边形
        cv2.polylines(img, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        # 添加文本
        cv2.putText(img, f"{text} ({confidence:.2f})", (points[0][0][0], points[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# 使用matplotlib显示图像
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
