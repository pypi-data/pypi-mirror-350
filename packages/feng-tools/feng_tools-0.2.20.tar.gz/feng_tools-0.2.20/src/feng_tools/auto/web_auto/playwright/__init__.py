"""
playwright相关工具
"""
import sys
from feng_tools.print.print_tools import print_install_info
try:
    import playwright
except ImportError:
    print_install_info('playwright', [
        "pip install pytest-playwright -i https://pypi.tuna.tsinghua.edu.cn/simple/ -U"
    ])
    sys.exit(1)