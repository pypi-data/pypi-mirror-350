"""
日志配置模块，使用Python标准logging模块。
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """
    配置日志系统。
    
    Args:
        config: 配置字典，可包含以下键：
            - log_dir: 日志文件目录
            - debug_mode: 是否为调试模式
            - format: 日志格式
            - max_bytes: 单个日志文件最大大小，默认为10MB
            - backup_count: 保留的日志文件数量，默认为5
            - log_file_prefix: 日志文件名前缀，默认为'app'
            - console_output: 是否输出到控制台，默认与debug_mode相同
            
    Returns:
        logging.Logger: 配置好的根日志记录器
    """
    # 获取配置参数
    log_dir = config.get('log_dir')
    debug_mode = config.get('debug_mode', False)
    max_bytes = config.get('max_bytes', 10 * 1024 * 1024)  # 默认10MB
    backup_count = config.get('backup_count', 5)
    log_file_prefix = config.get('log_file_prefix', 'app')
    # 控制台输出默认与debug_mode相同
    console_output = config.get('console_output', debug_mode)
    
    # 日志级别
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 移除所有现有处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 控制台日志格式
    console_format = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter(console_format)
    
    # 文件日志格式（更详细，包含文件路径和行号）
    file_format = config.get('file_format', 
                             '%(asctime)s - %(name)s - %(levelname)s - [%(pathname)s:%(lineno)d] - %(message)s')
    file_formatter = logging.Formatter(file_format)
    
    # 添加控制台处理器
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(log_level)
        root_logger.addHandler(console_handler)
    
    # 如果指定了日志目录，添加文件处理器
    if log_dir:
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建日志文件名（使用时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir_path / f"{log_file_prefix}_{timestamp}.log"
        
        # 使用RotatingFileHandler进行日志轮转
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
        
        # 记录日志系统初始化信息
        root_logger.info(f"日志系统已初始化，日志文件: {log_file}")
    
    # 设置第三方库的日志级别为WARNING，减少噪音
    for logger_name in ['urllib3', 'matplotlib', 'PIL']:
        if logging.getLogger(logger_name).handlers:
            logging.getLogger(logger_name).setLevel(logging.WARNING)
    
    # 设置未捕获异常处理器
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # 键盘中断交由系统处理
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        # 记录未捕获的异常
        root_logger.critical("未捕获的异常:", exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = handle_exception
    
    return root_logger