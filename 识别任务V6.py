import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
# 设置环境变量以避免某些库的兼容问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# 设置PaddleOCR模型的路径
cls_model_dir = 'paddleModels/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
rec_model_dir = 'paddleModels/whl/rec/ch/ch_PP-OCRv4_rec_infer'
ocr = PaddleOCR(use_angle_cls=True, lang="ch", cls_model_dir=cls_model_dir, rec_model_dir=rec_model_dir)

# 指定图像路径
img_path = 'test.jpg'
results = ocr.ocr(img_path, cls=True)
# 加载图像
img = Image.open(img_path).convert('RGB')
draw = ImageDraw.Draw(img)
font_path = "Font/platech.ttf"
font = ImageFont.truetype(font_path, 40)
for line in results:
    for item in line:
        points, text, confidence = item[0], item[1][0], item[1][1]
        points = np.array(points, dtype=np.int32)
        draw.polygon([tuple(p) for p in points], outline=(0, 255, 0))
        if points.shape[0] > 0:
            draw.text((points[0][0]+100, points[0][1] - 100), f"{text} ({confidence:.2f})", fill=(255, 0, 0), font=font)
cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
plt.figure(figsize=(10, 10))
plt.imshow(cv_img)
plt.axis('off')
plt.show()









