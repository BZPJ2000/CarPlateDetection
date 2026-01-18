# coding:utf-8
"""
图片车牌检测脚本
对单张图片进行车牌检测和识别
"""
import sys
import os
import cv2
import argparse
import time
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import PlatePipeline
from src.utils.visualization import img_cvread
from src.config import settings


def print_header():
    """打印程序头部信息"""
    print("=" * 60)
    print("           车牌检测与识别系统 - 图片检测模式")
    print("=" * 60)
    print()


def print_result(boxes, license_list, conf_list, elapsed_time):
    """格式化打印检测结果"""
    print("\n" + "-" * 60)
    print("检测结果:")
    print("-" * 60)

    if len(license_list) == 0:
        print("  未检测到车牌")
    else:
        print(f"  检测到 {len(license_list)} 个车牌\n")
        for i, (plate, conf, box) in enumerate(zip(license_list, conf_list, boxes)):
            print(f"  [{i+1}] 车牌号码: {plate}")
            print(f"      置信度: {conf:.2%}")
            print(f"      位置: ({box[0]}, {box[1]}) -> ({box[2]}, {box[3]})")
            print()

    print(f"  处理耗时: {elapsed_time:.3f} 秒")
    print("-" * 60)


def save_result(image, output_path):
    """保存检测结果"""
    try:
        cv2.imwrite(output_path, image)
        print(f"\n✓ 结果已保存到: {output_path}")
        return True
    except Exception as e:
        print(f"\n✗ 保存失败: {e}")
        return False


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='车牌检测与识别 - 图片模式')
    parser.add_argument('--image', '-i', type=str,
                       help='输入图片路径')
    parser.add_argument('--output', '-o', type=str,
                       help='输出图片路径（可选）')
    parser.add_argument('--no-display', action='store_true',
                       help='不显示结果窗口')
    parser.add_argument('--scale', type=float, default=0.5,
                       help='显示缩放比例（默认0.5）')

    args = parser.parse_args()

    # 打印头部信息
    print_header()

    # 确定图片路径
    if args.image:
        img_path = args.image
    else:
        # 使用默认测试图片
        img_path = os.path.join(
            settings.ROOT_DIR,
            "data", "test_images",
            "013671875-93_102-226&489_426&558-426&558_234&546_226&489_417&494-0_0_5_25_33_24_24_33-86-80.jpg"
        )

    # 检查文件是否存在
    if not os.path.exists(img_path):
        print(f"✗ 错误: 图片文件不存在: {img_path}")
        return

    print(f"输入图片: {img_path}")
    print(f"正在加载模型...")

    try:
        # 创建检测识别流程
        pipeline = PlatePipeline()
        print("✓ 模型加载成功\n")

        # 读取图片
        print("正在处理图片...")
        image = img_cvread(img_path)

        if image is None:
            print("✗ 错误: 无法读取图片")
            return

        # 记录开始时间
        start_time = time.time()

        # 处理图片
        boxes, license_list, conf_list = pipeline.process_image(img_path)

        # 计算耗时
        elapsed_time = time.time() - start_time

        # 打印结果
        print_result(boxes, license_list, conf_list, elapsed_time)

        # 绘制结果
        if boxes:
            image = pipeline.draw_results(image, boxes, license_list)

        # 保存结果
        if args.output:
            save_result(image, args.output)

        # 显示结果
        if not args.no_display:
            display_img = cv2.resize(image, dsize=None, fx=args.scale, fy=args.scale,
                                    interpolation=cv2.INTER_LINEAR)
            cv2.imshow("车牌检测结果 (按任意键退出)", display_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    except Exception as e:
        print(f"\n✗ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
