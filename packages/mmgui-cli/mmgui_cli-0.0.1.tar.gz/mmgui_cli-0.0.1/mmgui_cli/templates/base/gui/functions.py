from gui.function_registry import FunctionRegistry
from core_package.core import do_something

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
    print(f"Hello {msg} from {win}")


@registry.register("add_numbers")
def add_numbers(a, b):  # 不需要 win
    return a + b
