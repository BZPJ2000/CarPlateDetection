# coding:utf-8
"""
项目配置文件
包含所有路径配置和模型参数
"""
import os

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 模型路径配置
YOLO_MODEL_PATH = os.path.join(ROOT_DIR, 'models', 'yolo', 'best.pt')
PADDLE_CLS_MODEL = os.path.join(ROOT_DIR, 'models', 'paddle', 'cls', 'ch_ppocr_mobile_v2.0_cls_infer')
PADDLE_DET_MODEL = os.path.join(ROOT_DIR, 'models', 'paddle', 'det', 'ch', 'ch_PP-OCRv4_det_infer')
PADDLE_REC_MODEL = os.path.join(ROOT_DIR, 'models', 'paddle', 'rec', 'ch', 'ch_PP-OCRv4_rec_infer')

# 字体路径
FONT_PATH = os.path.join(ROOT_DIR, 'assets', 'fonts', 'platech.ttf')

# 输出路径配置
OUTPUT_DIR = os.path.join(ROOT_DIR, 'outputs')
OUTPUT_IMAGES_DIR = os.path.join(OUTPUT_DIR, 'images')
OUTPUT_VIDEOS_DIR = os.path.join(OUTPUT_DIR, 'videos')

# 测试数据路径
TEST_IMAGES_DIR = os.path.join(ROOT_DIR, 'data', 'test_images')
TEST_VIDEOS_DIR = os.path.join(ROOT_DIR, 'data', 'test_videos')

# 类别配置
NAMES = {0: 'License'}
CH_NAMES = ['车牌']

# 检测参数
CONF_THRESHOLD = 0.25  # 置信度阈值
IOU_THRESHOLD = 0.7    # NMS的IoU阈值

# 兼容旧版本的变量名
save_path = OUTPUT_DIR
model_path = YOLO_MODEL_PATH
names = NAMES