"""
pytest配置文件，设置项目根目录到Python路径
"""
import sys
import os
from pathlib import Path

# 将项目根目录添加到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 打印Python路径信息，方便调试
print(f"Python路径: {sys.path}")
print(f"项目根目录: {project_root}")
print(f"当前工作目录: {os.getcwd()}") 