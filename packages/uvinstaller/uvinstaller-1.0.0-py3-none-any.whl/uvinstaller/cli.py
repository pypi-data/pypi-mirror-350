"""
命令行接口模块
实现uvi命令的主要逻辑
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .uv_installer import UvInstaller, UvInstallerError
from .dependency_analyzer import DependencyAnalyzer, DependencyAnalyzerError
from .packager import Packager, PackagerError


def print_header():
    """打印程序头部信息"""
    print("=" * 60)
    print("uvinstaller - Python应用自动打包工具")
    print("使用uv和pyinstaller自动打包Python应用为单个二进制文件")
    print("=" * 60)


def print_usage():
    """打印使用说明"""
    print("\n使用方法:")
    print("  uvi <python文件名>")
    print("\n示例:")
    print("  uvi app.py")
    print("  uvi src/main.py")


def validate_python_file(file_path: str) -> Path:
    """验证Python文件路径"""
    path = Path(file_path)
    
    if not path.exists():
        raise ValueError(f"文件不存在: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"不是一个文件: {file_path}")
    
    if path.suffix.lower() != '.py':
        raise ValueError(f"不是Python文件: {file_path}")
    
    return path.resolve()


def main() -> int:
    """主函数"""
    try:
        print_header()
        
        # 解析命令行参数
        parser = argparse.ArgumentParser(
            description="使用uv和pyinstaller自动打包Python应用",
            add_help=False
        )
        parser.add_argument('file', nargs='?', help='要打包的Python文件')
        parser.add_argument('-h', '--help', action='help', help='显示帮助信息')
        parser.add_argument('-v', '--version', action='version', version='uvinstaller 0.1.0')
        
        args = parser.parse_args()
        
        if not args.file:
            print_usage()
            return 1
        
        # 验证输入文件
        try:
            source_file = validate_python_file(args.file)
            print(f"目标文件: {source_file}")
        except ValueError as e:
            print(f"错误: {e}")
            return 1
        
        # 步骤1: 确保uv可用
        print("\n步骤1: 检查uv环境...")
        uv_installer = UvInstaller()
        if not uv_installer.ensure_uv_available():
            print("错误: 无法安装或使用uv")
            return 1
        print("uv环境检查完成")
        
        # 步骤2: 分析依赖
        print("\n步骤2: 分析项目依赖...")
        analyzer = DependencyAnalyzer()
        try:
            dependencies = analyzer.analyze_project(source_file)
            deps_list = analyzer.get_dependencies_list()
            
            if deps_list:
                print(f"发现 {len(deps_list)} 个外部依赖:")
                for dep in deps_list:
                    print(f"  - {dep}")
            else:
                print("未发现外部依赖")
            
        except DependencyAnalyzerError as e:
            print(f"依赖分析失败: {e}")
            return 1
        
        # 步骤3: 执行打包
        print("\n步骤3: 开始打包...")
        packager = Packager(source_file)
        try:
            exe_path = packager.package(deps_list)
            print(f"\n✅ 打包成功!")
            print(f"可执行文件位置: {exe_path}")
            print(f"文件大小: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
            
        except PackagerError as e:
            print(f"打包失败: {e}")
            return 1
        
        print("\n打包完成! 🎉")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        return 1
    except Exception as e:
        print(f"\n意外错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 