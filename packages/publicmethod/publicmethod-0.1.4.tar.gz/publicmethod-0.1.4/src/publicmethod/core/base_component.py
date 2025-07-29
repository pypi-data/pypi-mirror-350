"""
通用基础组件模块，提供可重用组件的基类实现。

此模块定义了BaseComponent类，作为所有组件的基类，提供以下功能：
- 配置管理
- 数据读取
- 输出路径管理 
- 日志系统集成
- 状态管理
"""
import logging
from typing import Any, Dict, Optional, Union
from pathlib import Path
from .data_reader import DataReader
from .path_manager import PathManager
from .log_config import setup_logging


class BaseComponent:
    """通用基础组件类，提供数据读取、路径管理和日志功能，可作为其他组件的基类。"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化组件。

        Args:
            config: 可选的配置字典，可以包含以下键：
                - output_path: 输出路径，默认为None（使用默认路径）
                - encoding: 文件编码，默认为 'utf-8'
                - chunk_size: 读取块大小，默认为 8192
                - debug_mode: 是否为调试模式，默认为 False
        """
        self.config = config or {}
        
        # 获取当前模块的logger
        self.logger = logging.getLogger(__name__)
        
        self._initialize()

    def _initialize(self) -> None:
        """初始化内部状态。"""
        self._state = {}
        self._data = None
        
        # 初始化输出路径管理器
        self._path_manager = PathManager(
            self.config.get('output_path')
        )
        
        # 使用输出路径管理器创建的日志目录配置全局日志
        log_dir = str(self._path_manager.get_directory_path('logs'))
        logger_config = {
            'debug_mode': self.config.get('debug_mode', False),
            'log_dir': log_dir,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
        setup_logging(logger_config)
        
        # 初始化数据读取器
        self._data_reader = DataReader(self.config)
        
        self.logger.info(f"组件初始化完成，输出路径: {self._path_manager.run_path}")

    def read_data(self, source: Optional[Union[str, Path]] = None) -> str:
        """
        读取数据。

        Args:
            source: 数据源，可以是文件路径或None（表示从标准输入读取）

        Returns:
            读取到的数据字符串
        """
        try:
            self.logger.debug(f"开始读取数据，数据源: {source}")
            self._data = self._data_reader.read(source)
            self.logger.info(f"数据读取成功，数据长度: {len(self._data)}")
            return self._data
        except Exception as e:
            self.logger.error(f"数据读取失败: {str(e)}")
            raise

    def process(self, data: Optional[str] = None) -> Any:
        pass
        


    def get_state(self) -> Dict[str, Any]:
        """
        获取组件当前状态。

        Returns:
            包含组件状态的字典
        """
        return {
            'config': self.config,
            'data': self._data,
            'state': self._state.copy(),
            'output_path': str(self._path_manager.run_path),
            'categories': self._path_manager.list_categories()
        }

    def set_debug_mode(self, debug_mode: bool) -> None:
        """
        设置调试模式。

        Args:
            debug_mode: 是否为调试模式
        """
        self.config['debug_mode'] = debug_mode
        logger_config = {
            'debug_mode': debug_mode
        }
        setup_logging(logger_config)
        self.logger.info(f"调试模式已{'启用' if debug_mode else '禁用'}")