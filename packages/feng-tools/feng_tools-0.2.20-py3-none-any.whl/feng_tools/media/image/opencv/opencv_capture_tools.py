"""
OpenCV的摄像头工具
"""
import sys
try:
    import cv2
except ImportError:
    print("OpenCV未安装，请先安装OpenCV:")
    print("1. pip install opencv-python opencv-contrib-python")
    print("2. 或者从源码编译OpenCV")
    sys.exit(1)
def test_opencv():
    """测试OpenCV基本功能"""
    print("测试OpenCV基本功能...")

    # 测试OpenCV版本
    print(f"OpenCV版本: {cv2.__version__}")
    # 测试是否能打开摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("警告: 无法打开摄像头")
    else:
        print("摄像头测试通过")
        cap.release()
    # 测试是否能创建窗口
    try:
        cv2.namedWindow('Test Window', cv2.WINDOW_NORMAL)
        cv2.destroyWindow('Test Window')
        print("窗口创建测试通过")
    except Exception as e:
        print(f"窗口创建测试失败: {e}")

    print("OpenCV基本测试完成")

if __name__ == '__main__':
    test_opencv()