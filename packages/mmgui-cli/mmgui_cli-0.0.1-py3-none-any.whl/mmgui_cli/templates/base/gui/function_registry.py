import inspect


class FunctionRegistry:
    def __init__(self):
        self.functions = {}

    def register(self, name):
        """装饰器，用于注册函数"""

        def decorator(func):
            self.functions[name] = func
            return func

        return decorator

    def bind_all(self, webview, win=None):
        """将所有注册的函数绑定到 webview，并注入 win"""

        for name, func in self.functions.items():
            if self._needs_win(func):  # 根据函数定义自动决定是否注入 win
                wrapped_func = lambda *args, _func=func, _win=win, **kwargs: _func(
                    _win, *args, **kwargs
                )
                webview.bind_function(name, wrapped_func)
            else:
                webview.bind_function(name, func)

    def _needs_win(self, func):
        """
        判断函数是否需要注入 win：
        - 第一个参数名为 'win'，则认为需要
        """
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        return len(params) > 0 and params[0] == "win"
