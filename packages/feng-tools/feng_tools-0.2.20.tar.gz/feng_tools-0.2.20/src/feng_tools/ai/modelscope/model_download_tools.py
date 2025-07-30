"""
- 安装ModelScope
    pip install modelscope -i https://pypi.tuna.tsinghua.edu.cn/simple/
模型下载工具
"""
#SDK模型下载
from modelscope import snapshot_download

def download(model_id:str, local_dir:str=None, cache_dir:str=None):
    """下载模型
    :param model_id: 模型id
    :param local_dir:本地路径
    :param cache_dir: 缓存路径，
    """
    model_dir = snapshot_download(model_id, local_dir=local_dir, cache_dir=cache_dir)
    return model_dir

if __name__ == '__main__':
    # 下载魔搭社区上的NLLB-200模型
    download('Kleaner/v4_facebook-nllb-200-distilled-600M')