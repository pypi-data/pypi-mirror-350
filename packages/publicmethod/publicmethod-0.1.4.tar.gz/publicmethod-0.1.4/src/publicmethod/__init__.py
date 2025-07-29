"""
publicmethod - 通用Python组件库
=============================================

提供继承了日志管理、路径管理和数据读取功能的基础类框架。
帮助开发者快速构建基于组件的应用程序。
"""

from .core.base_component import BaseComponent
from .core.path_manager import PathManager
from .core.data_reader import DataReader
from .core.log_config import setup_logging

# 直接从_version.py导入版本（由setuptools_scm自动生成）
from ._version import __version__

# 方便用户直接导入常用类
__all__ = [
    'BaseComponent',   # 基础组件类
    'PathManager',     # 路径管理类
    'DataReader',      # 数据读取类
    'setup_logging'    # 日志设置函数
]
