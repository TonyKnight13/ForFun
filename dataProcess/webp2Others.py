from pathlib import Path
from abc import ABC, abstractmethod
from PIL import Image
import os
from typing import List, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum


class ImageFormat(Enum):
    """支持的图片格式枚举"""
    PNG = "png"
    JPEG = "jpeg"
    TIFF = "tiff"
    BMP = "bmp"
    GIF = "gif"
    
    @classmethod
    def get_lossless_formats(cls):
        """获取无损格式列表"""
        return [cls.PNG, cls.TIFF, cls.BMP]


@dataclass
class ConversionResult:
    """转换结果数据类"""
    source_file: str
    target_file: str
    success: bool
    error_message: Optional[str] = None
    source_size: Optional[int] = None
    target_size: Optional[int] = None
    conversion_time: Optional[float] = None


class ImageConverter(ABC):
    """图片转换器抽象基类"""
    
    def __init__(self, output_format: ImageFormat):
        self.output_format = output_format
        
    @abstractmethod
    def convert(self, source_path: str, target_path: str) -> ConversionResult:
        """转换单个图片"""
        pass
    
    def validate_format(self) -> bool:
        """验证输出格式是否支持"""
        return True


class WebPConverter(ImageConverter):
    """WebP图片转换器"""
    
    def __init__(self, output_format: ImageFormat, 
                 quality: int = 95,
                 preserve_transparency: bool = True):
        """
        初始化WebP转换器
        
        Args:
            output_format: 输出格式
            quality: 输出质量 (1-100)
            preserve_transparency: 是否保留透明度
        """
        super().__init__(output_format)
        self.quality = max(1, min(100, quality))
        self.preserve_transparency = preserve_transparency
        
    def convert(self, source_path: str, target_path: str) -> ConversionResult:
        """
        转换WebP图片
        
        Args:
            source_path: 源文件路径
            target_path: 目标文件路径
            
        Returns:
            ConversionResult: 转换结果
        """
        import time
        
        start_time = time.time()
        source_size = os.path.getsize(source_path) if os.path.exists(source_path) else None
        
        try:
            # 打开WebP图片
            with Image.open(source_path) as img:
                # 转换为RGB模式如果输出格式不支持透明度且原图有透明度
                if not self.preserve_transparency and img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img, mask=img.getchannel('A'))
                    img = background
                elif img.mode == 'P' and self.preserve_transparency:
                    img = img.convert('RGBA')
                
                # 根据格式选择保存参数
                save_params = self._get_save_params()
                
                # 保存图片
                img.save(target_path, format=self.output_format.value.upper(), **save_params)
                
                # 计算转换时间
                conversion_time = time.time() - start_time
                target_size = os.path.getsize(target_path) if os.path.exists(target_path) else None
                
                return ConversionResult(
                    source_file=source_path,
                    target_file=target_path,
                    success=True,
                    source_size=source_size,
                    target_size=target_size,
                    conversion_time=conversion_time
                )
                
        except Exception as e:
            return ConversionResult(
                source_file=source_path,
                target_file=target_path,
                success=False,
                error_message=str(e)
            )
    
    def _get_save_params(self) -> Dict:
        """获取保存参数"""
        params = {}
        
        if self.output_format in [ImageFormat.JPEG, ImageFormat.PNG]:
            params['quality'] = self.quality
            
        if self.output_format == ImageFormat.PNG:
            params['compress_level'] = 0  # 无压缩，最快速度
            
        if self.output_format == ImageFormat.TIFF:
            params['compression'] = 'none'  # 无压缩
            
        return params


class BatchImageConverter:
    """批量图片转换器"""
    
    def __init__(self, converter: ImageConverter):
        """
        初始化批量转换器
        
        Args:
            converter: 图片转换器实例
        """
        self.converter = converter
        
    def convert_directory(self, 
                         source_dir: str, 
                         target_dir: str,
                         recursive: bool = False) -> List[ConversionResult]:
        """
        转换目录中的所有WebP图片
        
        Args:
            source_dir: 源目录
            target_dir: 目标目录
            recursive: 是否递归处理子目录
            
        Returns:
            List[ConversionResult]: 转换结果列表
        """
        results = []
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        # 确保目标目录存在
        target_path.mkdir(parents=True, exist_ok=True)
        
        # 构建搜索模式
        pattern = "**/*.webp" if recursive else "*.webp"
        
        # 遍历WebP文件
        for webp_file in source_path.glob(pattern):
            if webp_file.is_file():
                # 构建目标文件路径
                relative_path = webp_file.relative_to(source_path)
                target_file = target_path / relative_path.with_suffix(f'.{self.converter.output_format.value}')
                
                # 确保目标子目录存在
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 转换文件
                result = self.converter.convert(str(webp_file), str(target_file))
                results.append(result)
                
                # 打印进度
                if result.success:
                    print(f"✓ 转换成功: {webp_file.name} -> {target_file.name}")
                else:
                    print(f"✗ 转换失败: {webp_file.name} - {result.error_message}")
        
        return results
    
    def convert_files(self, 
                     file_list: List[str], 
                     target_dir: str) -> List[ConversionResult]:
        """
        转换指定的文件列表
        
        Args:
            file_list: 文件路径列表
            target_dir: 目标目录
            
        Returns:
            List[ConversionResult]: 转换结果列表
        """
        results = []
        target_path = Path(target_dir)
        
        # 确保目标目录存在
        target_path.mkdir(parents=True, exist_ok=True)
        
        for source_file in file_list:
            source_path = Path(source_file)
            if source_path.is_file() and source_path.suffix.lower() == '.webp':
                # 构建目标文件路径
                target_file = target_path / source_path.with_suffix(f'.{self.converter.output_format.value}').name
                
                # 转换文件
                result = self.converter.convert(str(source_path), str(target_file))
                results.append(result)
                
                # 打印进度
                if result.success:
                    print(f"✓ 转换成功: {source_path.name} -> {target_file.name}")
                else:
                    print(f"✗ 转换失败: {source_path.name} - {result.error_message}")
        
        return results


