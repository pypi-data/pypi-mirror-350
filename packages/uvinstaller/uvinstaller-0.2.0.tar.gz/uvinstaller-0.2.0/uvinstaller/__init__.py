"""uvinstaller - 基于UV和PyInstaller的Python项目自动打包工具"""

__version__ = "0.1.1"
__author__ = "uvinstaller"

from .core.installer import UVInstaller

__all__ = ["UVInstaller"] 