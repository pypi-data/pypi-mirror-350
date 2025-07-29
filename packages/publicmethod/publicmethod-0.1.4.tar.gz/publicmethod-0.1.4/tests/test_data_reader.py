"""
数据读取组件的测试模块。
"""
import io
import pytest
from publicmethod.core.data_reader import DataReader


def test_data_reader_initialization():
    """测试数据读取组件初始化。"""
    reader = DataReader()
    assert reader.encoding == 'utf-8'
    assert reader.chunk_size == 8192
    assert reader.auto_detect_encoding == True

    config = {
        'encoding': 'gbk', 
        'chunk_size': 4096,
        'auto_detect_encoding': False
    }
    reader = DataReader(config)
    assert reader.encoding == 'gbk'
    assert reader.chunk_size == 4096
    assert reader.auto_detect_encoding == False


def test_read_from_stdin(monkeypatch):
    """测试从标准输入读取数据。"""
    test_input = "测试数据"
    monkeypatch.setattr('sys.stdin', io.StringIO(test_input))
    
    reader = DataReader()
    result = reader.read()  # 不传参数时从标准输入读取
    assert result == test_input


def test_read_from_file(tmp_path):
    """测试从文件读取数据。"""
    # 创建测试文件
    test_file = tmp_path / "test.txt"
    test_content = "测试文件内容"
    test_file.write_text(test_content, encoding='utf-8')

    reader = DataReader()
    result = reader.read(test_file)  # 传入文件路径时从文件读取
    assert result == test_content


def test_read_from_nonexistent_file():
    """测试读取不存在的文件。"""
    reader = DataReader()
    with pytest.raises(FileNotFoundError):
        reader.read("nonexistent.txt")


def test_auto_detect_encoding(tmp_path):
    """测试自动检测文件编码。"""
    # 创建不同编码的测试文件
    utf8_file = tmp_path / "utf8.txt"
    gbk_file = tmp_path / "gbk.txt"
    
    test_content = "中文测试内容"
    utf8_file.write_text(test_content, encoding='utf-8')
    gbk_file.write_text(test_content, encoding='gbk')
    
    # 启用自动编码检测的读取器
    reader = DataReader({'auto_detect_encoding': True})
    
    # 测试UTF-8文件
    result_utf8 = reader.read(utf8_file)
    assert result_utf8 == test_content
    
    # 测试GBK文件
    result_gbk = reader.read(gbk_file)
    assert result_gbk == test_content


def test_disable_auto_detect_encoding(tmp_path):
    """测试禁用自动编码检测。"""
    # 创建GBK编码的测试文件
    gbk_file = tmp_path / "gbk.txt"
    test_content = "中文测试内容"
    gbk_file.write_text(test_content, encoding='gbk')
    
    # 禁用自动编码检测，但指定正确的编码
    reader = DataReader({
        'auto_detect_encoding': False,
        'encoding': 'gbk'
    })
    result = reader.read(gbk_file)
    assert result == test_content
    
    # 禁用自动编码检测，使用错误的编码
    reader = DataReader({
        'auto_detect_encoding': False,
        'encoding': 'utf-8'  # 错误的编码
    })
    
    # 应当抛出异常
    with pytest.raises(IOError):
        reader.read(gbk_file)


def test_read_method(tmp_path):
    """测试通用读取方法。"""
    # 测试从文件读取
    test_file = tmp_path / "test.txt"
    test_content = "测试文件内容"
    test_file.write_text(test_content, encoding='utf-8')

    reader = DataReader()
    result = reader.read(test_file)
    assert result == test_content

    # 测试从标准输入读取
    test_input = "测试标准输入"
    with pytest.MonkeyPatch.context() as m:
        m.setattr('sys.stdin', io.StringIO(test_input))
        result = reader.read()
        assert result == test_input

def test_custom_encodings_list():
    """测试自定义编码列表。"""
    # 创建自定义编码列表的读取器
    custom_encodings = ['latin1', 'utf-16', 'ascii']
    reader = DataReader({
        'encodings': custom_encodings
    })
    
    # 检查编码列表是否正确设置
    assert reader.encodings == custom_encodings 
