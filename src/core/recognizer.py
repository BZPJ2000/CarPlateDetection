# coding:utf-8
"""
车牌识别模块
使用PaddleOCR进行车牌号码识别
"""
from paddleocr import PaddleOCR
from src.config import settings


class PlateRecognizer:
    """车牌识别器类"""

    def __init__(self, cls_model_dir=None, rec_model_dir=None, use_angle_cls=False):
        """
        初始化识别器
        :param cls_model_dir: 分类模型路径
        :param rec_model_dir: 识别模型路径
        :param use_angle_cls: 是否使用角度分类
        """
        self.cls_model_dir = cls_model_dir or settings.PADDLE_CLS_MODEL
        self.rec_model_dir = rec_model_dir or settings.PADDLE_REC_MODEL
        self.ocr = PaddleOCR(
            use_angle_cls=use_angle_cls,
            lang="ch",
            det=False,
            cls_model_dir=self.cls_model_dir,
            rec_model_dir=self.rec_model_dir
        )

    def recognize(self, image):
        """
        识别车牌号码
        :param image: 车牌图像（numpy数组）
        :return: (车牌号, 置信度) 或 (None, None)
        """
        result = self.ocr.ocr(image, cls=True)[0]
        if result:
            license_name, conf = result[0][1]
            # 去除特殊字符
            if '·' in license_name:
                license_name = license_name.replace('·', '')
            return license_name, conf
        return None, None

    def recognize_batch(self, images):
        """
        批量识别车牌
        :param images: 车牌图像列表
        :return: [(车牌号, 置信度), ...]
        """
        results = []
        for img in images:
            license_num, conf = self.recognize(img)
            if license_num:
                results.append((license_num, conf))
            else:
                results.append(('无法识别', 0))
        return results
