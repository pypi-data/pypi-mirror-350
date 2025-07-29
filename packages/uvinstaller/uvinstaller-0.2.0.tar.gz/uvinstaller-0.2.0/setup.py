"""uvinstaller包安装配置"""

from setuptools import setup, find_packages
import os

# 读取README文件作为长描述
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="uvinstaller",
    version="0.2.0",
    author="uvinstaller",
    description="基于UV和PyInstaller的Python项目自动打包工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # UV会在运行时自动安装，无需在此处声明依赖
        # pyinstaller也会通过UV自动安装
    ],
    entry_points={
        "console_scripts": [
            "uvi=uvinstaller.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 