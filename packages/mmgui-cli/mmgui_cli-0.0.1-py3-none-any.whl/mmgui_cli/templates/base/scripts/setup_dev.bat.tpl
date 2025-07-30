@echo off
@chcp 65001 >nul

echo 🔌 正在激活虚拟环境...
call .venv\Scripts\activate

echo 📦 正在安装依赖...
pip install -r requirements.txt

echo 🚀 启动应用...
python -m gui.app