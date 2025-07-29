"""
日志配置的测试模块。
"""
import logging
from publicmethod.core.log_config import setup_logging


def test_setup_logging_basic():
    """测试基本日志配置。"""
    # 测试默认配置
    config = {}
    logger = setup_logging(config)
    assert logger.level == logging.INFO
    
    # 清理之前的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def test_setup_logging_debug_mode(tmp_path):
    """测试调试模式。"""
    # 非调试模式
    config = {'debug_mode': False}
    logger = setup_logging(config)
    assert logger.level == logging.INFO
    
    # 调试模式
    config = {'debug_mode': True}
    logger = setup_logging(config)
    assert logger.level == logging.DEBUG
    
    # 清理之前的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def test_setup_logging_with_console_output():
    """测试控制台输出配置。"""
    # 启用控制台输出
    config = {'console_output': True}
    logger = setup_logging(config)
    
    # 检查处理器类型
    has_console_handler = any(
        isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        for h in logger.handlers
    )
    assert has_console_handler
    
    # 禁用控制台输出
    config = {'console_output': False}
    logger = setup_logging(config)
    
    # 检查处理器类型
    has_console_handler = any(
        isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        for h in logger.handlers
    )
    assert not has_console_handler
    
    # 清理之前的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def test_setup_logging_with_file_output(tmp_path):
    """测试文件输出配置。"""
    log_dir = tmp_path / "logs"
    
    # 配置文件输出
    config = {
        'log_dir': str(log_dir)
    }
    logger = setup_logging(config)
    
    # 检查日志目录是否创建
    assert log_dir.exists()
    
    # 检查是否有文件处理器
    has_file_handler = any(
        isinstance(h, logging.FileHandler)
        for h in logger.handlers
    )
    assert has_file_handler
    
    # 写入一条日志消息
    test_message = "测试日志消息"
    logger.info(test_message)
    
    # 检查日志文件是否创建
    log_files = list(log_dir.glob('*.log'))
    assert len(log_files) == 1
    
    # 检查日志内容
    log_content = log_files[0].read_text(encoding='utf-8')
    assert test_message in log_content
    
    # 清理之前的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def test_setup_logging_custom_format():
    """测试自定义日志格式。"""
    # 配置自定义格式
    custom_format = '%(levelname)s: %(message)s'
    config = {
        'format': custom_format
    }
    logger = setup_logging(config)
    
    # 检查控制台处理器的格式
    console_handler = next(
        (h for h in logger.handlers if isinstance(h, logging.StreamHandler) 
         and not isinstance(h, logging.FileHandler)),
        None
    )
    
    if console_handler:
        assert console_handler.formatter._fmt == custom_format
    
    # 清理之前的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def test_setup_logging_third_party_loggers():
    """测试第三方库日志级别设置。"""
    # 创建第三方库的日志记录器
    third_party_loggers = []
    for name in ['urllib3', 'matplotlib', 'PIL']:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)  # 先设置为DEBUG级别
        third_party_loggers.append(logger)
    
    # 配置日志
    config = {}
    setup_logging(config)
    
    # 检查第三方库的日志级别是否被设置为WARNING
    for logger in third_party_loggers:
        if logger.handlers:  # 只检查有处理器的日志记录器
            assert logger.level == logging.WARNING
    
    # 清理
    for logger in third_party_loggers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler) 