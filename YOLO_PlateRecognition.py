#coding:utf-8
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from ultralytics import YOLO
import cv2
import detect_tools as tools
from PIL import ImageFont
from paddleocr import PaddleOCR


def get_license_result(ocr,image):
    """
    image:输入的车牌截取照片
    输出，车牌号与置信度
    """
    result = ocr.ocr(image, cls=True)[0]
    if result:
        license_name, conf = result[0][1]
        if '·' in license_name:
            license_name = license_name.replace('·', '')
        return license_name, conf
    else:
        return None, None

img_path = "TestFiles/013671875-90_268-248&480_423&559-419&546_248&559_250&482_423&480-0_0_3_24_25_32_28_30-153-86.jpg"

now_img = tools.img_cvread(img_path)

fontC = ImageFont.truetype("Font/platech.ttf", 50, 0)
# 加载ocr模型
cls_model_dir = 'paddleModels/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
rec_model_dir = 'paddleModels/whl/rec/ch/ch_PP-OCRv4_rec_infer'
ocr = PaddleOCR(use_angle_cls=False, lang="ch", det=False, cls_model_dir=cls_model_dir,rec_model_dir=rec_model_dir)
# 所需加载的模型目录
path = 'models/best.pt'
# 加载预训练模型
model = YOLO(path, task='detect')
# 检测图片
results = model(img_path)[0]
location_list = results.boxes.xyxy.tolist()
if len(location_list) >= 1:
    location_list = [list(map(int, e)) for e in location_list]
    # 截取每个车牌区域的照片
    license_imgs = []
    for each in location_list:
        x1, y1, x2, y2 = each
        cropImg = now_img[y1:y2, x1:x2]
        license_imgs.append(cropImg)
        cv2.imshow('111',cropImg)
        cv2.waitKey(0)
    # 车牌识别结果
    lisence_res = []
    conf_list = []
    for each in license_imgs:
        license_num, conf = get_license_result(ocr, each)
        if license_num:
            lisence_res.append(license_num)
            conf_list.append(conf)
        else:
            lisence_res.append('无法识别')
            conf_list.append(0)
    for text, box in zip(lisence_res, location_list):
        now_img = tools.drawRectBox(now_img, box, text, fontC)
now_img = cv2.resize(now_img,dsize=None,fx=0.5,fy=0.5,interpolation=cv2.INTER_LINEAR)
cv2.imshow("YOLOv8 Detection", now_img)
cv2.waitKey(0)





