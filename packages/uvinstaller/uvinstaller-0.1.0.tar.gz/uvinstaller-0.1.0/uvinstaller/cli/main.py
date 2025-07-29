"""命令行接口主入口"""

import argparse
import sys
from pathlib import Path
from ..core.installer import UVInstaller


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="uvi",
        description="基于UV和PyInstaller的Python项目自动打包工具"
    )
    
    # 主要位置参数：入口文件
    parser.add_argument(
        "entry_point",
        help="Python入口文件路径"
    )
    
    return parser


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 检查入口文件是否存在
    entry_path = Path(args.entry_point)
    if not entry_path.exists():
        print(f"错误：入口文件不存在: {args.entry_point}", file=sys.stderr)
        sys.exit(1)
    
    # 创建UVInstaller实例并执行打包
    installer = UVInstaller()
    installer.pack(args.entry_point)


if __name__ == "__main__":
    main() 