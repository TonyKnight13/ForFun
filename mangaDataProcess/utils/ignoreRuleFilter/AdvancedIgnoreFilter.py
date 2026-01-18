import re
from pathlib import Path
from typing import Union

from mangaDataProcess.utils import IgnoreRuleFilter

class AdvancedIgnoreFilter(IgnoreRuleFilter):
    """
    增强版忽略过滤器，支持更完整的.gitignore语法
    """
    
    def _pattern_to_regex(self, pattern: str) -> str:
        """
        增强版模式转换，支持更多.gitignore特性
        
        支持的语法:
        - *: 匹配任意字符序列
        - ?: 匹配单个字符
        - [abc]: 匹配a、b或c
        - [!abc]: 匹配非a、b、c的字符
        - **/: 匹配任意层级的目录
        - !: 例外规则（需要在外部处理）
        """
        # 处理例外规则（以!开头）
        if pattern.startswith('!'):
            pattern = pattern[1:]
            # 注意：例外规则需要在过滤逻辑中特殊处理
        
        # 标准化路径分隔符
        pattern = pattern.replace('\\', '/')
        
        # 处理**模式
        if '**' in pattern:
            # 将**转换为.*
            pattern = pattern.replace('**', '.*')
        
        # 处理目录模式
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/')
            is_dir = True
        else:
            is_dir = False
        
        # 将通配符模式转换为正则表达式
        regex_parts = []
        i = 0
        while i < len(pattern):
            char = pattern[i]
            
            if char == '*':
                if i + 1 < len(pattern) and pattern[i + 1] == '*':
                    # 已经处理过**的情况
                    regex_parts.append('.*')
                    i += 2
                else:
                    regex_parts.append('[^/]*')
                    i += 1
            elif char == '?':
                regex_parts.append('[^/]')
                i += 1
            elif char == '[':
                # 处理字符类
                j = i + 1
                while j < len(pattern) and pattern[j] != ']':
                    j += 1
                if j < len(pattern):
                    char_class = pattern[i:j+1]
                    # 转换字符类语法
                    if char_class.startswith('[!') or char_class.startswith('[^'):
                        char_class = '[^' + char_class[2:-1] + ']'
                    regex_parts.append(char_class)
                    i = j + 1
                else:
                    regex_parts.append(re.escape(char))
                    i += 1
            else:
                regex_parts.append(re.escape(char))
                i += 1
        
        regex = ''.join(regex_parts)
        
        # 添加边界
        if pattern.startswith('/'):
            # 从根目录开始匹配
            regex = '^' + regex
        elif '/' in pattern:
            # 包含路径分隔符，需要完整匹配
            regex = '^' + regex
        else:
            # 只匹配文件名
            regex = '(^|/)' + regex
        
        if is_dir:
            regex += '(/.*)?$'
        else:
            regex += '$'
        
        return regex
    
    def load_rules_with_exceptions(self, root_path: Union[str, Path]) -> tuple:
        """
        加载规则并分离例外规则
        
        Returns:
            (ignore_patterns, exception_patterns)
        """
        root = Path(root_path)
        ignore_patterns = []
        exception_patterns = []
        
        ignore_file_path = root / self.ignore_file
        if ignore_file_path.exists():
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if line.startswith('!'):
                            exception_patterns.append(line[1:])
                        else:
                            ignore_patterns.append(line)
        
        return ignore_patterns, exception_patterns