class ConversionReport:
    """转换报告生成器"""
    
    def __init__(self, results: List[ConversionResult]):
        """
        初始化报告生成器
        
        Args:
            results: 转换结果列表
        """
        self.results = results
    
    def generate_summary(self) -> Dict:
        """生成转换摘要"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful
        
        # 计算总文件大小变化
        total_source_size = sum(r.source_size for r in self.results if r.source_size)
        total_target_size = sum(r.target_size for r in self.results if r.success and r.target_size)
        
        # 计算总转换时间
        total_time = sum(r.conversion_time for r in self.results if r.success and r.conversion_time)
        
        return {
            "total_files": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "total_source_size": total_source_size,
            "total_target_size": total_target_size,
            "size_change_percent": ((total_target_size - total_source_size) / total_source_size * 100 
                                   if total_source_size else 0),
            "total_conversion_time": total_time
        }
    
    def print_report(self):
        """打印转换报告"""
        summary = self.generate_summary()
        
        print("\n" + "="*60)
        print("图片转换报告")
        print("="*60)
        print(f"总文件数: {summary['total_files']}")
        print(f"成功转换: {summary['successful']}")
        print(f"转换失败: {summary['failed']}")
        print(f"成功率: {summary['success_rate']:.1%}")
        
        if summary['total_source_size']:
            print(f"\n文件大小变化:")
            print(f"  源文件总大小: {self._format_size(summary['total_source_size'])}")
            print(f"  目标文件总大小: {self._format_size(summary['total_target_size'])}")
            print(f"  大小变化: {summary['size_change_percent']:+.1f}%")
        
        if summary['total_conversion_time']:
            print(f"\n转换时间: {summary['total_conversion_time']:.2f}秒")
            if summary['successful'] > 0:
                avg_time = summary['total_conversion_time'] / summary['successful']
                print(f"平均每张图片: {avg_time:.2f}秒")
        
        print("="*60)
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


# 使用示例
def main():
    """主函数示例"""
    # 1. 创建PNG转换器（推荐格式）
    png_converter = WebPConverter(
        output_format=ImageFormat.PNG,
        quality=100,  # 最高质量
        preserve_transparency=True
    )
    
    # 2. 创建批量转换器
    batch_converter = BatchImageConverter(png_converter)
    
    # 3. 转换整个目录
    print("开始转换WebP图片...")
    results = batch_converter.convert_directory(
        source_dir="./origin//webp_images",  # 替换为您的WebP图片目录
        target_dir="./processed/converted_images",
        recursive=True  # 递归处理子目录
    )
    
    # 4. 生成报告
    report = ConversionReport(results)
    report.print_report()
    
    # 5. 显示失败文件（如果有）
    failed_files = [r.source_file for r in results if not r.success]
    if failed_files:
        print("\n转换失败的文件:")
        for file in failed_files:
            print(f"  - {file}")


# 高级使用示例：多格式转换
class MultiFormatConverter:
    """多格式图片转换器"""
    
    def __init__(self, source_dir: str, output_base_dir: str):
        """
        初始化多格式转换器
        
        Args:
            source_dir: 源目录
            output_base_dir: 输出基础目录
        """
        self.source_dir = source_dir
        self.output_base_dir = output_base_dir
    
    def convert_to_multiple_formats(self, formats: List[ImageFormat]) -> Dict[ImageFormat, List[ConversionResult]]:
        """
        转换为多种格式
        
        Args:
            formats: 目标格式列表
            
        Returns:
            每种格式的转换结果字典
        """
        all_results = {}
        
        for fmt in formats:
            print(f"\n开始转换为 {fmt.value.upper()} 格式...")
            
            # 创建对应格式的转换器
            converter = WebPConverter(
                output_format=fmt,
                quality=100,
                preserve_transparency=True
            )
            
            # 创建批量转换器
            batch_converter = BatchImageConverter(converter)
            
            # 设置输出目录
            output_dir = Path(self.output_base_dir) / fmt.value
            
            # 执行转换
            results = batch_converter.convert_directory(
                source_dir=self.source_dir,
                target_dir=str(output_dir),
                recursive=True
            )
            
            # 生成报告
            report = ConversionReport(results)
            report.print_report()
            
            all_results[fmt] = results
        
        return all_results


if __name__ == "__main__":
    # 检查依赖
    try:
        from PIL import Image
    except ImportError:
        print("请先安装Pillow库: pip install Pillow")
        exit(1)
    
    # 运行主函数
    main()
    
    # 多格式转换示例（取消注释以使用）
    # print("\n" + "="*60)
    # print("多格式转换示例")
    # print("="*60)
    # multi_converter = MultiFormatConverter(
    #     source_dir="./webp_images",
    #     output_base_dir="./multi_format_output"
    # )
    # 
    # # 转换为PNG和TIFF（推荐的无损格式）
    # results = multi_converter.convert_to_multiple_formats([
    #     ImageFormat.PNG,
    #     ImageFormat.TIFF,
    #     ImageFormat.BMP
    # ])
