# uvinstaller

🚀 **uvinstaller** 是一个自动化Python应用打包工具，使用 `uv` 和 `pyinstaller` 将Python脚本打包成单个可执行文件。

## ✨ 特性

- 🔧 **自动安装uv**: 如果系统中没有uv，会自动下载安装
- 📦 **智能依赖分析**: 自动分析Python文件的所有依赖关系
- 🌏 **虚拟环境隔离**: 使用uv创建干净的虚拟环境进行打包
- 📱 **单文件输出**: 生成单个可执行文件，便于分发
- 🧹 **自动清理**: 打包完成后自动清理临时文件
- 🖥️ **跨平台支持**: 支持Windows、Linux、macOS

## 🚀 快速开始

### 安装

```bash
pip install uvinstaller
```

### 使用

```bash
uvi your_script.py
```

就是这么简单！工具会自动：
1. 检查并安装uv环境
2. 分析脚本的所有依赖
3. 创建虚拟环境并安装依赖
4. 使用pyinstaller打包
5. 将可执行文件复制到源码目录

## 📋 使用示例

### 基本用法

```bash
# 打包单个Python文件
uvi app.py

# 打包带路径的文件
uvi src/main.py
```

### 支持的文件结构

```
my_project/
├── main.py          # 主入口文件
├── utils.py         # 本地模块
├── config/          # 本地包
│   └── __init__.py
└── requirements.txt # 依赖文件(可选)
```

运行 `uvi main.py` 会自动：
- 分析 `main.py` 的导入
- 扫描同目录下的所有Python文件
- 读取 `requirements.txt`（如果存在）
- 安装所有必要的依赖

## 🔧 工作原理

1. **环境检查**: 检查系统是否有uv，没有则自动安装
2. **依赖分析**: 使用AST分析Python文件的导入语句
3. **环境创建**: 使用uv创建临时虚拟环境
4. **依赖安装**: 在虚拟环境中安装pyinstaller和项目依赖
5. **文件复制**: 复制源码到临时目录
6. **执行打包**: 使用pyinstaller生成单文件可执行程序
7. **文件复制**: 将可执行文件复制到源码目录
8. **清理临时文件**: 删除所有临时文件和目录

## 🎯 适用场景

- 🖥️ **桌面应用**: 将Python GUI应用打包为exe
- 🔧 **命令行工具**: 将脚本打包为可执行工具
- 📊 **数据处理脚本**: 打包数据分析脚本
- 🌐 **自动化脚本**: 打包运维和自动化脚本
- 🎮 **游戏和娱乐**: 打包Python游戏

## 📁 项目结构

```
uvinstaller/
├── src/
│   └── uvinstaller/
│       ├── __init__.py
│       ├── cli.py              # 命令行接口
│       ├── uv_installer.py     # uv自动安装
│       ├── dependency_analyzer.py  # 依赖分析
│       └── packager.py         # 打包器
├── pyproject.toml              # 项目配置
├── build_and_publish.py        # 构建发布脚本
└── README.md
```

## 🛠️ 开发

### 本地开发环境

```bash
# 克隆代码
git clone https://github.com/uvinstaller/uvinstaller.git
cd uvinstaller

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest
```

### 构建和发布

使用提供的构建脚本：

```bash
python build_and_publish.py
```

脚本会自动：
- 清理构建目录
- 安装构建依赖
- 构建wheel和源码包
- 检查包的完整性
- 可选上传到PyPI

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [uv](https://github.com/astral-sh/uv) - 快速Python包管理器
- [PyInstaller](https://github.com/pyinstaller/pyinstaller) - Python应用打包工具

## 📞 支持

如果遇到问题或有建议，请：

1. 查看 [Issues](https://github.com/uvinstaller/uvinstaller/issues)
2. 创建新的Issue
3. 联系维护者

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！ 