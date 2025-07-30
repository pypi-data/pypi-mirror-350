# 变更日志

本文件记录了UVInstaller项目的所有重要变更。

格式基于[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [0.3.0] - 2025-05-25

### 新增
- **智能依赖检测功能**：自动分析Python文件中的import语句，检测第三方依赖库
- 递归依赖分析：支持分析项目中相关Python文件的依赖关系
- AST语法树解析：使用Python AST模块精确解析import语句
- 标准库过滤：自动过滤Python内置模块和标准库，只安装第三方依赖
- 多编码支持：支持UTF-8和GBK编码的Python文件
- **UV构建支持**：新增基于UV的现代化构建和发布方案

### 改进
- 增强依赖安装流程：先安装检测到的依赖，再安装requirements.txt中的依赖
- 优化错误处理：对依赖检测过程中的语法错误和编码错误提供友好提示
- 改进日志输出：显示检测到的第三方依赖列表，提供更清晰的执行反馈
- 现代化构建配置：完全基于pyproject.toml标准

### 修复
- **修复核心Bug**：解决了对指定Python文件打包前没有读取并安装所需依赖库的问题
- 修复依赖检测方法未正确调用的问题
- 修复模块可用性检查逻辑

### 技术变更
- 新增ast、sys、importlib.util模块导入
- 重构_detect_dependencies方法，支持传入entry_point参数
- 新增_parse_imports_recursive、_is_likely_imported等辅助方法
- 完善_is_builtin_or_stdlib方法，覆盖更多标准库模块
- 删除setup.py，完全使用pyproject.toml配置
- 添加UV构建配置和开发依赖管理
- 新增UV发布指南文档

## [0.2.0] - 2025-05-24

### 新增
- **UV自动安装功能**：首次运行时自动检测并安装UV环境
- UV环境检查和验证机制
- 网络请求重试机制（最多3次重试）
- 更详细的错误处理和用户提示信息
- 支持用户中断操作（Ctrl+C）

### 改进
- 增强所有网络相关操作的重试机制
- 优化错误信息显示，提供更友好的用户体验
- 改进依赖管理，UV和PyInstaller均在运行时动态安装
- 更新系统要求说明，仅需Python和pip

### 修复
- 修复当UV未安装时程序崩溃的问题
- 修复网络不稳定时安装失败的问题

### 技术变更
- 从setup.py中移除pyinstaller硬依赖
- 项目状态从Alpha升级到Beta
- 更新README.md文档，增加UV自动安装说明

## [0.1.1] - 2024-12-18

### 修复
- 修复打包输出路径问题
- 改进临时文件清理机制

## [0.1.0] - 2024-12-18

### 新增
- 基本的Python项目打包功能
- UV虚拟环境管理
- PyInstaller集成
- 自动依赖检测和安装
- 临时文件清理功能
- 命令行接口（uvi命令）

### 功能特性
- 支持requirements.txt依赖文件
- 生成单个可执行文件（--onefile模式）
- 自动清理build目录和.spec文件
- 跨平台支持（Windows/Linux/macOS） 