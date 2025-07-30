import sys, os
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
