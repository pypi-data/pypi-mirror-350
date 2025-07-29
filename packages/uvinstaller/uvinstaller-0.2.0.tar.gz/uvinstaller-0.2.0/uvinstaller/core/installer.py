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
        
        # 检查并安装UV环境
        self._ensure_uv_available()
        
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
    
    def _ensure_uv_available(self):
        """确保UV环境可用，如果没有安装则自动安装"""
        print("检查UV环境...")
        
        # 检查uv命令是否可用
        try:
            result = subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
            print(f"UV环境已就绪 - {result.stdout.strip()}")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("未检测到UV环境，正在自动安装...")
            
        # 自动安装UV，使用无限重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"正在安装UV... (尝试 {attempt + 1}/{max_retries})")
                
                # 安装UV
                install_result = subprocess.run(
                    ["pip", "install", "uv"], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                print("UV安装成功")
                
                # 验证安装
                verify_result = subprocess.run(
                    ["uv", "--version"], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                print(f"UV环境验证成功 - {verify_result.stdout.strip()}")
                return
                
            except subprocess.CalledProcessError as e:
                error_msg = f"安装失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误详情: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    raise RuntimeError(f"UV安装失败，已尝试{max_retries}次。请手动执行: pip install uv")
                else:
                    print("稍后重试...")
                    
            except FileNotFoundError:
                raise RuntimeError(
                    "pip命令不可用，无法安装UV。\n"
                    "请确保已正确安装Python和pip，或手动安装UV: pip install uv"
                )
    
    def _detect_dependencies(self):
        """检测项目依赖"""
        print("检测项目依赖...")
        # 检查requirements.txt文件
        
    def _create_uv_env(self):
        """创建UV虚拟环境"""
        print("创建UV虚拟环境...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                subprocess.run(["uv", "venv", ".venv"], check=True, capture_output=True, text=True)
                print("UV虚拟环境创建成功")
                return
            except subprocess.CalledProcessError as e:
                error_msg = f"创建虚拟环境失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误详情: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    raise RuntimeError(f"UV虚拟环境创建失败，已尝试{max_retries}次")
                else:
                    print("稍后重试...")
        
    def _install_dependencies(self):
        """安装依赖"""
        print("安装项目依赖...")
        
        max_retries = 3
        
        # 安装pyinstaller
        for attempt in range(max_retries):
            try:
                print(f"正在安装PyInstaller... (尝试 {attempt + 1}/{max_retries})")
                subprocess.run(
                    ["uv", "pip", "install", "pyinstaller>=5.0"], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                print("PyInstaller安装成功")
                break
            except subprocess.CalledProcessError as e:
                error_msg = f"PyInstaller安装失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误详情: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    raise RuntimeError(f"PyInstaller安装失败，已尝试{max_retries}次")
                else:
                    print("稍后重试...")
        
        # 安装项目依赖
        if os.path.exists("requirements.txt"):
            for attempt in range(max_retries):
                try:
                    print(f"正在安装项目依赖... (尝试 {attempt + 1}/{max_retries})")
                    subprocess.run(
                        ["uv", "pip", "install", "-r", "requirements.txt"], 
                        check=True, 
                        capture_output=True, 
                        text=True
                    )
                    print("项目依赖安装成功")
                    break
                except subprocess.CalledProcessError as e:
                    error_msg = f"项目依赖安装失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                    if hasattr(e, 'stderr') and e.stderr:
                        error_msg += f"\n错误详情: {e.stderr}"
                    print(error_msg)
                    
                    if attempt == max_retries - 1:
                        raise RuntimeError(f"项目依赖安装失败，已尝试{max_retries}次")
                    else:
                        print("稍后重试...")
        else:
            print("未找到requirements.txt文件，跳过项目依赖安装")
        
    def _run_pyinstaller(self, entry_point):
        """执行PyInstaller打包为单个文件"""
        print("执行PyInstaller打包...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                cmd = ["uv", "run", "pyinstaller", entry_point, "--distpath", self.output_dir, "--onefile"]
                print(f"正在打包... (尝试 {attempt + 1}/{max_retries})")
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                print("PyInstaller打包成功")
                return
            except subprocess.CalledProcessError as e:
                error_msg = f"PyInstaller打包失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误详情: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    raise RuntimeError(f"PyInstaller打包失败，已尝试{max_retries}次")
                else:
                    print("稍后重试...")
    
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