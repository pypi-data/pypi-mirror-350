"""UVInstaller核心类实现"""

import subprocess
import shutil
import os
from pathlib import Path


class UVInstaller:
    """基于UV和PyInstaller的Python项目自动打包工具"""
    
    def __init__(self):
        """初始化UVInstaller"""
        self.output_dir = "dist"
        
    def pack(self, entry_point):
        """打包Python项目为单个可执行文件
        
        Args:
            entry_point: 入口文件路径
        """
        print(f"开始打包项目: {entry_point}")
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 检测依赖
        self._detect_dependencies()
        
        # 创建UV虚拟环境
        self._create_uv_env()
        
        # 安装依赖
        self._install_dependencies()
        
        # 执行PyInstaller打包
        self._run_pyinstaller(entry_point)
        
        # 移动exe文件到源文件目录
        self._move_exe_to_source_dir(entry_point)
        
        # 清理临时文件
        self._cleanup()
            
        print("打包完成，可执行文件已生成在源文件目录中")
    
    def _detect_dependencies(self):
        """检测项目依赖"""
        print("检测项目依赖...")
        # 检查requirements.txt文件
        
    def _create_uv_env(self):
        """创建UV虚拟环境"""
        print("创建UV虚拟环境...")
        subprocess.run(["uv", "venv", ".venv"], check=True)
        
    def _install_dependencies(self):
        """安装依赖"""
        print("安装项目依赖...")
        if os.path.exists("requirements.txt"):
            subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], check=True)
        
    def _run_pyinstaller(self, entry_point):
        """执行PyInstaller打包为单个文件"""
        print("执行PyInstaller打包...")
        cmd = ["uv", "run", "pyinstaller", entry_point, "--distpath", self.output_dir, "--onefile"]
        subprocess.run(cmd, check=True)
    
    def _move_exe_to_source_dir(self, entry_point):
        """将exe文件移动到源文件同目录"""
        print("移动可执行文件到源文件目录...")
        
        # 获取源文件路径信息
        entry_path = Path(entry_point)
        source_dir = entry_path.parent
        exe_name = entry_path.stem + ".exe"
        
        # 构建exe文件路径
        exe_source_path = Path(self.output_dir) / exe_name
        exe_target_path = source_dir / exe_name
        
        # 移动文件
        if exe_source_path.exists():
            shutil.move(str(exe_source_path), str(exe_target_path))
            print(f"可执行文件已移动到: {exe_target_path}")
        else:
            print(f"警告：未找到可执行文件: {exe_source_path}")
        
    def _cleanup(self):
        """清理临时文件"""
        print("清理临时文件...")
        cleanup_dirs = ["build", ".venv", self.output_dir]
        cleanup_files = ["*.spec"]
        
        # 清理目录
        for dir_name in cleanup_dirs:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"已删除目录: {dir_name}")
        
        # 清理文件        
        import glob
        for pattern in cleanup_files:
            for file_path in glob.glob(pattern):
                os.remove(file_path)
                print(f"已删除文件: {file_path}") 