# coding:utf-8
"""
车牌检测识别完整流程
整合检测和识别功能
"""
from src.core.detector import PlateDetector
from src.core.recognizer import PlateRecognizer
from src.utils.visualization import drawRectBox, img_cvread
from PIL import ImageFont
from src.config import settings


class PlatePipeline:
    """车牌检测识别流程类"""

    def __init__(self, detector=None, recognizer=None):
        """
        初始化流程
        :param detector: 检测器实例
        :param recognizer: 识别器实例
        """
        self.detector = detector or PlateDetector()
        self.recognizer = recognizer or PlateRecognizer()

    def process_image(self, image):
        """
        处理单张图像
        :param image: 输入图像（numpy数组或路径）
        :return: (检测框列表, 识别结果列表, 置信度列表)
        """
        # 检测车牌位置
        boxes = self.detector.get_plate_boxes(image)

        if not boxes:
            return [], [], []

        # 读取图像（如果是路径）
        if isinstance(image, str):
            image = img_cvread(image)

        # 裁剪车牌区域
        plate_images = self.detector.crop_plates(image, boxes)

        # 识别车牌号码
        results = self.recognizer.recognize_batch(plate_images)

        license_list = [r[0] for r in results]
        conf_list = [r[1] for r in results]

        return boxes, license_list, conf_list

    def draw_results(self, image, boxes, texts, font_path=None, font_size=50):
        """
        在图像上绘制检测和识别结果
        :param image: 原始图像
        :param boxes: 边界框列表
        :param texts: 识别文本列表
        :param font_path: 字体路径
        :param font_size: 字体大小
        :return: 绘制后的图像
        """
        font_path = font_path or settings.FONT_PATH
        fontC = ImageFont.truetype(font_path, font_size, 0)

        for text, box in zip(texts, boxes):
            image = drawRectBox(image, box, text, fontC)

        return image
