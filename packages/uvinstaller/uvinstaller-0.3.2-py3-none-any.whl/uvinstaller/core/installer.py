"""UVInstaller核心类实现"""

import subprocess
import shutil
import os
import ast
import sys
import importlib.util
from pathlib import Path


class UVInstaller:
    """基于UV和PyInstaller的Python项目自动打包工具"""
    
    # 清华镜像源
    MIRROR_URL = "https://pypi.tuna.tsinghua.edu.cn/simple/"
    
    def __init__(self, debug=False):
        """初始化UVInstaller
        
        Args:
            debug: 是否启用调试模式
        """
        self.output_dir = "dist"
        self.detected_dependencies = set()
        self.debug = debug
        
    def _check_environment(self):
        """检查运行环境"""
        print("检查运行环境...")
        
        # 检查Python版本
        python_version = sys.version
        print(f"Python版本: {python_version}")
        
        # 检查当前工作目录
        current_dir = os.getcwd()
        print(f"当前工作目录: {current_dir}")
        
        # 检查写入权限
        try:
            test_file = os.path.join(current_dir, "test_write_permission.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("目录写入权限: 正常")
        except Exception as e:
            print(f"目录写入权限: 异常 - {e}")
            
        # 检查网络连接（通过ping镜像源）
        try:
            import urllib.request
            urllib.request.urlopen(self.MIRROR_URL, timeout=5)
            print(f"镜像源连接: 正常 ({self.MIRROR_URL})")
        except Exception as e:
            print(f"镜像源连接: 异常 - {e}")
            print("建议检查网络连接或尝试使用官方源")
            
        print("环境检查完成")
        
    def pack(self, entry_point):
        """打包Python项目为单个可执行文件
        
        Args:
            entry_point: 入口文件路径
        """
        print(f"开始打包项目: {entry_point}")
        
        # 检查运行环境
        self._check_environment()
        
        # 检查并安装UV环境
        self._ensure_uv_available()
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 检测依赖
        self._detect_dependencies(entry_point)
        
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
                    ["pip", "install", "-i", self.MIRROR_URL, "uv"], 
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
                    raise RuntimeError(f"UV安装失败，已尝试{max_retries}次。请手动执行: pip install -i {self.MIRROR_URL} uv")
                else:
                    print("稍后重试...")
                    
            except FileNotFoundError:
                raise RuntimeError(
                    "pip命令不可用，无法安装UV。\n"
                    f"请确保已正确安装Python和pip，或手动安装UV: pip install -i {self.MIRROR_URL} uv"
                )
    
    def _detect_dependencies(self, entry_point):
        """检测Python文件的依赖库"""
        print("检测项目依赖...")
        
        # 已分析的文件集合，避免重复分析
        self.analyzed_files = set()
        
        # 解析入口文件和相关的Python文件
        self._parse_imports_recursive(entry_point)
        
        # 如果有requirements.txt，也解析它
        if os.path.exists("requirements.txt"):
            self._parse_requirements_txt()
            
        print(f"检测到的第三方依赖: {', '.join(sorted(self.detected_dependencies)) if self.detected_dependencies else '无'}")
    
    def _parse_imports_recursive(self, file_path):
        """递归解析Python文件中的import语句"""
        # 转换为绝对路径并规范化
        abs_path = os.path.abspath(file_path)
        if abs_path in self.analyzed_files:
            return
        self.analyzed_files.add(abs_path)
        
        # 解析当前文件
        self._parse_imports(abs_path)
        
        # 查找同目录下可能被导入的其他Python文件
        try:
            current_dir = os.path.dirname(abs_path)
            for item in os.listdir(current_dir):
                if item.endswith('.py') and item != os.path.basename(abs_path):
                    other_file = os.path.join(current_dir, item)
                    if other_file not in self.analyzed_files:
                        # 简单检查是否可能被导入（通过检查是否有相同目录的导入）
                        if self._is_likely_imported(abs_path, item[:-3]):  # 移除.py扩展名
                            self._parse_imports_recursive(other_file)
        except OSError:
            pass  # 目录不可访问时跳过
    
    def _is_likely_imported(self, file_path, module_name):
        """检查模块是否可能被导入"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单的文本搜索，检查是否包含import语句
                return f"import {module_name}" in content or f"from {module_name}" in content
        except Exception:
            return False
    
    def _parse_imports(self, file_path):
        """解析Python文件中的import语句"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"警告：无法读取文件 {file_path}，跳过依赖检测")
                return
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"警告：解析文件 {file_path} 时发生语法错误: {e}")
            return
        
        # 遍历AST节点查找import语句
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._check_and_add_dependency(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._check_and_add_dependency(node.module)
    
    def _check_and_add_dependency(self, module_name):
        """检查模块是否为第三方依赖并添加到依赖列表"""
        # 提取顶级模块名
        top_level_module = module_name.split('.')[0]
        
        # 跳过内置模块和标准库模块
        if self._is_builtin_or_stdlib(top_level_module):
            return
        
        # 检查模块是否已安装
        if self._is_module_available(top_level_module):
            self.detected_dependencies.add(top_level_module)
    
    def _is_builtin_or_stdlib(self, module_name):
        """检查模块是否为内置模块或标准库模块"""
        # 内置模块
        builtin_modules = set(sys.builtin_module_names)
        if module_name in builtin_modules:
            return True
        
        # 常见标准库模块（Python 3.x）
        stdlib_modules = {
            'os', 'sys', 'datetime', 'time', 'json', 'urllib', 'http', 're',
            'math', 'random', 'collections', 'itertools', 'functools', 'operator',
            'pathlib', 'glob', 'shutil', 'tempfile', 'io', 'string', 'textwrap',
            'unicodedata', 'codecs', 'pickle', 'copy', 'gc', 'weakref', 'types',
            'inspect', 'ast', 'dis', 'traceback', 'warnings', 'contextlib',
            'threading', 'multiprocessing', 'concurrent', 'subprocess', 'signal',
            'socket', 'ssl', 'select', 'selectors', 'asyncio', 'email', 'mailbox',
            'csv', 'configparser', 'logging', 'argparse', 'getopt', 'readline',
            'rlcompleter', 'cmd', 'pdb', 'profile', 'pstats', 'timeit', 'trace',
            'unittest', 'doctest', 'xmlrpc', 'xml', 'html', 'sqlite3', 'zlib',
            'gzip', 'bz2', 'lzma', 'tarfile', 'zipfile', 'hashlib', 'hmac',
            'secrets', 'base64', 'binascii', 'struct', 'array', 'decimal',
            'fractions', 'statistics', 'tkinter', 'turtle'
        }
        
        return module_name in stdlib_modules
    
    def _is_module_available(self, module_name):
        """检查模块是否可用（已安装）"""
        try:
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            return False
    
    def _parse_requirements_txt(self):
        """解析requirements.txt文件"""
        try:
            with open('requirements.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 提取包名（忽略版本要求）
                        if '==' in line:
                            package_name = line.split('==')[0].strip()
                        elif '>=' in line:
                            package_name = line.split('>=')[0].strip()
                        elif '<=' in line:
                            package_name = line.split('<=')[0].strip()
                        elif '>' in line:
                            package_name = line.split('>')[0].strip()
                        elif '<' in line:
                            package_name = line.split('<')[0].strip()
                        else:
                            package_name = line.strip()
                        
                        if package_name:
                            self.detected_dependencies.add(package_name)
        except Exception as e:
            print(f"警告：解析requirements.txt时出错: {e}")
    
    def _create_uv_env(self):
        """创建UV虚拟环境"""
        print("创建UV虚拟环境...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                cmd = ["uv", "venv", ".venv"]
                print(f"执行命令: {' '.join(cmd)}")  # 显示实际执行的命令
                if self.debug:
                    # 调试模式下显示实时输出
                    result = subprocess.run(cmd, check=True)
                else:
                    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                    if result.stdout:
                        print(f"创建输出: {result.stdout}")
                print("UV虚拟环境创建成功")
                return
            except subprocess.CalledProcessError as e:
                error_msg = f"创建虚拟环境失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if not self.debug and hasattr(e, 'stdout') and e.stdout:
                    error_msg += f"\n标准输出: {e.stdout}"
                if not self.debug and hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误输出: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    print("建议解决方案：")
                    print(f"1. 手动执行命令验证: {' '.join(cmd)}")
                    print("2. 检查当前目录是否有写入权限")
                    print("3. 确认UV是否正确安装和配置")
                    print("4. 删除现有的.venv目录后重试")
                    raise RuntimeError(f"UV虚拟环境创建失败，已尝试{max_retries}次")
                else:
                    print("稍后重试...")
        
    def _install_dependencies(self):
        """安装依赖"""
        print("安装项目依赖...")
        
        # 安装pyinstaller
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                print(f"正在安装PyInstaller... (尝试 {attempt + 1}/{max_retries})")
                cmd = ["uv", "pip", "install", "-i", self.MIRROR_URL, "pyinstaller>=5.0"]
                print(f"执行命令: {' '.join(cmd)}")  # 显示实际执行的命令
                if self.debug:
                    # 调试模式下显示实时输出
                    result = subprocess.run(cmd, check=True)
                else:
                    result = subprocess.run(
                        cmd, 
                        check=True, 
                        capture_output=True, 
                        text=True
                    )
                    if result.stdout:
                        print(f"安装输出: {result.stdout}")
                print("PyInstaller安装成功")
                break
            except subprocess.CalledProcessError as e:
                error_msg = f"PyInstaller安装失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if not self.debug and hasattr(e, 'stdout') and e.stdout:
                    error_msg += f"\n标准输出: {e.stdout}"
                if not self.debug and hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误输出: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    print("建议解决方案：")
                    print(f"1. 手动执行命令验证: {' '.join(cmd)}")
                    print("2. 检查网络连接和镜像源是否可用")
                    print("3. 尝试使用官方源: https://pypi.org/simple/")
                    print("4. 检查Python版本是否支持PyInstaller>=5.0")
                    raise RuntimeError(f"PyInstaller安装失败，已尝试{max_retries}次")
                else:
                    print("稍后重试...")
        
        # 安装检测到的第三方依赖
        if self.detected_dependencies:
            dependencies_list = list(self.detected_dependencies)
            for attempt in range(max_retries):
                try:
                    print(f"正在安装检测到的依赖: {', '.join(dependencies_list)}... (尝试 {attempt + 1}/{max_retries})")
                    cmd = ["uv", "pip", "install", "-i", self.MIRROR_URL] + dependencies_list
                    print(f"执行命令: {' '.join(cmd)}")  # 显示实际执行的命令
                    if self.debug:
                        # 调试模式下显示实时输出
                        result = subprocess.run(cmd, check=True)
                    else:
                        result = subprocess.run(
                            cmd, 
                            check=True, 
                            capture_output=True, 
                            text=True
                        )
                        if result.stdout:
                            print(f"安装输出: {result.stdout}")
                    print("检测到的依赖安装成功")
                    break
                except subprocess.CalledProcessError as e:
                    error_msg = f"依赖安装失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                    if not self.debug and hasattr(e, 'stdout') and e.stdout:
                        error_msg += f"\n标准输出: {e.stdout}"
                    if not self.debug and hasattr(e, 'stderr') and e.stderr:
                        error_msg += f"\n错误输出: {e.stderr}"
                    print(error_msg)
                    
                    if attempt == max_retries - 1:
                        print(f"警告：检测到的依赖安装失败，已尝试{max_retries}次")
                        print("这可能会导致打包失败，请检查依赖是否正确")
                        print("建议解决方案：")
                        print(f"1. 手动执行命令验证: {' '.join(cmd)}")
                        print("2. 检查网络连接和镜像源是否可用")
                        print("3. 确认依赖包名称是否正确")
                        print("4. 尝试使用官方源: https://pypi.org/simple/")
                        print("5. 检查是否需要特定版本的依赖")
                    else:
                        print("稍后重试...")
        else:
            print("未检测到第三方依赖")
        
        # 安装requirements.txt中的依赖（如果存在）
        if os.path.exists("requirements.txt"):
            for attempt in range(max_retries):
                try:
                    print(f"正在从requirements.txt安装项目依赖... (尝试 {attempt + 1}/{max_retries})")
                    cmd = ["uv", "pip", "install", "-i", self.MIRROR_URL, "-r", "requirements.txt"]
                    print(f"执行命令: {' '.join(cmd)}")  # 显示实际执行的命令
                    if self.debug:
                        # 调试模式下显示实时输出
                        result = subprocess.run(cmd, check=True)
                    else:
                        result = subprocess.run(
                            cmd, 
                            check=True, 
                            capture_output=True, 
                            text=True
                        )
                        if result.stdout:
                            print(f"安装输出: {result.stdout}")
                    print("requirements.txt依赖安装成功")
                    break
                except subprocess.CalledProcessError as e:
                    error_msg = f"requirements.txt依赖安装失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                    if not self.debug and hasattr(e, 'stdout') and e.stdout:
                        error_msg += f"\n标准输出: {e.stdout}"
                    if not self.debug and hasattr(e, 'stderr') and e.stderr:
                        error_msg += f"\n错误输出: {e.stderr}"
                    print(error_msg)
                    
                    if attempt == max_retries - 1:
                        print(f"警告：requirements.txt依赖安装失败，已尝试{max_retries}次")
                        print("建议解决方案：")
                        print(f"1. 手动执行命令验证: {' '.join(cmd)}")
                        print("2. 检查requirements.txt文件格式是否正确")
                        print("3. 检查网络连接和镜像源是否可用")
                        print("4. 尝试使用官方源: https://pypi.org/simple/")
                    else:
                        print("稍后重试...")
        else:
            print("未找到requirements.txt文件")
    
    def _run_pyinstaller(self, entry_point):
        """执行PyInstaller打包为单个文件"""
        print("执行PyInstaller打包...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                cmd = ["uv", "run", "pyinstaller", entry_point, "--distpath", self.output_dir, "--onefile"]
                print(f"执行命令: {' '.join(cmd)}")  # 显示实际执行的命令
                print(f"正在打包... (尝试 {attempt + 1}/{max_retries})")
                if self.debug:
                    # 调试模式下显示实时输出
                    result = subprocess.run(cmd, check=True)
                else:
                    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                    if result.stdout:
                        print(f"打包输出: {result.stdout}")
                print("PyInstaller打包成功")
                return
            except subprocess.CalledProcessError as e:
                error_msg = f"PyInstaller打包失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                if not self.debug and hasattr(e, 'stdout') and e.stdout:
                    error_msg += f"\n标准输出: {e.stdout}"
                if not self.debug and hasattr(e, 'stderr') and e.stderr:
                    error_msg += f"\n错误输出: {e.stderr}"
                print(error_msg)
                
                if attempt == max_retries - 1:
                    print("建议解决方案：")
                    print(f"1. 手动执行命令验证: {' '.join(cmd)}")
                    print("2. 检查入口文件是否存在和可执行")
                    print("3. 确认所有依赖都已正确安装")
                    print("4. 检查代码中是否有语法错误")
                    print("5. 尝试使用 --debug 参数获取更多信息")
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