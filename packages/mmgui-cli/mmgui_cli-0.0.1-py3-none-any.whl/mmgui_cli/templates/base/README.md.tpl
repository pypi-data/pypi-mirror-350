# 🚀 MMGUI 项目 - {{ project_name }}

> 使用 `mmgui-cli` 快速创建的桌面应用项目模板

本项目基于 [MMGUI](https://github.com/sandin/mmgui/) 构建，提供了一个快速开发 Python 桌面 GUI 应用的脚手架。

---

## 📁 项目结构概览

```
{{ project_name }}/
├── {{ project_module }}/     # 核心业务逻辑模块
│   ├── __init__.py
│   └── core.py
├── gui/                      # GUI 界面与交互逻辑
│   ├── __init__.py
│   ├── app.py                # 主程序入口
│   ├── functions.py          # 功能函数绑定
│   ├── function_registry.py
│   └── ui/
│       └── index.html        # 前端界面（可选模板）
├── scripts/                  # 脚本目录（启动后可删除）
│   ├── setup_dev.sh          # Linux/macOS 开发环境安装脚本
│   └── setup_dev.bat         # Windows 开发环境安装脚本
├── README.md                 # 当前文档
└── requirements.txt          # 项目依赖
```

---

## 🔧 安装与运行

### 1. 使用一键安装脚本（推荐）：

```bash
# Linux / macOS
./scripts/setup_dev.sh

# Windows
scripts\setup_dev.bat
```

### 3. 启动应用

```bash
python -m gui.app
```
or
```bash
mmgui_cli run
```