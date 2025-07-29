import os

from feng_tools.web.download import download_tools


def download(model_dict:dict[str,str], save_model_dir):
    """
    下载模型
    :param model_dict: 模型名称和模型url的字典, 示例：
        {
            'opencv_face_recognition_model.caffemodel':
                'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel',
            'opencv_face_recognition_model.prototxt':
                'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt'
        }
    :param save_model_dir: 保存模型的目录
    """
    os.makedirs(save_model_dir, exist_ok=True)
    # 下载每个模型文件
    for file_name, url in model_dict.items():
        file_path = os.path.join(save_model_dir, file_name)
        if not os.path.exists(file_path):
            try:
                download_tools.download_file(url, file_path)
            except Exception as e:
                print(f"下载 {file_name} 失败: {e}")
                print(f"请手动下载文件并保存到 {file_path}")
        else:
            print(f"{file_name} 已存在，跳过下载")
    print("\n所有模型文件下载完成!")

if __name__ == '__main__':
    download({
        'opencv_face_recognition_model.caffemodel':
            'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel',
        'opencv_face_recognition_model.prototxt':
            'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt'
    }, './data/models/opencv_face_recognition_model')