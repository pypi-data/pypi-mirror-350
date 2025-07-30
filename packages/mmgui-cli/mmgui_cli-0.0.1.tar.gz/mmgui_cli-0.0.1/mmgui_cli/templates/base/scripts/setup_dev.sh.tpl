#!/bin/bash
set -e

echo "🔌 正在激活虚拟环境..."
source .venv/bin/activate

echo "📦 正在安装依赖..."
pip install -r requirements.txt

echo "🚀 启动应用..."
python -m gui.app