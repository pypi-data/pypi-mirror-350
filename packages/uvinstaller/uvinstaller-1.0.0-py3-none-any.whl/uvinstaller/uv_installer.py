"""
uv自动安装模块
负责检测系统中是否存在uv，如果不存在则自动安装
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Optional
import requests


class UvInstallerError(Exception):
    """uv安装器异常"""
    pass


class UvInstaller:
    """uv自动安装器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        
    def is_uv_installed(self) -> bool:
        """检查uv是否已安装"""
        return shutil.which("uv") is not None
    
    def get_uv_download_url(self) -> str:
        """获取uv下载链接"""
        base_url = "https://github.com/astral-sh/uv/releases/latest/download/"
        
        if self.system == "windows":
            if "x86_64" in self.arch or "amd64" in self.arch:
                return f"{base_url}uv-x86_64-pc-windows-msvc.zip"
            else:
                return f"{base_url}uv-i686-pc-windows-msvc.zip"
        elif self.system == "linux":
            if "x86_64" in self.arch or "amd64" in self.arch:
                return f"{base_url}uv-x86_64-unknown-linux-gnu.tar.gz"
            elif "aarch64" in self.arch or "arm64" in self.arch:
                return f"{base_url}uv-aarch64-unknown-linux-gnu.tar.gz"
            else:
                return f"{base_url}uv-i686-unknown-linux-gnu.tar.gz"
        elif self.system == "darwin":
            if "arm" in self.arch or "aarch64" in self.arch:
                return f"{base_url}uv-aarch64-apple-darwin.tar.gz"
            else:
                return f"{base_url}uv-x86_64-apple-darwin.tar.gz"
        else:
            raise UvInstallerError(f"不支持的系统: {self.system}")
    
    def download_file(self, url: str, dest_path: Path) -> None:
        """下载文件"""
        try:
            print(f"正在下载 uv 从 {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"下载完成: {dest_path}")
        except requests.exceptions.RequestException as e:
            raise UvInstallerError(f"下载失败: {e}")
    
    def extract_archive(self, archive_path: Path, extract_dir: Path) -> None:
        """解压文件"""
        try:
            if archive_path.suffix == '.zip':
                import zipfile
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            elif archive_path.suffix == '.gz':
                import tarfile
                with tarfile.open(archive_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(extract_dir)
            else:
                raise UvInstallerError(f"不支持的压缩格式: {archive_path.suffix}")
        except Exception as e:
            raise UvInstallerError(f"解压失败: {e}")
    
    def install_uv(self) -> bool:
        """安装uv"""
        if self.is_uv_installed():
            print("uv 已经安装")
            return True
        
        print("uv 未安装，开始自动安装...")
        
        try:
            # 创建临时目录
            temp_dir = Path.home() / ".uvinstaller_temp"
            temp_dir.mkdir(exist_ok=True)
            
            # 下载uv
            download_url = self.get_uv_download_url()
            archive_name = download_url.split('/')[-1]
            archive_path = temp_dir / archive_name
            
            self.download_file(download_url, archive_path)
            
            # 解压
            extract_dir = temp_dir / "extracted"
            extract_dir.mkdir(exist_ok=True)
            self.extract_archive(archive_path, extract_dir)
            
            # 查找uv可执行文件
            uv_exe = None
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file == "uv" or file == "uv.exe":
                        uv_exe = Path(root) / file
                        break
                if uv_exe:
                    break
            
            if not uv_exe:
                raise UvInstallerError("在下载的文件中未找到uv可执行文件")
            
            # 确定安装目录
            if self.system == "windows":
                install_dir = Path.home() / "AppData" / "Local" / "uvinstaller" / "bin"
            else:
                install_dir = Path.home() / ".local" / "bin"
            
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制uv到安装目录
            uv_target = install_dir / uv_exe.name
            shutil.copy2(uv_exe, uv_target)
            
            # 设置可执行权限 (非Windows系统)
            if self.system != "windows":
                uv_target.chmod(0o755)
            
            # 添加到PATH环境变量提示
            if str(install_dir) not in os.environ.get("PATH", ""):
                print(f"注意: 请将 {install_dir} 添加到PATH环境变量中")
                print(f"或者重新启动终端后再次运行此程序")
                
                # 临时添加到当前会话的PATH
                os.environ["PATH"] = f"{install_dir}{os.pathsep}{os.environ.get('PATH', '')}"
            
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            print("uv 安装完成")
            return True
            
        except Exception as e:
            print(f"安装uv失败: {e}")
            # 清理临时文件
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)
            return False
    
    def ensure_uv_available(self) -> bool:
        """确保uv可用"""
        if self.is_uv_installed():
            return True
        
        return self.install_uv() 