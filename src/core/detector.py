# coding:utf-8
"""
车牌检测模块
使用YOLOv8进行车牌位置检测
"""
from ultralytics import YOLO
from src.config import settings


class PlateDetector:
    """车牌检测器类"""

    def __init__(self, model_path=None, conf=None, iou=None):
        """
        初始化检测器
        :param model_path: YOLO模型路径
        :param conf: 置信度阈值
        :param iou: IoU阈值
        """
        self.model_path = model_path or settings.YOLO_MODEL_PATH
        self.conf = conf or settings.CONF_THRESHOLD
        self.iou = iou or settings.IOU_THRESHOLD
        self.model = YOLO(self.model_path, task='detect')

    def detect(self, image):
        """
        检测图像中的车牌
        :param image: 输入图像（numpy数组或图像路径）
        :return: 检测结果对象
        """
        results = self.model(image)[0]
        return results

    def get_plate_boxes(self, image):
        """
        获取车牌边界框坐标
        :param image: 输入图像
        :return: 车牌边界框列表 [[x1,y1,x2,y2], ...]
        """
        results = self.detect(image)
        location_list = results.boxes.xyxy.tolist()

        if len(location_list) >= 1:
            location_list = [list(map(int, e)) for e in location_list]
            return location_list
        return []

    def crop_plates(self, image, boxes):
        """
        根据边界框裁剪车牌区域
        :param image: 原始图像
        :param boxes: 边界框列表
        :return: 裁剪后的车牌图像列表
        """
        plate_images = []
        for box in boxes:
            x1, y1, x2, y2 = box
            crop_img = image[y1:y2, x1:x2]
            plate_images.append(crop_img)
        return plate_images
