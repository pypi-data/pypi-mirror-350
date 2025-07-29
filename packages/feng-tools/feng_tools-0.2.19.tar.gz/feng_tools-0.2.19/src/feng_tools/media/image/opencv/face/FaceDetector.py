from typing import List, Tuple, Any
try:
    import cv2
    import numpy as np
except ImportError:
    raise ImportError("请先安装OpenCV和numpy库")


class FaceDetector:
    """人脸检测器类: 使用OpenCV的Haar级联分类器实现人脸检测功能。"""

    def __init__(self):
        """初始化人脸检测器

        加载OpenCV预训练的人脸检测模型。
        """
        # 加载OpenCV预训练的人脸检测级联分类器
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        if self.face_cascade.empty():
            raise ValueError("无法加载人脸检测模型")

    def detect_faces(self, image: np.ndarray) -> list[tuple[Any]] | list[Any]:
        """检测图片中的人脸
        Args:
            image: 输入的图片数据，OpenCV格式的numpy数组
        Returns:
            List[Tuple[int, int, int, int]]: 检测到的人脸位置列表
            每个元素为(x, y, w, h)，表示人脸矩形框的左上角坐标(x,y)和宽高(w,h)
        """
        # 转换为灰度图，提高检测速度和准确率
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,  # 图像缩放比例
            minNeighbors=5,   # 最小邻居数
            minSize=(30, 30)  # 最小人脸尺寸
        )

        # 如果没有检测到人脸，返回空列表
        if len(faces) == 0:
            return []

        # 返回检测到的人脸位置列表
        return [tuple(face) for face in faces]

    def draw_faces(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """在图片上绘制检测到的人脸框
        Args:
            image: 原始图片
            faces: 人脸位置列表，由detect_faces方法返回

        Returns:
            np.ndarray: 标注了人脸框的图片
        """
        # 复制原图，避免修改原始数据
        image_with_faces = image.copy()

        # 在图片上绘制每个检测到的人脸
        for (x, y, w, h) in faces:
            cv2.rectangle(
                image_with_faces,
                (x, y),             # 左上角坐标
                (x + w, y + h),     # 右下角坐标
                (0, 255, 0),        # 颜色：绿色
                2                   # 线条粗细
            )
        return image_with_faces