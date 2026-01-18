# coding:utf-8
"""
摄像头实时车牌检测脚本
使用摄像头进行实时车牌检测和识别
"""
import sys
import os
import cv2
import argparse
import time
from collections import deque

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import PlatePipeline


def print_header():
    """打印程序头部信息"""
    print("=" * 60)
    print("           车牌检测与识别系统 - 摄像头实时检测")
    print("=" * 60)
    print()


def find_camera(camera_id=None):
    """查找可用的摄像头"""
    if camera_id is not None:
        cap = cv2.VideoCapture(camera_id)
        ret, _ = cap.read()
        if ret:
            print(f'✓ 找到摄像头，ID: {camera_id}')
            return cap
        cap.release()
        print(f'✗ 无法打开摄像头 ID: {camera_id}')
        return None

    # 自动搜索
    print("正在搜索可用摄像头...")
    for cid in range(10):
        cap = cv2.VideoCapture(cid)
        ret, _ = cap.read()
        if ret:
            print(f'✓ 找到摄像头，ID: {cid}')
            return cap
        cap.release()
    return None


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='车牌检测与识别 - 摄像头模式')
    parser.add_argument('--camera', '-c', type=int,
                       help='摄像头ID（默认自动搜索）')
    parser.add_argument('--output', '-o', type=str,
                       help='输出视频路径（可选）')
    parser.add_argument('--show-fps', action='store_true',
                       help='在画面上显示FPS')

    args = parser.parse_args()

    # 打印头部信息
    print_header()
    print("正在加载模型...")

    try:
        # 创建检测识别流程
        pipeline = PlatePipeline()
        print("✓ 模型加载成功\n")

        # 查找摄像头
        cap = find_camera(args.camera)
        if cap is None:
            print("✗ 错误: 未找到可用的摄像头")
            return

        # 获取摄像头信息
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        print(f"摄像头分辨率: {width}x{height}")
        print(f"按 'q' 键退出, 按 's' 键截图\n")

        # 准备输出视频
        out = None
        if args.output:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(args.output, fourcc, 20, (width, height))
            print(f"录制到: {args.output}\n")

        print("开始实时检测...\n")

        frame_count = 0
        detected_count = 0
        start_time = time.time()
        fps_queue = deque(maxlen=30)  # 用于计算平均FPS

        while cap.isOpened():
            loop_start = time.time()
            success, frame = cap.read()

            if not success:
                print("\n✗ 无法读取摄像头画面")
                break

            frame_count += 1

            # 处理帧
            boxes, license_list, conf_list = pipeline.process_image(frame)

            if boxes:
                detected_count += 1
                frame = pipeline.draw_results(frame, boxes, license_list)

            # 计算FPS
            loop_time = time.time() - loop_start
            fps_queue.append(1.0 / loop_time if loop_time > 0 else 0)
            avg_fps = sum(fps_queue) / len(fps_queue)

            # 在画面上显示信息
            info_y = 30
            cv2.putText(frame, f"Frame: {frame_count}", (10, info_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if args.show_fps:
                cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, info_y + 35),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if license_list:
                plates_text = ", ".join(license_list)
                cv2.putText(frame, f"Detected: {plates_text}", (10, info_y + 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 保存到输出视频
            if out:
                out.write(frame)

            # 显示结果
            cv2.imshow("摄像头车牌检测 (q:退出 s:截图)", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("s"):
                # 截图
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshot_{timestamp}.jpg"
                cv2.imwrite(screenshot_path, frame)
                print(f"\n✓ 截图已保存: {screenshot_path}")

        # 清理
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()

        # 打印统计信息
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print("检测结束!")
        print(f"{'='*60}")
        print(f"  总帧数: {frame_count}")
        print(f"  检测到车牌的帧数: {detected_count}")
        print(f"  运行时长: {elapsed:.2f} 秒")
        print(f"  平均FPS: {frame_count/elapsed:.2f}")
        if args.output:
            print(f"  录制已保存到: {args.output}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n✗ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
