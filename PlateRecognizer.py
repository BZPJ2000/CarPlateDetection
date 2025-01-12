#coding:utf-8
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import cv2
from ultralytics import YOLO
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



fontC = ImageFont.truetype("Font/platech.ttf", 50, 0)
# 加载ocr模型
cls_model_dir = 'paddleModels/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
rec_model_dir = 'paddleModels/whl/rec/ch/ch_PP-OCRv4_rec_infer'
ocr = PaddleOCR(use_angle_cls=False, lang="ch", det=False, cls_model_dir=cls_model_dir,rec_model_dir=rec_model_dir)

# 所需加载的模型目录
path = 'models/best.pt'
model = YOLO(path, task='detect')


video_path = "test.mp4"

cap = cv2.VideoCapture(video_path)
while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model(frame)[0]

        location_list = results.boxes.xyxy.tolist()
        if len(location_list) >= 1:
            location_list = [list(map(int, e)) for e in location_list]
            # 截取每个车牌区域的照片
            license_imgs = []
            for each in location_list:
                x1, y1, x2, y2 = each
                cropImg = frame[y1:y2, x1:x2]
                license_imgs.append(cropImg)
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
                frame = tools.drawRectBox(frame, box, text, fontC)

        frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        cv2.imshow("YOLOv8 Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()