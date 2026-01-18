# coding:utf-8
"""
YOLO模型训练脚本
用于训练车牌检测模型
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ultralytics import YOLO
from src.config import settings


def main():
    # 数据配置文件路径
    data_yaml = os.path.join(settings.ROOT_DIR, 'data', 'datasets', 'PlateData', 'data.yaml')

    # 加载预训练模型
    model = YOLO('yolov8n.pt')

    # 训练参数
    results = model.train(
        data=data_yaml,
        epochs=300,
        batch=4,
        imgsz=640,
        device='cpu',  # 使用CPU训练，如有GPU可改为0
        project=os.path.join(settings.ROOT_DIR, 'outputs', 'runs'),
        name='train'
    )

    print("训练完成！")


if __name__ == "__main__":
    main()
