import os

import numpy as np

# Set environment variable to avoid library conflicts
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import cv2
from paddleocr import PaddleOCR, draw_ocr


cls_model_dir = 'paddleModels/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
rec_model_dir = 'paddleModels/whl/rec/ch/ch_PP-OCRv4_rec_infer'

# Initialize the PaddleOCR model with specific paths
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=False, cls_model_dir=cls_model_dir, rec_model_dir=rec_model_dir)

# Define the path of the image to be processed
img_path = 'TestFiles/014453125-90_269-261&439_483&505-481&505_262&504_261&439_483&442-1_0_5_29_32_30_32_30-72-59.jpg'

# Perform OCR on the image
results = ocr.ocr(img_path, cls=True)

# Read the original image for annotation
image = cv2.imread(img_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert color from BGR to RGB

# 绘制边界框和文本
for line in results:
    for item in line:
        if len(item) >= 4:
            box, _, text, confidence = item
            # 绘制边界框
            box = [[int(vertex[0]), int(vertex[1])] for vertex in box]
            pts = np.array(box, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # 绘制文本
            text_loc = (box[0][0], box[0][1] - 10)
            cv2.putText(image, f'{text} ({confidence:.2f})', text_loc, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        else:
            print("Unexpected result format:", item)

# 转换颜色空间，以便使用cv2.imshow正常显示
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# 显示图像
cv2.imshow('Annotated Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
