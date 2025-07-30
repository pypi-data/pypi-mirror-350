# mmgui-cli
快速创建mmgui项目
本项目基于 [MMGUI](https://github.com/sandin/mmgui/) 构建，提供了一个快速开发 Python 桌面 GUI 应用的脚手架。

## 🚀 快速开始

### 1. 新建一个项目
```bash
mkdir my_project && cd my_project
```

### 2. 新建虚拟环境并激活（推荐）
```bash
python -m venv .venv
.venv/Scripts/activate
```
### 3. 安装mmgui-cli
```bash
pip install mmgui-cli
```
### 4. 使用mmgui-cli初始化项目
```bash
mmgui_cli init <project_name>
```
- `project_name`: `可选`，项目名称，不提供时默认为当前目录名称
### 5. 安装项目依赖（可在init时一键安装并启动）
```bash
pip  install -r requirements.txt
```
### 6. 启动项目
```bash
mmgui_cli run
```


