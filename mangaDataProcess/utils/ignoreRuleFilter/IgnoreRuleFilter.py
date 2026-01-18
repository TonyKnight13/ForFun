import os
import re
from pathlib import Path
from typing import List, Optional, Pattern, Union


class IgnoreRuleFilter:
    """
    忽略规则过滤器类，支持类似.gitignore的语法
    可以独立使用，也可以集成到其他类中
    """
    
    def __init__(self, ignore_file: str = ".mangaignore"):
        """
        初始化过滤器
        
        Args:
            ignore_file: 忽略文件名，默认为.mangaignore
        """
        self.ignore_file = ignore_file
        self._compiled_patterns: List[Pattern] = []
        self._raw_patterns: List[str] = []
        
    def load_rules(self, root_path: Union[str, Path], 
                   additional_patterns: Optional[List[str]] = None) -> None:
        """
        从文件加载忽略规则
        
        Args:
            root_path: 根目录路径
            additional_patterns: 额外的忽略模式
        """
        root = Path(root_path)
        self._raw_patterns = []
        
        # 1. 从忽略文件读取规则
        ignore_file_path = root / self.ignore_file
        if ignore_file_path.exists():
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释
                    if line and not line.startswith('#'):
                        self._raw_patterns.append(line)
        
        # 2. 添加额外规则
        if additional_patterns:
            self._raw_patterns.extend(additional_patterns)
        
        # 3. 编译规则
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """编译所有忽略规则为正则表达式"""
        self._compiled_patterns = []
        
        for pattern in self._raw_patterns:
            try:
                # 将通配符模式转换为正则表达式
                regex_pattern = self._pattern_to_regex(pattern)
                compiled = re.compile(regex_pattern, re.IGNORECASE)
                self._compiled_patterns.append(compiled)
            except re.error as e:
                print(f"警告: 忽略模式 '{pattern}' 编译失败: {e}")
    
    def _pattern_to_regex(self, pattern: str) -> str:
        """
        将通配符模式转换为正则表达式
        
        Args:
            pattern: 通配符模式，如 "*.zip", "E*", "temp/"
            
        Returns:
            正则表达式字符串
        """
        # 处理目录分隔符
        pattern = pattern.replace('/', os.sep)
        
        # 如果是目录模式（以/结尾），需要特殊处理
        if pattern.endswith(os.sep):
            # 目录模式：匹配该目录下的所有内容
            dir_pattern = pattern.rstrip(os.sep)
            # 转义特殊字符
            escaped = re.escape(dir_pattern)
            # 恢复通配符
            escaped = escaped.replace(r'\*', '.*').replace(r'\?', '.')
            return f'^{escaped}{re.escape(os.sep)}.*'
        
        # 处理普通文件模式
        # 转义特殊字符
        escaped = re.escape(pattern)
        # 恢复通配符功能
        escaped = escaped.replace(r'\*', '.*').replace(r'\?', '.')
        
        # 如果模式包含路径分隔符，需要完整匹配
        if os.sep in pattern:
            return f'^{escaped}$'
        else:
            # 只匹配文件名
            return f'{os.sep}{escaped}$'
    
    def should_ignore(self, file_path: Union[str, Path], 
                     relative_to: Optional[Union[str, Path]] = None) -> bool:
        """
        判断文件是否应该被忽略
        
        Args:
            file_path: 文件路径
            relative_to: 相对路径的基准目录
            
        Returns:
            True如果应该忽略，False否则
        """
        file_path = Path(file_path)
        
        # 计算相对路径
        if relative_to:
            rel_path = str(file_path.relative_to(relative_to))
        else:
            rel_path = str(file_path)
        
        # 检查是否匹配任何忽略模式
        for pattern in self._compiled_patterns:
            if pattern.search(rel_path):
                return True
        
        return False
    
    def filter_files(self, file_list: List[Union[str, Path]], 
                    root_path: Optional[Union[str, Path]] = None) -> List[Path]:
        """
        过滤文件列表
        
        Args:
            file_list: 文件路径列表
            root_path: 根目录路径，用于计算相对路径
            
        Returns:
            过滤后的文件路径列表
        """
        filtered = []
        
        for file_path in file_list:
            file_path = Path(file_path)
            
            if not self.should_ignore(file_path, root_path):
                filtered.append(file_path)
        
        return filtered
    
    def add_rule(self, pattern: str) -> None:
        """
        添加单个忽略规则
        
        Args:
            pattern: 忽略模式
        """
        self._raw_patterns.append(pattern)
        self._compile_patterns()
    
    def clear_rules(self) -> None:
        """清除所有忽略规则"""
        self._raw_patterns.clear()
        self._compiled_patterns.clear()
    
    def get_rules(self) -> List[str]:
        """获取当前所有忽略规则"""
        return self._raw_patterns.copy()