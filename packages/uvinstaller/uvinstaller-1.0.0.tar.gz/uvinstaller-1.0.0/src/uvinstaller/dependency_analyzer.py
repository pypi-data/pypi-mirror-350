"""
依赖分析模块
负责分析Python文件的依赖关系，提取需要安装的包
"""

import ast
import os
import sys
from pathlib import Path
from typing import Set, List, Optional, Dict
import re


class DependencyAnalyzerError(Exception):
    """依赖分析器异常"""
    pass


class DependencyAnalyzer:
    """Python文件依赖分析器"""
    
    # 标准库模块列表 (Python 3.8+)
    STDLIB_MODULES = {
        'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 
        'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins',
        'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
        'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
        'contextlib', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv', 'ctypes', 'curses',
        'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils',
        'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler',
        'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib',
        'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip',
        'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp',
        'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword',
        'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap',
        'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt',
        'multiprocessing', 'netrc', 'nntplib', 'numbers', 'operator', 'optparse', 'os',
        'ossaudiodev', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil',
        'platform', 'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats',
        'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random',
        're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched',
        'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal',
        'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'sqlite3',
        'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess',
        'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'tabnanny', 'tarfile',
        'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'threading', 'time',
        'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc',
        'tty', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest',
        'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser',
        'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile',
        'zipimport', 'zlib', '__future__', '__main__'
    }
    
    def __init__(self):
        self.analyzed_files: Set[Path] = set()
        self.dependencies: Set[str] = set()
    
    def extract_imports_from_ast(self, file_path: Path) -> Set[str]:
        """从AST中提取导入的模块"""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
                        
        except SyntaxError as e:
            print(f"警告: 文件 {file_path} 有语法错误，跳过分析: {e}")
        except Exception as e:
            print(f"警告: 分析文件 {file_path} 时出错: {e}")
            
        return imports
    
    def extract_imports_from_regex(self, file_path: Path) -> Set[str]:
        """使用正则表达式提取导入（备用方法）"""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配 import 语句
            import_pattern = r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)'
            from_import_pattern = r'^\s*from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import'
            
            for line in content.split('\n'):
                # 跳过注释行
                if line.strip().startswith('#'):
                    continue
                    
                # 匹配 import 语句
                match = re.match(import_pattern, line)
                if match:
                    modules = match.group(1).split(',')
                    for module in modules:
                        imports.add(module.strip().split('.')[0])
                
                # 匹配 from import 语句
                match = re.match(from_import_pattern, line)
                if match:
                    imports.add(match.group(1).split('.')[0])
                    
        except Exception as e:
            print(f"警告: 使用正则表达式分析文件 {file_path} 时出错: {e}")
            
        return imports
    
    def is_local_module(self, module_name: str, file_path: Path) -> bool:
        """检查模块是否是本地模块"""
        file_dir = file_path.parent
        
        # 检查是否存在同名的.py文件
        local_py_file = file_dir / f"{module_name}.py"
        if local_py_file.exists():
            return True
            
        # 检查是否存在同名的目录（包）
        local_dir = file_dir / module_name
        if local_dir.is_dir() and (local_dir / "__init__.py").exists():
            return True
            
        return False
    
    def analyze_file(self, file_path: Path) -> Set[str]:
        """分析单个Python文件的依赖"""
        if file_path in self.analyzed_files:
            return set()
            
        self.analyzed_files.add(file_path)
        
        if not file_path.exists() or file_path.suffix != '.py':
            return set()
        
        print(f"分析文件: {file_path}")
        
        # 首先尝试AST方法，如果失败则使用正则表达式
        imports = self.extract_imports_from_ast(file_path)
        if not imports:
            imports = self.extract_imports_from_regex(file_path)
        
        # 过滤掉标准库模块和本地模块
        external_imports = set()
        for module in imports:
            if (module not in self.STDLIB_MODULES and 
                not self.is_local_module(module, file_path) and
                not module.startswith('_')):  # 排除内部模块
                external_imports.add(module)
        
        return external_imports
    
    def analyze_directory(self, directory_path: Path) -> Set[str]:
        """分析目录中所有Python文件的依赖"""
        all_dependencies = set()
        
        for py_file in directory_path.rglob("*.py"):
            dependencies = self.analyze_file(py_file)
            all_dependencies.update(dependencies)
            
        return all_dependencies
    
    def analyze_project(self, entry_file: Path) -> Set[str]:
        """分析整个项目的依赖"""
        if not entry_file.exists():
            raise DependencyAnalyzerError(f"文件不存在: {entry_file}")
        
        # 分析入口文件
        dependencies = self.analyze_file(entry_file)
        
        # 分析入口文件所在目录的其他Python文件
        project_dir = entry_file.parent
        dir_dependencies = self.analyze_directory(project_dir)
        dependencies.update(dir_dependencies)
        
        # 检查是否有requirements.txt
        requirements_file = project_dir / "requirements.txt"
        if requirements_file.exists():
            req_dependencies = self.parse_requirements_file(requirements_file)
            dependencies.update(req_dependencies)
            print(f"从 requirements.txt 中发现 {len(req_dependencies)} 个依赖")
        
        self.dependencies = dependencies
        return dependencies
    
    def parse_requirements_file(self, requirements_file: Path) -> Set[str]:
        """解析requirements.txt文件"""
        dependencies = set()
        
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 移除版本约束
                        package = re.split(r'[>=<!=]', line)[0].strip()
                        if package:
                            dependencies.add(package)
        except Exception as e:
            print(f"警告: 解析 requirements.txt 时出错: {e}")
            
        return dependencies
    
    def get_dependencies_list(self) -> List[str]:
        """获取依赖列表"""
        return sorted(list(self.dependencies)) 