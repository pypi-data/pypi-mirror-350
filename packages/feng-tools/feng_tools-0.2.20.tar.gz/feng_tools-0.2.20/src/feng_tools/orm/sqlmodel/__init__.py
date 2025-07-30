"""
SQLModel 相关工具类
"""
from feng_tools.base.print import print_tools
try:
    import sqlmodel
except ImportError:
    print_tools.print_install_info("SQLModel", ["pip install sqlmodel"])

from .base_models import *
