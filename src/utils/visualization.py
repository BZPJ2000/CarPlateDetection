# encoding:utf-8
"""
可视化工具模块
提供图像绘制、显示和处理的工具函数
"""
import cv2
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from src.config import settings


def cv_show(name, img):
    """
    显示图像并等待按键
    :param name: 窗口名称
    :param img: 图像数组
    """
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def drawRectBox(image, rect, addText, fontC, color=(0, 0, 255)):
    """
    绘制矩形框与文字标签
    :param image: 原始图像
    :param rect: 矩形框坐标 [x1, y1, x2, y2]
    :param addText: 要显示的文字
    :param fontC: 字体对象
    :param color: 边框颜色 (B, G, R)
    :return: 绘制后的图像
    """
    # 绘制矩形框
    cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), color, 2)

    # 使用PIL绘制中文文字
    font_size = int((rect[3] - rect[1]) / 1.5)
    font_size = max(20, min(font_size, 100))  # 限制字体大小范围

    try:
        fontC = ImageFont.truetype(settings.FONT_PATH, font_size, 0)
    except:
        # 如果字体加载失败，使用默认字体
        fontC = ImageFont.load_default()

    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)

    # 绘制文字背景
    text_bbox = draw.textbbox((0, 0), addText, font=fontC)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    bg_x1 = rect[0]
    bg_y1 = rect[1] - text_height - 10
    bg_x2 = rect[0] + text_width + 10
    bg_y2 = rect[1]

    draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(0, 0, 255))

    # 绘制文字
    draw.text((rect[0] + 5, rect[1] - text_height - 5), addText, (255, 255, 255), font=fontC)

    return np.array(img)


def img_cvread(path):
    # 读取含中文名的图片文件
    # img = cv2.imread(path)
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img


def draw_boxes(img, boxes):
    for each in boxes:
        x1 = each[0]
        y1 = each[1]
        x2 = each[2]
        y2 = each[3]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img



def cvimg_to_qpiximg(cvimg):
    height, width, depth = cvimg.shape
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    qimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
    qpix_img = QPixmap(qimg)
    return qpix_img




# 封装函数:图片上显示中文
def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=50):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)



