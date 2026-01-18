# coding:utf-8
"""
视频车牌检测脚本
对视频文件进行车牌检测和识别
"""
import sys
import os
import cv2
import argparse
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import PlatePipeline
from src.config import settings


def print_header():
    """打印程序头部信息"""
    print("=" * 60)
    print("           车牌检测与识别系统 - 视频检测模式")
    print("=" * 60)
    print()


def print_progress(frame_count, detected_count, fps, current_plates):
    """打印处理进度"""
    print(f"\r帧数: {frame_count} | 检测到车牌: {detected_count} | FPS: {fps:.1f} | 当前: {current_plates}", end='', flush=True)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='车牌检测与识别 - 视频模式')
    parser.add_argument('--video', '-v', type=str,
                       help='输入视频路径')
    parser.add_argument('--output', '-o', type=str,
                       help='输出视频路径（可选）')
    parser.add_argument('--no-display', action='store_true',
                       help='不显示结果窗口')
    parser.add_argument('--scale', type=float, default=0.5,
                       help='显示缩放比例（默认0.5）')
    parser.add_argument('--skip-frames', type=int, default=1,
                       help='跳帧处理（默认1，即每帧都处理）')

    args = parser.parse_args()

    # 打印头部信息
    print_header()

    # 确定视频路径
    if args.video:
        video_path = args.video
    else:
        video_path = os.path.join(settings.ROOT_DIR, "data", "test_images", "1.mp4")

    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"✗ 错误: 视频文件不存在: {video_path}")
        return

    print(f"输入视频: {video_path}")
    print(f"正在加载模型...")

    try:
        # 创建检测识别流程
        pipeline = PlatePipeline()
        print("✓ 模型加载成功\n")

        # 打开视频
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("✗ 错误: 无法打开视频文件")
            return

        # 获取视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"视频信息: {width}x{height} @ {fps}FPS, 共 {total_frames} 帧")
        print(f"按 'q' 键退出, 按 'p' 键暂停/继续\n")

        # 准备输出视频
        out = None
        if args.output:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

        frame_count = 0
        detected_count = 0
        start_time = time.time()
        paused = False

        print("开始处理...")

        while cap.isOpened():
            if not paused:
                success, frame = cap.read()
                if not success:
                    break

                frame_count += 1

                # 跳帧处理
                if frame_count % args.skip_frames != 0:
                    continue

                # 处理帧
                boxes, license_list, conf_list = pipeline.process_image(frame)

                if boxes:
                    detected_count += 1
                    frame = pipeline.draw_results(frame, boxes, license_list)

                # 计算FPS
                elapsed = time.time() - start_time
                current_fps = frame_count / elapsed if elapsed > 0 else 0

                # 打印进度
                current_plates = ', '.join(license_list) if license_list else '无'
                print_progress(frame_count, detected_count, current_fps, current_plates)

                # 保存到输出视频
                if out:
                    out.write(frame)

            # 显示结果
            if not args.no_display:
                display_frame = cv2.resize(frame, dsize=None, fx=args.scale, fy=args.scale,
                                          interpolation=cv2.INTER_LINEAR)

                # 添加状态文本
                status = "暂停" if paused else "播放中"
                cv2.putText(display_frame, status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("视频车牌检测 (q:退出 p:暂停)", display_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("p"):
                    paused = not paused

        # 清理
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()

        # 打印统计信息
        elapsed = time.time() - start_time
        print(f"\n\n{'='*60}")
        print("处理完成!")
        print(f"{'='*60}")
        print(f"  总帧数: {frame_count}")
        print(f"  检测到车牌的帧数: {detected_count}")
        print(f"  总耗时: {elapsed:.2f} 秒")
        print(f"  平均FPS: {frame_count/elapsed:.2f}")
        if args.output:
            print(f"  输出已保存到: {args.output}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n✗ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
