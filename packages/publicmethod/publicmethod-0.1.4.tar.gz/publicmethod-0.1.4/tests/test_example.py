"""
基础组件的测试模块。
"""
import io
import pytest
from pathlib import Path
from publicmethod.core.path_manager import PathManager
from publicmethod.core.base_component import BaseComponent


def test_output_path_manager():
    """测试输出路径管理器。"""
    # 测试默认路径
    manager = PathManager()
    assert manager.base_path == Path.cwd() / 'output'
    assert manager.run_path.parent == manager.base_path
    
    # 确认默认目录结构
    categories = manager.list_categories()
    assert 'logs' in categories
    assert 'data' in categories
    assert 'results' in categories

    # 测试自定义路径
    custom_path = Path('custom_output')
    manager = PathManager(custom_path)
    assert manager.base_path == custom_path
    assert manager.run_path.parent == custom_path

    # 测试目录路径获取
    logs_path = manager.get_directory_path('logs')
    data_path = manager.get_directory_path('data')
    results_path = manager.get_directory_path('results')
    assert logs_path.parent == manager.run_path
    assert data_path.parent == manager.run_path
    assert results_path.parent == manager.run_path


def test_base_component_initialization(tmp_path):
    """测试组件初始化。"""
    # 测试默认输出路径
    component = BaseComponent()
    state = component.get_state()
    assert 'output_path' in state
    assert Path(state['output_path']).parent == Path.cwd() / 'output'

    # 测试自定义输出路径
    component = BaseComponent({'output_path': str(tmp_path)})
    state = component.get_state()
    assert Path(state['output_path']).parent == tmp_path


def test_base_component_with_config(tmp_path):
    """测试带配置的组件初始化。"""
    config = {
        'output_path': str(tmp_path),
        'encoding': 'utf-8',
        'chunk_size': 4096,
        'debug_mode': True
    }
    component = BaseComponent(config)
    assert component.config == config
    state = component.get_state()
    assert Path(state['output_path']).parent == tmp_path


def test_base_component_read_data(tmp_path):
    """测试数据读取功能。"""
    # 测试从文件读取
    test_file = tmp_path / "test.txt"
    test_content = "测试文件内容"
    test_file.write_text(test_content, encoding='utf-8')

    component = BaseComponent({'output_path': str(tmp_path)})
    result = component.read_data(test_file)
    assert result == test_content
    assert component.get_state()['data'] == test_content

    # 测试从标准输入读取
    test_input = "测试标准输入"
    with pytest.MonkeyPatch.context() as m:
        m.setattr('sys.stdin', io.StringIO(test_input))
        result = component.read_data()
        assert result == test_input
        assert component.get_state()['data'] == test_input


def test_base_component_debug_mode(tmp_path):
    """测试调试模式。"""
    # 创建组件并启用调试模式
    component = BaseComponent({
        'output_path': str(tmp_path),
        'debug_mode': True
    })
    
    # 测试调试模式切换
    component.set_debug_mode(False)
    assert not component.config['debug_mode']
    
    component.set_debug_mode(True)
    assert component.config['debug_mode']


def test_base_component_error_handling(tmp_path):
    """测试错误处理。"""
    component = BaseComponent({'output_path': str(tmp_path)})
    
    # 测试读取不存在的文件
    with pytest.raises(FileNotFoundError):
        component.read_data(tmp_path / "nonexistent.txt") 