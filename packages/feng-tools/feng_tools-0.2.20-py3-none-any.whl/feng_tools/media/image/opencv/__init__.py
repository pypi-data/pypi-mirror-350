"""
Opencv相关工具
"""
import sys
from feng_tools.print.print_tools import print_install_info
try:
    import cv2
except ImportError:
    print_install_info('OpenCV', [
        "1. pip install opencv-python opencv-contrib-python",
        "2. 或者从源码编译OpenCV"
    ])
    sys.exit(1)