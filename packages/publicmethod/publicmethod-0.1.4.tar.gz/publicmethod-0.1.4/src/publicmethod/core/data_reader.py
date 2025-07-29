"""
数据读取组件模块，支持从标准输入和本地文件读取数据。
"""
import sys
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, TextIO, List


class DataReader:
    """数据读取组件，支持多种数据源读取。"""

    # 常用编码列表，按尝试顺序排列
    COMMON_ENCODINGS = ['utf-8', 'gbk', 'gb18030', 'gb2312', 'big5', 'cp936', 'latin1']

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化数据读取组件。

        Args:
            config: 可选的配置字典，可以包含以下键：
                - encoding: 文件编码，默认为 'utf-8'
                - chunk_size: 读取块大小，默认为 8192
                - auto_detect_encoding: 是否自动检测编码，默认为True
                - encodings: 自定义的编码尝试列表
        """
        self.config = config or {}
        self.encoding = self.config.get('encoding', 'utf-8')
        self.chunk_size = self.config.get('chunk_size', 8192)
        self.auto_detect_encoding = self.config.get('auto_detect_encoding', True)
        self._source: Optional[TextIO] = None
        
        # 用户可以提供自定义的编码尝试列表
        self.encodings = self.config.get('encodings', self.COMMON_ENCODINGS)
        
        # 获取当前模块的logger
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("数据读取器初始化完成")

    def _read_from_stdin(self) -> str:
        """
        从标准输入读取数据（内部方法）。

        Returns:
            读取到的数据字符串
        """
        self.logger.debug("从标准输入读取数据")
        data = sys.stdin.read()
        # 如果data是文件路径，尝试从文件读取
        if isinstance(data, (str, Path)) and Path(data).is_file():
            self.logger.debug(f"检测到data是文件路径,尝试从文件读取: {data}")
            return self._read_from_file(data)
        self.logger.debug(f"从标准输入读取了 {len(data)} 个字符")
        return data

    def _read_from_file_with_encoding(self, file_path: Path, encoding: str) -> str:
        """
        使用指定编码从文件读取数据。

        Args:
            file_path: 文件路径
            encoding: 尝试的编码

        Returns:
            读取到的数据字符串

        Raises:
            UnicodeDecodeError: 当使用指定编码无法正确解码文件内容时
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = f.read()
                self.logger.info(f"使用编码 {encoding} 成功读取了 {len(data)} 个字符: {file_path}")
                # 记录使用的编码，以便将来使用
                self.encoding = encoding
                return data
        except UnicodeDecodeError:
            self.logger.debug(f"使用编码 {encoding} 读取失败，尝试其他编码")
            raise

    def _read_from_file(self, file_path: Union[str, Path]) -> str:
        """
        从本地文件读取数据（内部方法）。

        Args:
            file_path: 文件路径

        Returns:
            读取到的数据字符串

        Raises:
            FileNotFoundError: 当文件不存在时
            IOError: 当文件读取失败时
        """
        file_path = Path(file_path)
        self.logger.debug(f"尝试读取文件: {file_path}")
        
        if not file_path.exists():
            error_msg = f"文件不存在: {file_path}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # 如果不自动检测编码，则使用指定的编码
        if not self.auto_detect_encoding:
            try:
                return self._read_from_file_with_encoding(file_path, self.encoding)
            except UnicodeDecodeError as e:
                error_msg = f"使用编码 {self.encoding} 读取文件失败: {file_path}"
                self.logger.error(f"{error_msg}, 错误: {str(e)}")
                raise IOError(error_msg) from e
        
        # 自动检测编码
        errors = []
        
        # 首先尝试用户指定的编码
        try:
            return self._read_from_file_with_encoding(file_path, self.encoding)
        except UnicodeDecodeError as e:
            errors.append(f"尝试编码 {self.encoding}: {str(e)}")
            self.logger.debug(f"使用指定编码 {self.encoding} 读取失败，尝试其他编码")
        
        # 然后尝试其他常用编码
        for encoding in self.encodings:
            if encoding == self.encoding:  # 跳过已尝试的编码
                continue
                
            try:
                return self._read_from_file_with_encoding(file_path, encoding)
            except UnicodeDecodeError as e:
                errors.append(f"尝试编码 {encoding}: {str(e)}")
                continue
        
        # 如果所有编码都失败，则尝试使用二进制模式读取并强制转换
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                # 使用errors='replace'参数来替换无法解码的字符
                text = data.decode(self.encoding, errors='replace')
                self.logger.warning(f"所有编码尝试失败，使用二进制模式读取并替换无法解码的字符: {file_path}")
                return text
        except Exception as e:
            error_msg = f"读取文件失败，所有编码尝试均失败: {file_path}"
            self.logger.error(f"{error_msg}, 尝试的编码: {self.encodings}")
            self.logger.error(f"错误详情: {errors}")
            raise IOError(error_msg) from e

    def read(self, source: Optional[Union[str, Path]] = None) -> str:
        """
        读取数据，自动判断数据源。
        当source为None时从标准输入读取，否则从指定文件读取。

        Args:
            source: 数据源，可以是文件路径或None（表示从标准输入读取）

        Returns:
            读取到的数据字符串

        Raises:
            FileNotFoundError: 当指定文件不存在时
            IOError: 当文件读取失败时
        """
        self.logger.debug(f"读取数据，数据源: {source}")
        if source is None:
            return self._read_from_stdin()
        return self._read_from_file(source)

    def read_chunks(self, source: Optional[Union[str, Path]] = None) -> str:
        """
        分块读取数据，适用于大文件。
        当source为None时从标准输入读取，否则从指定文件读取。

        Args:
            source: 数据源，可以是文件路径或None（表示从标准输入读取）

        Returns:
            读取到的数据字符串

        Raises:
            FileNotFoundError: 当指定文件不存在时
            IOError: 当文件读取失败时
        """
        self.logger.debug(f"分块读取数据，数据源: {source}, 块大小: {self.chunk_size}")
        if source is None:
            return self._read_from_stdin()

        # 对于分块读取，我们先确定文件编码，再进行分块读取
        file_path = Path(source)
        if not file_path.exists():
            error_msg = f"文件不存在: {file_path}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # 先读取一小部分来判断编码
        if self.auto_detect_encoding:
            with open(file_path, 'rb') as f:
                sample = f.read(min(1024, self.chunk_size))
                
            # 尝试不同的编码
            detected_encoding = self.encoding
            for encoding in [self.encoding] + [e for e in self.encodings if e != self.encoding]:
                try:
                    sample.decode(encoding)
                    detected_encoding = encoding
                    self.logger.debug(f"检测到文件编码: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
        else:
            detected_encoding = self.encoding

        # 使用检测到的编码读取文件
        try:
            chunks = []
            with open(file_path, 'r', encoding=detected_encoding) as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    
            data = ''.join(chunks)
            self.logger.info(f"使用编码 {detected_encoding} 成功从文件分块读取了 {len(data)} 个字符: {file_path}")
            return data
        except IOError as e:
            error_msg = f"读取文件失败: {file_path}"
            self.logger.error(f"{error_msg}, 错误: {str(e)}")
            raise IOError(error_msg) from e 