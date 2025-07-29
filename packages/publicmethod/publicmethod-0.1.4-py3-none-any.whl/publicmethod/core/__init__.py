"""
通用Python组件库，提供数据读取、路径管理和日志功能
"""

from .base_component import BaseComponent
from .path_manager import PathManager
from .data_reader import DataReader
from .log_config import setup_logging

__version__ = "0.1.0"
__all__ = ['BaseComponent', 'PathManager', 'DataReader', 'setup_logging'] 