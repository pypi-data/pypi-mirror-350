import os
import sys


def create_project_structure(project_name):
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        return

    # 创建主目录
    os.makedirs(project_name)
    os.chdir(project_name)

    # 创建项目包目录
    os.makedirs(os.path.join(project_name))
    os.makedirs(os.path.join("gui"))
    os.makedirs(os.path.join("gui", "ui"))

    # 创建 gui 子目录
    gui_dir = "gui"

    # 创建 README.md
    with open("README.md", "w") as f:
        f.write(f"# {project_name}\n\nA mmgui-based desktop application.")

    # 创建 requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("git+https://github.com/sandin/mmgui.git\n")

    # 创建 project_name/__init__.py
    with open(os.path.join(project_name, "__init__.py"), "w") as f:
        pass  # empty file

    # 创建 project_name/core.py
    with open(
        os.path.join(project_name, "core.py"), "w", encoding="utf-8"
    ) as f:
        f.write(
            """
# core.py
# 这里可以放置与业务逻辑相关的类和方法。
def do_something():
    print("Doing something...")
    return "Done!"
"""
        )

    # 创建 gui/__init__.py
    with open(os.path.join(gui_dir, "__init__.py"), "w") as f:
        pass  # empty file

    # 创建 gui/app.py
    with open(os.path.join(gui_dir, "app.py"), "w", encoding="utf-8") as f:
        f.write(
            """import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mmgui import App, BrowserWindow
from gui.functions import registry

app = App(headless=False)

def on_create(ctx):
    win = BrowserWindow({
        "title": "Demo - mmgui",
        "width": 1200,
        "height": 800,
        "dev_mode": True,
    })

    registry.bind_all(win.webview, win)
    win.webview.load_file(os.path.join(os.path.dirname(__file__), "ui/index.html"))
    win.show()

app.on("create", on_create)
app.run()
"""
        )

    # 创建 gui/function_registry.py
    with open(
        os.path.join(gui_dir, "function_registry.py"), "w", encoding="utf-8"
    ) as f:
        f.write(
            """import inspect


class FunctionRegistry:
    def __init__(self):
        self.functions = {}

    def register(self, name):
        \"\"\"装饰器，用于注册函数\"\"\"

        def decorator(func):
            self.functions[name] = func
            return func

        return decorator

    def bind_all(self, webview, win=None):
        \"\"\"将所有注册的函数绑定到 webview，并注入 win\"\"\"

        for name, func in self.functions.items():
            if self._needs_win(func):  # 根据函数定义自动决定是否注入 win
                wrapped_func = lambda *args, _func=func, _win=win, **kwargs: _func(
                    _win, *args, **kwargs
                )
                webview.bind_function(name, wrapped_func)
            else:
                webview.bind_function(name, func)

    def _needs_win(self, func):
        \"\"\"
        判断函数是否需要注入 win：
        - 第一个参数名为 'win'，则认为需要
        \"\"\"
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        return len(params) > 0 and params[0] == "win"
"""
        )

    # 创建 gui/functions.py
    with open(os.path.join(gui_dir, "functions.py"), "w", encoding="utf-8") as f:
        f.write(
            f"""from gui.function_registry import FunctionRegistry
from {project_name}.core import do_something

registry = FunctionRegistry()

@registry.register("open_file")
def open_file(win):
    files = win.show_file_dialog_for_file("打开文件", "Text File(*.txt)")
    return files[0] if files else None

@registry.register("get_version")
def get_version():
    do_something()
    return "v1.0.0"

@registry.register("hello_mmgui")
def hello_mmgui(win, msg):  # 需要 win
    print(f"Hello {{msg}} from {{win}}")

@registry.register("add_numbers")
def add_numbers(a, b):  # 不需要 win
    return a + b
"""
        )

    # 创建 gui/ui/index.html
    with open(os.path.join(gui_dir, "ui", "index.html"), "w", encoding="utf-8") as f:
        f.write(
            """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MMGUI Demo</title>
    <style>
      button {
        outline: none;
      }
    </style>
</head>
<body>
    <h1>Hello from MMGUI!</h1>
    <button onclick="testOpenFile()">Test Open File</button>
    <button onclick="testGetVersion()">Test Get Version</button>
    <button onclick="testHelloMmgui()">Test Hello Mmgui</button>
    <button onclick="testAddNumbers()">Test Add Numbers</button>

    <script>
        async function testOpenFile() {
            const res = await RPC.invoke("open_file");
            alert(res);
        }

        async function testGetVersion() {
            const res = await RPC.invoke("get_version");
            console.log(res); // 输出 v1.0.0
        }

        async function testHelloMmgui() {
            await RPC.invoke("hello_mmgui", { msg: "前端同学" });
        }

        async function testAddNumbers() {
            const res = await RPC.invoke("add_numbers", { a: 3, b: 5 });
            console.log(res); // 输出 8
        }
    </script>
</body>
</html>
"""
        )

    print(f"✅ Project '{project_name}' created successfully!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_mmgui_project.py project_name")
    else:
        project_name = sys.argv[1]
        create_project_structure(project_name)
