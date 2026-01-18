#!/usr/bin/env python
# coding:utf-8
"""
车牌检测与识别系统 - 主入口
支持图片、视频、摄像头三种检测模式
"""
import sys
import os
import argparse

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           车牌检测与识别系统 v2.0                              ║
║           License Plate Detection & Recognition              ║
║                                                              ║
║           基于 YOLOv8 + PaddleOCR                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(
        description='车牌检测与识别系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  图片检测:    python main.py image -i test.jpg
  视频检测:    python main.py video -v test.mp4
  摄像头检测:  python main.py camera

更多帮助:
  python main.py image --help
  python main.py video --help
  python main.py camera --help
        """
    )

    subparsers = parser.add_subparsers(dest='mode', help='检测模式')

    # 图片检测模式
    image_parser = subparsers.add_parser('image', help='图片检测模式')
    image_parser.add_argument('--image', '-i', type=str, help='输入图片路径')
    image_parser.add_argument('--output', '-o', type=str, help='输出图片路径')
    image_parser.add_argument('--no-display', action='store_true', help='不显示结果')
    image_parser.add_argument('--scale', type=float, default=0.5, help='显示缩放比例')

    # 视频检测模式
    video_parser = subparsers.add_parser('video', help='视频检测模式')
    video_parser.add_argument('--video', '-v', type=str, help='输入视频路径')
    video_parser.add_argument('--output', '-o', type=str, help='输出视频路径')
    video_parser.add_argument('--no-display', action='store_true', help='不显示结果')
    video_parser.add_argument('--scale', type=float, default=0.5, help='显示缩放比例')
    video_parser.add_argument('--skip-frames', type=int, default=1, help='跳帧处理')

    # 摄像头检测模式
    camera_parser = subparsers.add_parser('camera', help='摄像头检测模式')
    camera_parser.add_argument('--camera', '-c', type=int, help='摄像头ID')
    camera_parser.add_argument('--output', '-o', type=str, help='输出视频路径')
    camera_parser.add_argument('--show-fps', action='store_true', help='显示FPS')

    args = parser.parse_args()

    # 打印横幅
    print_banner()

    if not args.mode:
        parser.print_help()
        return

    # 根据模式调用相应的脚本
    if args.mode == 'image':
        from scripts import detect_image
        sys.argv = ['detect_image.py']
        if args.image:
            sys.argv.extend(['--image', args.image])
        if args.output:
            sys.argv.extend(['--output', args.output])
        if args.no_display:
            sys.argv.append('--no-display')
        sys.argv.extend(['--scale', str(args.scale)])
        detect_image.main()

    elif args.mode == 'video':
        from scripts import detect_video
        sys.argv = ['detect_video.py']
        if args.video:
            sys.argv.extend(['--video', args.video])
        if args.output:
            sys.argv.extend(['--output', args.output])
        if args.no_display:
            sys.argv.append('--no-display')
        sys.argv.extend(['--scale', str(args.scale)])
        sys.argv.extend(['--skip-frames', str(args.skip_frames)])
        detect_video.main()

    elif args.mode == 'camera':
        from scripts import detect_camera
        sys.argv = ['detect_camera.py']
        if args.camera is not None:
            sys.argv.extend(['--camera', str(args.camera)])
        if args.output:
            sys.argv.extend(['--output', args.output])
        if args.show_fps:
            sys.argv.append('--show-fps')
        detect_camera.main()


if __name__ == "__main__":
    main()
