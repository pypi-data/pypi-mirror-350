import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union


class PathManager:
    """输出路径管理器，处理所有输出相关的路径。"""

    # 预定义的路径类别
    DEFAULT_CATEGORIES = ['logs', 'data', 'results']

    def __init__(self, base_path: Optional[Union[str, Path]] = None):
        """
        初始化输出路径管理器。

        Args:
            base_path: 基础输出路径，如果为None则使用默认路径
        """
        # 获取当前模块的logger
        self.logger = logging.getLogger(__name__)

        # 设置基础路径
        if base_path is None:
            # 默认使用当前目录下的output文件夹
            self.base_path = Path.cwd() / 'output'
        else:
            self.base_path = Path(base_path)

        # 创建时间戳文件夹
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.run_path = self.base_path / timestamp

        # 初始化路径映射
        self._path_map: Dict[str, Path] = {}

        # 创建默认目录
        self._create_default_directories()

        # 记录初始化完成
        self.logger.info(f"输出路径管理器初始化完成，基础路径: {self.run_path}")

    def _create_default_directories(self) -> None:
        """创建默认的目录结构。"""
        self.logger.debug("创建默认目录结构...")
        for category in self.DEFAULT_CATEGORIES:
            self._create_path(category)
        self.logger.debug("默认目录结构创建完成")

    def _create_path(self, *path_parts: str) -> Path:
        """
        创建路径并更新路径映射。

        Args:
            *path_parts: 路径部分

        Returns:
            创建的路径对象
        """
        if not path_parts:
            raise ValueError("至少需要提供一个路径部分")

        # 验证所有路径部分
        for part in path_parts:
            if not part or not part.strip():
                raise ValueError("路径部分不能为空")

        # 构建完整路径
        full_path = self.run_path
        path_key = ""

        for part in path_parts:
            full_path = full_path / part
            path_key = f"{path_key}/{part}" if path_key else part
            self._path_map[path_key] = full_path

        # 创建路径
        full_path.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"创建路径: {full_path}")
        return full_path

    def get_directory_path(self, *path_parts: str) -> Path:
        """
        获取目录路径，如果路径不存在则自动创建。

        Args:
            *path_parts: 路径部分，可以是多个层级

        Returns:
            完整的目录路径
        """
        # 构建路径键
        path_key = ""
        for part in path_parts:
            path_key = f"{path_key}/{part}" if path_key else part

        # 检查路径是否已存在
        if path_key in self._path_map:
            return self._path_map[path_key]

        # 路径不存在，创建它
        return self._create_path(*path_parts)

    def get_file_path(self, *path_parts: str, filename: str) -> Path:
        """
        获取文件路径，如果路径不存在则自动创建。

        Args:
            *path_parts: 路径部分，可以是多个层级
            filename: 文件名

        Returns:
            完整的文件路径

        Raises:
            ValueError: 当文件名无效时
        """
        if not filename or not filename.strip():
            error_msg = "文件名不能为空"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # 获取目录路径（如果已存在则直接返回，否则创建）
        dir_path = self.get_directory_path(*path_parts)

        # 返回文件路径
        file_path = dir_path / filename
        self.logger.debug(f"获取文件路径: {file_path}")
        return file_path

    def list_categories(self) -> List[str]:
        """
        列出所有已创建的路径类别。

        Returns:
            路径类别列表
        """
        categories = list(self._path_map.keys())
        self.logger.debug(f"当前路径类别: {categories}")
        return categories

    def get_all_paths(self) -> Dict[str, Path]:
        """
        获取所有路径映射。

        Returns:
            路径映射字典
        """
        return self._path_map.copy()