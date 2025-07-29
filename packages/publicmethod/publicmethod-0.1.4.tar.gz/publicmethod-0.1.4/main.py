"""
主程序入口，展示如何使用BaseComponent的子类。
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# 将src目录添加到模块搜索路径
sys.path.append(str(Path(__file__).parent / "src"))
from components.base_component import BaseComponent

class TextProcessor(BaseComponent):
    """文本处理组件，继承自BaseComponent，提供文本分析功能。"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化文本处理组件。
        
        Args:
            config: 配置字典，可以包含BaseComponent支持的所有配置项，以及：
                - lowercase: 是否将文本转换为小写，默认为True
                - remove_punctuation: 是否删除标点符号，默认为False
        """
        # 继承父类的初始化方法
        super().__init__(config)
        
        # 使用当前模块名称重新获取logger
        self.logger = logging.getLogger(__name__)
        
        # 特定于TextProcessor的配置
        self.lowercase = self.config.get('lowercase', True)
        self.remove_punctuation = self.config.get('remove_punctuation', False)
        
        self.logger.info("文本处理组件初始化完成")
    
    def process(self, text: Optional[str] = None) -> Dict[str, Any]:
        """
        重写父类的process方法，实现文本处理功能。
        
        Args:
            data: 要处理的文本数据，如果为None，则使用之前读取的数据
            
        Returns:
            包含处理结果的字典
        
        Raises:
            ValueError: 当没有数据可供处理时
        """
        if text is None:
            text = self._data

        
        # 执行文本处理
        self.logger.debug("开始文本处理")
        
        # 转小写
        if self.lowercase:
            self.logger.debug("转换文本为小写")
            text = text.lower()
        
        # 删除标点符号
        if self.remove_punctuation:
            import string
            self.logger.debug("删除文本中的标点符号")
            for punctuation in string.punctuation:
                text = text.replace(punctuation, ' ')
        
        # 分词并计算词频
        words = text.split()
        word_count = len(words)
        unique_words = set(words)
        unique_count = len(unique_words)
        
        # 计算词频（仅计算前10个最常见的词）
        from collections import Counter
        word_freq = Counter(words).most_common(10)
        
        # 准备结果
        result = {
            'word_count': word_count,
            'unique_word_count': unique_count,
            'most_common_words': word_freq,
            'processed_text': text[:200] + ('...' if len(text) > 200 else '')  # 仅保留前200个字符
        }
        
        # 将结果保存为JSON文件
        import json
        result_path = self._path_manager.get_file_path('results', filename='text_analysis.json')

        # 处理文本中可能存在的无效Unicode字符
        def handle_bad_unicode(obj):
            if isinstance(obj, str):
                return obj.encode('utf-8', 'replace').decode('utf-8')
            elif isinstance(obj, dict):
                return {k: handle_bad_unicode(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [handle_bad_unicode(item) for item in obj]
            return obj
        
        # 净化结果中的无效字符
        clean_result = handle_bad_unicode(result)
        
        try:
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(clean_result, f, ensure_ascii=False, indent=2)
        except UnicodeError as e:
            self.logger.warning(f"保存JSON时遇到编码问题: {e}")
            # 尝试使用ensure_ascii=True作为备选方案
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(clean_result, f, ensure_ascii=True, indent=2)
                self.logger.info("已使用ASCII转义序列保存JSON")
        
        self.logger.info(f"文本处理完成，共处理了{word_count}个单词，{unique_count}个唯一单词")
        self._last_result = result  # 保存最后的处理结果
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取文本统计信息，这是TextProcessor特有的方法。
        
        Returns:
            包含文本统计信息的字典
        
        Raises:
            ValueError: 当尚未处理数据时
        """
        if not hasattr(self, '_last_result') or self._last_result is None:
            self.logger.error("尚未处理数据，无法获取统计信息")
            raise ValueError("尚未处理数据，请先调用process方法")
        
        return self._last_result


def main():
    """主函数，展示如何使用TextProcessor组件。"""
    # 创建配置
    config = {
        'debug_mode': False,  # 启用调试模式，会输出详细日志到控制台
        'output_path': 'E:/Download/Output/',
        'lowercase': True,
        'remove_punctuation': True,
    }
    
    # 创建文本处理器
    processor = TextProcessor(config)
    
    
    # 示例2：从不同编码的文件读取处理
    try:
        processor.read_data(r'./sample_text.txt')
        result2 = processor.process()
        print(f"文件中单词总数: {result2['word_count']}")
        print(f"唯一单词数: {result2['unique_word_count']}")
        print(f"处理后文本示例: {result2['processed_text'][:50]}...")
    except Exception as e:
        print(f"处理文件时出错: {e}")
        

    
    print("\n处理完成，详细结果请查看日志文件和输出目录。")



if __name__ == "__main__":
    main()