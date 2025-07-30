import platform
import sys, os
try:
    import cv2
except ImportError:
    print("OpenCV未安装，请先安装OpenCV:")
    print("1. pip install opencv-python opencv-contrib-python")
    print("2. 或者从源码编译OpenCV")
    sys.exit(1)

from feng_tools.print.print_tools import print_header, print_section

def check_installation():
    """检查OpenCV安装"""
    print("=== OpenCV安装检查 ===")
    print(f"OpenCV版本: {cv2.__version__}")
    print(f"构建信息: {cv2.getBuildInformation()}")

    # 检查关键模块
    modules = ['core', 'dnn', 'videoio', 'highgui']
    for m in modules:
        try:
            getattr(cv2, m)
            print(f"{m}模块: 可用")
        except:
            print(f"{m}模块: 不可用")

    return check_dnn_support()



def check_versions():
    print_section("版本检查")
    print(f"Python版本: {sys.version}")
    print(f"OpenCV版本: {cv2.__version__}")
    print(f"系统平台: {platform.platform()}")

def check_dnn_support():
    print_section("DNN支持检查")
    print("可用后端:")
    for backend in [cv2.dnn.DNN_BACKEND_DEFAULT, cv2.dnn.DNN_BACKEND_OPENCV]:
        print(f"- {backend}: {cv2.dnn.getBackendName(backend)}")

    print("\n可用目标设备:")
    for target in [cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_OPENCL]:
        print(f"- {target}: {'可用' if cv2.dnn.DNN_TARGET_CPU else '不可用'}")
    print("\n OpenCV DNN模块检查 ===")
    try:
        has_dnn = cv2.dnn_registerLayer("dummy") is not None
        print(f"DNN模块可用: {'是' if has_dnn else '否'}")
        return has_dnn
    except:
        print("DNN模块不可用")
        return False

def test_basic_dnn():
    """测试基本的DNN功能"""
    print_header("最简单的OpenCV DNN测试")

    try:
        # 使用OpenCV自带的模型
        model_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        print(f"尝试加载模型: {model_file}")

        if not cv2.data.haarcascades:
            print("错误: OpenCV数据目录未设置")
            return False
        # 尝试加载一个简单的分类器
        classifier = cv2.CascadeClassifier(model_file)
        if classifier.empty():
            print("错误: 无法加载分类器")
            return False

        print("成功加载OpenCV分类器!")
        return True
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False
def test_default_caffe_model():
    """测试默认的Caffe模型加载"""
    print_header("Caffe模型测试")
    try:
        # 使用OpenCV自带的测试模型
        proto = cv2.samples.findFile("dnn/bvlc_googlenet.prototxt")
        model = cv2.samples.findFile("dnn/bvlc_googlenet.caffemodel")

        print(f"测试prototxt路径: {proto}")
        print(f"测试caffemodel路径: {model}")

        if not os.path.exists(proto) or not os.path.exists(model):
            print("OpenCV测试模型不存在，跳过测试")
            return False

        print("尝试加载测试Caffe模型...")
        net = cv2.dnn.readNetFromCaffe(proto, model)
        print("测试Caffe模型加载成功!")
        return True
    except Exception as e:
        print(f"Caffe模型测试失败: {str(e)}")
        return False

def verify_model(prototxt_file_path, caffemodel_file_path):
    """验证模型文件"""
    print("=== 模型文件验证 ===")
    # 1. 检查文件是否存在
    print("\n[1] 检查文件是否存在...")
    missing_files = []
    files = {
        'prototxt': prototxt_file_path,
        'caffemodel': caffemodel_file_path
    }
    for name, path in files.items():
        if os.path.exists(path):
            print(f"找到 {name}: {path}")
        else:
            print(f"未找到 {name}: {path}")
            missing_files.append(name)
        # 检查文件大小
        size = os.path.getsize(path)
        print(f"- 文件大小: {size} 字节")

        # 检查文件权限
        readable = os.access(path, os.R_OK)
        print(f"- 可读权限: {'是' if readable else '否'}")

    if missing_files:
        print(f"\n错误: 缺少以下文件: {', '.join(missing_files)}")
        print("请确保路径正确.")
        return False

    # 2. 尝试加载模型
    print("\n[3] 尝试加载模型...")
    try:
        # 使用OpenCV自带的测试模型
        proto = cv2.samples.findFile(files['prototxt'])
        model = cv2.samples.findFile(files['caffemodel'])
        net = cv2.dnn.readNetFromCaffe(proto, model)
        print("模型加载成功, 成功创建DNN网络!")
        # 设置后端
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        print(f"使用后端: {cv2.dnn.getBackendName(net.getPreferableBackend())}")
        print(f"使用目标设备: {cv2.dnn.getTargetName(net.getPreferableTarget())}")

    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        return False
    # 3. 测试推理功能
    print("\n[3] 测试推理功能...")
    try:
        # 创建测试图像
        try:
            import numpy as np
        except ImportError:
            print("缺少numpy库, 无法创建测试图像.")
            return False
        test_img = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
        print(f"创建测试图像: {test_img.shape}")

        # 预处理
        blob = cv2.dnn.blobFromImage(
            test_img,
            1.0,
            (300, 300),
            (104.0, 177.0, 123.0),  # 均值减法
            swapRB=False,  # BGR格式
            crop=False
        )
        print("图像预处理完成")

        # 运行推理
        net.setInput(blob)
        detections = net.forward()
        print(f"推理成功! 输出形状: {detections.shape}")

        return True
    except Exception as e:
        print(f"推理测试失败: {str(e)}")
        return False

if __name__ == '__main__':
    if check_installation():
        print("\n建议: OpenCV安装正常，DNN模块可用")
    else:
        print("\n建议: 请重新安装完整版OpenCV:")
        print("1. pip uninstall opencv-python")
        print("2. pip install opencv-python opencv-contrib-python")
        print("3. 或者从源码编译OpenCV")
    # 运行诊断
    check_versions()
    check_dnn_support()
    test_default_caffe_model()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'data', 'models')
    verify_model(os.path.join(model_dir, "opencv_face_recognition_model.prototxt"),
                 os.path.join(model_dir, "opencv_face_recognition_model.caffemodel"))

    print_section("诊断完成")
    sys.exit(0)