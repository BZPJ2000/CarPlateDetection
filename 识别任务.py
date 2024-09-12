from paddleocr import PaddleOCR, draw_ocr
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from paddleocr import PaddleOCR
cls_model_dir = 'paddleModels/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
rec_model_dir = 'paddleModels/whl/rec/ch/ch_PP-OCRv4_rec_infer'
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=False, cls_model_dir=cls_model_dir, rec_model_dir=rec_model_dir)
img_path = '测试图片.jpg'
results = ocr.ocr(img_path, cls=True)
for line in results:
    for item in line:
        if len(item) >= 4:
            _, _, text, confidence = item
            print("Text:", text)
            print("Confidence:", confidence)
        else:
            print("Unexpected result format:", item)
