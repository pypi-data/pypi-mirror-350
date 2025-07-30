"""
打包器模块
负责使用uv创建虚拟环境、安装依赖并使用pyinstaller打包
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional
import time


class PackagerError(Exception):
    """打包器异常"""
    pass


class Packager:
    """Python应用打包器"""
    
    def __init__(self, source_file: Path):
        self.source_file = source_file.resolve()
        self.source_dir = self.source_file.parent
        self.app_name = self.source_file.stem
        self.temp_dir: Optional[Path] = None
        self.venv_path: Optional[Path] = None
        
    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, timeout: int = 300) -> subprocess.CompletedProcess:
        """运行命令并处理异常"""
        try:
            print(f"执行命令: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
            return result
        except subprocess.TimeoutExpired as e:
            raise PackagerError(f"命令超时: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            error_msg = f"命令执行失败: {' '.join(cmd)}\n"
            if e.stdout:
                error_msg += f"标准输出: {e.stdout}\n"
            if e.stderr:
                error_msg += f"错误输出: {e.stderr}\n"
            raise PackagerError(error_msg)
        except FileNotFoundError:
            raise PackagerError(f"命令未找到: {cmd[0]}")
    
    def create_temp_environment(self) -> Path:
        """创建临时工作目录"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="uvinstaller_"))
        print(f"创建临时目录: {self.temp_dir}")
        return self.temp_dir
    
    def create_virtual_environment(self) -> Path:
        """使用uv创建虚拟环境"""
        if not self.temp_dir:
            raise PackagerError("临时目录未创建")
        
        self.venv_path = self.temp_dir / "venv"
        
        print("创建虚拟环境...")
        self.run_command(["uv", "venv", str(self.venv_path)])
        
        return self.venv_path
    
    def get_venv_python(self) -> str:
        """获取虚拟环境中的Python可执行文件路径"""
        if not self.venv_path:
            raise PackagerError("虚拟环境未创建")
        
        if os.name == 'nt':  # Windows
            return str(self.venv_path / "Scripts" / "python.exe")
        else:  # Unix-like
            return str(self.venv_path / "bin" / "python")
    
    def get_venv_pip(self) -> str:
        """获取虚拟环境中的pip可执行文件路径"""
        if not self.venv_path:
            raise PackagerError("虚拟环境未创建")
        
        if os.name == 'nt':  # Windows
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:  # Unix-like
            return str(self.venv_path / "bin" / "pip")
    
    def install_dependencies(self, dependencies: List[str]) -> None:
        """在虚拟环境中安装依赖"""
        if not dependencies:
            print("没有外部依赖需要安装")
            return
        
        print(f"安装依赖: {', '.join(dependencies)}")
        
        # 首先安装pyinstaller
        print("安装 pyinstaller...")
        self.run_command([
            "uv", "pip", "install", 
            "--python", self.get_venv_python(),
            "pyinstaller"
        ])
        
        # 逐个安装依赖，提高成功率
        for dep in dependencies:
            try:
                print(f"安装依赖: {dep}")
                self.run_command([
                    "uv", "pip", "install",
                    "--python", self.get_venv_python(),
                    dep
                ], timeout=120)
            except PackagerError as e:
                print(f"警告: 安装依赖 {dep} 失败: {e}")
                print(f"尝试使用pip安装 {dep}...")
                try:
                    self.run_command([
                        self.get_venv_pip(), "install", dep
                    ], timeout=120)
                    print(f"使用pip成功安装 {dep}")
                except PackagerError:
                    print(f"错误: 无法安装依赖 {dep}，可能会影响打包结果")
    
    def copy_source_files(self) -> Path:
        """复制源码文件到临时目录"""
        if not self.temp_dir:
            raise PackagerError("临时目录未创建")
        
        source_copy_dir = self.temp_dir / "source"
        source_copy_dir.mkdir()
        
        # 复制主文件
        main_file_copy = source_copy_dir / self.source_file.name
        shutil.copy2(self.source_file, main_file_copy)
        
        # 复制同目录下的其他Python文件
        for py_file in self.source_dir.glob("*.py"):
            if py_file != self.source_file:
                shutil.copy2(py_file, source_copy_dir / py_file.name)
        
        # 如果存在子包，也复制过来
        for item in self.source_dir.iterdir():
            if (item.is_dir() and 
                not item.name.startswith('.') and 
                not item.name.startswith('__pycache__') and
                (item / "__init__.py").exists()):
                shutil.copytree(item, source_copy_dir / item.name)
        
        print(f"源码文件已复制到: {source_copy_dir}")
        return main_file_copy
    
    def run_pyinstaller(self, main_file: Path) -> Path:
        """使用pyinstaller打包应用"""
        if not self.venv_path:
            raise PackagerError("虚拟环境未创建")
        
        # 获取pyinstaller路径
        if os.name == 'nt':  # Windows
            pyinstaller_path = self.venv_path / "Scripts" / "pyinstaller.exe"
        else:  # Unix-like
            pyinstaller_path = self.venv_path / "bin" / "pyinstaller"
        
        if not pyinstaller_path.exists():
            raise PackagerError("pyinstaller未正确安装")
        
        # 设置输出目录
        dist_dir = self.temp_dir / "dist"
        build_dir = self.temp_dir / "build"
        
        print("开始使用pyinstaller打包...")
        
        # 构建pyinstaller命令
        cmd = [
            str(pyinstaller_path),
            "--onefile",  # 生成单个可执行文件
            "--clean",    # 清理临时文件
            "--noconfirm", # 不询问覆盖
            f"--distpath={dist_dir}",
            f"--workpath={build_dir}",
            f"--specpath={self.temp_dir}",
            str(main_file)
        ]
        
        # 设置环境变量，确保使用虚拟环境
        env = os.environ.copy()
        if os.name == 'nt':
            env["PATH"] = f"{self.venv_path / 'Scripts'}{os.pathsep}{env.get('PATH', '')}"
        else:
            env["PATH"] = f"{self.venv_path / 'bin'}{os.pathsep}{env.get('PATH', '')}"
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
                timeout=600,  # 10分钟超时
                check=True,
                env=env
            )
            
            if result.stdout.strip():
                print("PyInstaller输出:")
                print(result.stdout.strip())
                
        except subprocess.TimeoutExpired:
            raise PackagerError("PyInstaller打包超时")
        except subprocess.CalledProcessError as e:
            error_msg = f"PyInstaller打包失败\n"
            if e.stdout:
                error_msg += f"标准输出: {e.stdout}\n"
            if e.stderr:
                error_msg += f"错误输出: {e.stderr}\n"
            raise PackagerError(error_msg)
        
        # 查找生成的可执行文件
        if os.name == 'nt':
            exe_name = f"{self.app_name}.exe"
        else:
            exe_name = self.app_name
        
        exe_path = dist_dir / exe_name
        if not exe_path.exists():
            raise PackagerError(f"未找到生成的可执行文件: {exe_path}")
        
        print(f"打包完成: {exe_path}")
        return exe_path
    
    def copy_executable_to_source(self, exe_path: Path) -> Path:
        """将可执行文件复制到源码目录"""
        target_path = self.source_dir / exe_path.name
        
        # 如果目标文件已存在，先备份
        if target_path.exists():
            backup_path = self.source_dir / f"{exe_path.name}.backup"
            if backup_path.exists():
                backup_path.unlink()
            shutil.move(target_path, backup_path)
            print(f"已备份原文件为: {backup_path}")
        
        shutil.copy2(exe_path, target_path)
        print(f"可执行文件已复制到: {target_path}")
        
        return target_path
    
    def cleanup(self) -> None:
        """清理临时文件"""
        if self.temp_dir and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
                print(f"清理临时目录: {self.temp_dir}")
            except Exception as e:
                print(f"警告: 清理临时目录失败: {e}")
    
    def package(self, dependencies: List[str]) -> Path:
        """执行完整的打包流程"""
        try:
            # 创建临时环境
            self.create_temp_environment()
            
            # 创建虚拟环境
            self.create_virtual_environment()
            
            # 安装依赖
            self.install_dependencies(dependencies)
            
            # 复制源码文件
            main_file_copy = self.copy_source_files()
            
            # 执行pyinstaller打包
            exe_path = self.run_pyinstaller(main_file_copy)
            
            # 复制可执行文件到源码目录
            final_exe_path = self.copy_executable_to_source(exe_path)
            
            return final_exe_path
            
        finally:
            # 清理临时文件
            self.cleanup() 