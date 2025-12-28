import os
import platform
from utilsConstants import utilsConstants

class osUtils:
    osConstants = utilsConstants()
    def __init__(self) -> None:
        self.process_path = ""

    def find_all_hidden_files(self, recursive=False):
        """
        查找所有隐藏文件（支持递归）

        Args:
            recursive: 是否递归检查子目录
        Returns:
            list: 隐藏文件路径列表
        """
        hidden_files = []
        system = platform.system()

        def check_file(file_path, file_name):
            """检查单个文件是否为隐藏文件"""
            if system == "Windows":
                try:
                    import ctypes
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
                    if attrs != -1 and attrs & (self.osConstants.WIN_FILE_ATTRIBUTE_HIDDEN | self.osConstants.WIN_FILE_ATTRIBUTE_SYSTEM):
                        return True
                except:
                    if file_name.startswith('.') or file_name.startswith('~$'):
                        return True
            else:
                if file_name.startswith('.'):
                    return True
            return False

        def scan_directory(directory):
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)

                    # 检查当前文件/目录
                    if check_file(item_path, item):
                        hidden_files.append(item_path)

                    # 如果是目录且需要递归，继续扫描
                    if recursive and os.path.isdir(item_path):
                        scan_directory(item_path)
            except PermissionError:
                # 跳过没有权限的目录
                pass

        scan_directory(self.process_path)
        return hidden_files